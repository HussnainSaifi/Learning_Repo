import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="Research Paper & Article Summarizer",
    page_icon="📄",
    layout="centered"
)

# App Header
st.title("📄 AI Research Paper & Article Summarizer")
st.markdown("Upload any research paper, article, or CV in **PDF** format to instantly generate an executive summary and key insights.")

# File Uploader Widget
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Display file details
    file_details = {"Filename": uploaded_file.name, "Filesize": f"{uploaded_file.size / 1024:.2f} KB"}
    st.write("**File Details:**")
    st.json(file_details)

    if st.button("🚀 Generate Summary", type="primary"):
        with st.spinner("Analyzing document and generating AI summary... Please wait."):
            try:
                # FastAPI backend endpoint
                backend_url = "http://127.0.0.1:8000/summarize/"
                
                # Prepare file for multipart form-data upload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                
                # Send POST request to FastAPI
                response = requests.post(backend_url, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Summary Generated Successfully!")
                    
                    # Display Output inside an expandable box or markdown block
                    st.markdown("### 📋 Executive Summary & Takeaways")
                    st.markdown(result["summary"])
                else:
                    error_detail = response.json().get("detail", "Unknown error occurred")
                    st.error(f"❌ Server Error: {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error("⚠️ FastAPI backend se connection nahi ho saka! Make sure your uvicorn server is running (`uvicorn src.main:app --reload`).")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")