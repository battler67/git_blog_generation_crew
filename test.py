import streamlit as st
import os 
from datetime import datetime
from src.research_and_blog_crew.crew import ResearchAndBlogCrew

os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"

st.set_page_config(page_title="AI Research Crew", layout="wide")

st.title("Research & Blog Crew")
st.markdown("Generate structured research + blog content using AI agents.")

topic = st.text_input("Enter Research Topic")

if "Full_result" not in st.session_state:
    st.session_state.Full_result = ""

if st.button("Run Crew") and topic:

    inputs = {
        "topic": topic,
        "current_year": str(datetime.now().year)
    }

    with st.spinner(" Agents are working sequentially..."):

        crew_instance = ResearchAndBlogCrew().crew()
        result = crew_instance.kickoff(inputs=inputs)

    st.success("✅ Crew Execution Completed!")

    st.divider()

    st.markdown("## Task Outputs")
    
    # Full_result = ""
    for idx, task_output in enumerate(result.tasks_output):

        agent_name = task_output.agent
        output_text = task_output.raw

        with st.expander(f"🔹 Task {idx+1} — {agent_name}", expanded=True):
            st.markdown(output_text, unsafe_allow_html=True)
            
        st.session_state.Full_result += '\n\n'+output_text

        st.divider()

    st.markdown("## Final Combined Output")
    st.markdown(result.raw, unsafe_allow_html=True)

    st.download_button(
        label="📥 Download Blog Markdown",
        data=st.session_state.Full_result,
        file_name="blog_output.md",
        mime="text/markdown"
    )