import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Reverse Career Planner",
    page_icon="🚀",
    layout="wide"
)

# DEBUG - REMOVE LATER
st.write("API Key loaded:", api_key[:10] if api_key else "NOT FOUND")

st.title("🚀 Reverse Career Planner")

st.write(
    "Tell us your dream career and we'll generate a roadmap to achieve it."
)

career = st.text_input(
    "Desired Career",
    placeholder="Data Scientist"
)

years = st.slider(
    "Time to Achieve Goal (Years)",
    1,
    10,
    3
)

skills = st.text_area(
    "Current Skills",
    placeholder="Python, HTML, Communication"
)

if st.button("Generate Roadmap"):

    if not api_key:
        st.error("Please add your GEMINI_API_KEY in the .env file")

    else:
        try:
            client = genai.Client(api_key=api_key)

            prompt = f"""
            Act as an expert career mentor.

            Desired Career:
            {career}

            Time Available:
            {years} years

            Current Skills:
            {skills}

            Generate:

            1. Career Overview

            2. Required Skills

            3. Skill Gap Analysis

            4. Year-wise Roadmap

            5. Projects to Build

            6. Certifications

            7. Interview Preparation Strategy

            8. Salary Expectations

            9. Final Tips

            Make it detailed and beginner friendly.
            """

            with st.spinner("Creating your roadmap..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

                st.success("Roadmap Generated!")

                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {e}")