import streamlit as st
from PyPDF2 import PdfReader
import docx
import io

# --- Streamlit page config ---
st.set_page_config(page_title="Smart Resume Reviewer - Hackathon Demo")

# --- Title ---
st.title("📄 Smart Resume Reviewer")
st.write("Upload your resume (PDF or DOCX) or paste text, then provide the target job role.")

# --- Step 1: Resume Input ---
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
resume_text_input = st.text_area("Or paste your resume text here", height=200)

resume_text = ""

# Extract text from PDF
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"
    # Extract text from DOCX
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            resume_text += para.text + "\n"

# Use pasted text if no file or in addition
if resume_text_input.strip():
    resume_text += resume_text_input + "\n"

# Display extracted resume
if resume_text:
    st.subheader("📑 Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=200)
else:
    st.info("Please upload a PDF/DOCX or paste your resume text to continue.")

# --- Step 2: Job Role & Job Description ---
if resume_text:
    st.subheader("🎯 Target Role / Job Description")
    job_role = st.text_input("Target job role (e.g., Data Scientist, Software Engineer)")
    job_desc = st.text_area("Optional: Paste job description here (helps AI tailor feedback)", height=200)

    if job_role.strip():
        st.success(f"Job role set to: **{job_role}**")
        if job_desc.strip():
            st.write("Job description provided.")
        else:
            st.info("No job description provided. AI feedback will use role only.")
    else:
        st.warning("Please enter the target job role to proceed.")

# --- Step 3: Mock AI Resume Feedback ---
if resume_text and job_role.strip():
    st.subheader("🤖 AI Resume Feedback (Mock Demo)")

    if st.button("Generate AI Feedback"):
        with st.spinner("Generating feedback..."):
            feedback = f"""
Strengths:
- Resume is well-structured and easy to read.
- Shows relevant experience for {job_role}.
- Includes technical skills and tools clearly.

Areas to Improve:
- Add measurable achievements (e.g., "improved X by Y%").
- Highlight soft skills like teamwork or leadership.
- Tailor experience more closely to {job_role}.

Missing Skills/Keywords:
- Consider adding skills relevant to {job_role}, e.g., specific frameworks or tools.

Suggestions:
- Use bullet points for clarity.
- Quantify achievements where possible.
- Keep resume concise (1-2 pages recommended).
"""
            st.text_area("AI Feedback", feedback, height=400)
