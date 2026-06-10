import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Reverse Career Planner",
    page_icon="🚀",
    layout="wide"
)

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
        st.error("API key not found. Please configure GEMINI_API_KEY.")

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

                success = False

                for _ in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt,
                        )

                        st.success("Roadmap Generated!")
                        st.markdown(response.text)

                        success = True
                        break

                    except Exception:
                        time.sleep(5)

                if not success:
                    st.warning(
                        "The AI service is currently busy. Showing a sample roadmap."
                    )

                    st.markdown(f"""
# {career} Career Roadmap

## Required Skills
- Python
- Data Structures & Algorithms
- Object-Oriented Programming
- Database Management Systems
- Git & GitHub

## Skill Gap Analysis
Focus on strengthening technical fundamentals and building practical projects.

## Year 1
- Learn core programming concepts
- Build beginner projects
- Improve problem-solving skills

## Year 2
- Work on advanced projects
- Earn relevant certifications
- Participate in internships

## Year 3
- Prepare for interviews
- Build a strong resume
- Apply for jobs and internships

## Recommended Projects
- Portfolio Website
- Task Management App
- AI Career Assistant
- Data Analysis Dashboard

## Certifications
- Python Programming
- Data Structures & Algorithms
- Cloud Fundamentals

## Interview Preparation
- Practice coding questions
- Mock interviews
- Resume optimization

## Final Tips
Stay consistent, build projects regularly, and keep learning new technologies.
""")

        except Exception:
            st.error(
                "The AI service is temporarily unavailable. Please try again later."
            )
