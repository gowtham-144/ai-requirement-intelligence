import streamlit as st
from llm_engine import analyze_requirement
from scoring_engine import calculate_final_score
from visualization import radar_chart
from pdf_generator import generate_pdf

import PyPDF2
from docx import Document


st.set_page_config(page_title="AI Requirement Intelligence", layout="wide")
st.title("AI Requirement Intelligence")


uploaded_file = st.file_uploader(
    "Upload Requirement Document (TXT, PDF, DOCX)",
    type=["txt", "pdf", "docx"]
)

text_input = ""


if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    try:
        if file_type == "txt":
            text_input = uploaded_file.read().decode("utf-8")

        elif file_type == "pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_input += page_text

        elif file_type == "docx":
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                text_input += para.text + "\n"

    except Exception as e:
        st.error(f"Error reading file: {e}")


manual_text = st.text_area("Or Paste Requirement Text Here")


if manual_text.strip():
    text_input = manual_text


if st.button("Analyze Requirement"):

    if not text_input.strip():
        st.warning("Please upload a document or enter requirement text.")
    else:
        
        text_input = text_input[:8000]

        with st.spinner("Analyzing requirement..."):
            result = analyze_requirement(text_input)

        if "error" in result:
            st.error(result["error"])
        else:
            final_score = calculate_final_score(result)

            
            st.subheader("Final Clarity Score")
            st.metric("Score", f"{final_score} / 100")

            
            score_data = {
                "AI Score": result["ai_clarity_score"],
                "Final Score": final_score
            }

            fig = radar_chart(score_data)
            st.plotly_chart(fig, use_container_width=True)

            
            pdf_file = generate_pdf(result)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Download PDF Report",
                    data=f,
                    file_name="requirement_report.pdf",
                    mime="application/pdf"
                )