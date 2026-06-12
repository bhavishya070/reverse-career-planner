import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time
import requests

load_dotenv()

st.set_page_config(
    page_title="Reverse Career Planner",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Reverse Career Planner")

st.write(
    "Plan your dream career with AI-generated personalized roadmaps."
)

# Language Selection
language = st.selectbox(
    "🌐 Select Language",
    ["English", "Hindi", "Telugu"]
)

# AI Provider Selection
provider = st.radio(
    "🤖 Choose AI Provider",
    ["Gemini API", "Ollama (Local AI)"]
)

# BYOK
user_api_key = st.text_input(
    "🔑 Gemini API Key (Optional - BYOK)",
    type="password"
)

api_key = user_api_key if user_api_key else os.getenv("GEMINI_API_KEY")

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

    if not career:
        st.warning("Please enter a desired career.")
        st.stop()

    prompt = f"""
You are an expert career mentor.

IMPORTANT:
Generate the COMPLETE response in {language} language only.

Do NOT use English unless English is selected.

All headings, explanations, roadmap steps, certifications,
projects, salary expectations and tips must be in {language}.

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

    try:

        with st.spinner("Generating your roadmap..."):

            answer = None

            # GEMINI
            if provider == "Gemini API":

                if not api_key:
                    st.error(
                        "Please provide a Gemini API key or configure GEMINI_API_KEY."
                    )
                    st.stop()

                client = genai.Client(api_key=api_key)

                for _ in range(3):

                    try:

                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt,
                        )

                        answer = response.text
                        break

                    except Exception:
                        time.sleep(5)

            # OLLAMA
            else:

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False
                    }
                )

                answer = response.json()["response"]

            if answer:

                st.success("Roadmap Generated Successfully!")

                st.write(f"🌐 Language: {language}")
                st.write(f"🤖 AI Provider: {provider}")

                st.markdown(answer)

            else:

                st.warning(
                    "AI service is busy. Showing sample roadmap."
                )

                st.markdown(f"""
# {career}

## Career Overview
A promising career path with strong growth opportunities.

## Required Skills
- Python
- DSA
- DBMS
- OOP
- Git & GitHub

## Year 1
Learn fundamentals and build beginner projects.

## Year 2
Advanced projects, certifications and internships.

## Year 3
Interview preparation and job applications.

## Final Tips
Stay consistent and keep building real-world projects.
""")

    except Exception as e:

        st.error(f"Error: {e}")
