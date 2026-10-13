import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from src.tools import tools_schema, query_company_policy, get_current_time

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class AgentEngine:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = "openai/gpt-oss-20b"

    def run(self, user_query: str) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an Enterprise AI Agent with tool-calling capabilities. "
                    "Use 'query_company_policy' when asked about company rules, leaves, or operations. "
                    "Use 'get_current_time' when asked about the current date or time. "
                    "Always respond to the user in their original language (or Roman Urdu if queried in Roman Urdu)."
                )
            },
            {"role": "user", "content": user_query}
        ]

        # Step 1: LLM Reasoning Call (with Tools schema attached)
        response = self.groq_client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tools_schema,
            tool_choice="auto",
            max_tokens=300
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Step 2: Check if Agent decided to call a Tool (Action)
        if tool_calls:
            messages.append(response_message)  # Append assistant's decision to history

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"🛠️ [AGENT DECISION]: Calling Tool -> '{function_name}' with args: {function_args}")

                # Execute Tool from src/tools.py
                if function_name == "query_company_policy":
                    tool_output = query_company_policy(query=function_args.get("query", ""))
                elif function_name == "get_current_time":
                    tool_output = get_current_time()
                else:
                    tool_output = "Tool not found."

                # Step 3: Append Tool Result back to conversation history
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_output
                })

            # Step 4: Final LLM Call to generate response based on Tool output
            final_response = self.groq_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=300
            )

            return final_response.choices[0].message.content

        # If no tool call was needed, return direct response
        return response_message.content


# Terminal Testing Execution
if __name__ == "__main__":
    agent = AgentEngine()

    print("\n--- Test 1: Policy Query (Tool Activation) ---")
    q1 = "Company mein leave apply karne ka tareeqa kya hai?"
    print(f"❓ User: {q1}")
    a1 = agent.run(q1)
    print(f"🤖 Agent: {a1}")

    print("\n--- Test 2: System Time Query (Tool Activation) ---")
    q2 = "Aaj kya date aur time ho raha hai?"
    print(f"❓ User: {q2}")
    a2 = agent.run(q2)
    print(f"🤖 Agent: {a2}")