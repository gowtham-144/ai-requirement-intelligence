import streamlit as st
import json

from llm_engine import analyze_requirement
from ambiguity_detector import detect_ambiguities
from scoring_engine import calculate_clarity_score
from visualization import radar_chart
from pdf_exporter import generate_pdf

st.set_page_config(page_title="AI Requirement Intelligence", layout="wide")

st.title("AI Requirement Intelligence Engine")
st.caption("Transforming vague ideas into structured clarity")

st.divider()

# ---------------- INPUT ----------------
with st.container():
    st.subheader("Requirement Input")
    user_input = st.text_area("Enter your requirement", height=180)
    analyze = st.button("Analyze Requirement")

st.divider()

# ---------------- ANALYSIS ----------------
if analyze:

    if user_input.strip() == "":
        st.warning("Please enter a requirement.")
    else:
        with st.spinner("Analyzing requirement..."):

            ai_result = analyze_requirement(user_input)

            if "error" in ai_result:
                st.error(ai_result["error"])
            else:
                rule_ambiguities = detect_ambiguities(user_input)

                final_score = calculate_clarity_score(
                    ai_result["ai_clarity_score"],
                    len(rule_ambiguities)
                )

                # -------- Metrics --------
                col1, col2, col3 = st.columns(3)

                col1.metric("AI Score", ai_result["ai_clarity_score"])
                col2.metric("Final Score", final_score)
                col3.metric("Ambiguities Found", len(rule_ambiguities))

                st.divider()

                # -------- Confidence --------
                st.subheader("AI Confidence Level")
                st.progress(ai_result["ai_clarity_score"] / 100)

                st.divider()

                # -------- Radar --------
                quality_scores = {
                    "Functional": min(len(ai_result["functional_requirements"]) * 10, 100),
                    "Non-Functional": min(len(ai_result["non_functional_requirements"]) * 15, 100),
                    "Ambiguity Risk": max(100 - len(rule_ambiguities) * 10, 0),
                    "Risk Coverage": min(len(ai_result["technical_risks"]) * 20, 100),
                    "Requirement Depth": ai_result["ai_clarity_score"]
                }

                st.subheader("Requirement Quality Radar")
                st.plotly_chart(radar_chart(quality_scores), use_container_width=True)

                st.divider()

                # -------- Tabs --------
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["Summary", "Requirements", "Risks", "Improvements"]
                )

                with tab1:
                    st.write(ai_result["executive_summary"])

                with tab2:
                    st.subheader("Functional Requirements")
                    st.write(ai_result["functional_requirements"])

                    st.subheader("Non-Functional Requirements")
                    st.write(ai_result["non_functional_requirements"])

                with tab3:
                    st.subheader("Ambiguities")
                    st.write(ai_result["ambiguities"])
                    st.write(rule_ambiguities)

                    st.subheader("Technical Risks")
                    st.write(ai_result["technical_risks"])

                with tab4:
                    st.write(ai_result["improvements"])

                # -------- Downloads --------
                report_data = {
                    "executive_summary": ai_result["executive_summary"],
                    "functional_requirements": ai_result["functional_requirements"],
                    "non_functional_requirements": ai_result["non_functional_requirements"],
                    "ambiguities": ai_result["ambiguities"] + rule_ambiguities,
                    "technical_risks": ai_result["technical_risks"],
                    "improvements": ai_result["improvements"],
                    "final_score": final_score
                }

                pdf_file = generate_pdf(report_data)

                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "Download PDF Report",
                        f,
                        "requirement_report.pdf"
                    )
