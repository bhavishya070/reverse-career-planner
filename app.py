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

# Language Selection
language = st.selectbox(
    "🌐 Select Language",
    ["English", "Hindi", "Telugu"]
)

translations = {
    "English": {
        "title": "🚀 Reverse Career Planner",
        "subtitle": "Plan your dream career with AI-generated personalized roadmaps.",
        "career": "Desired Career",
        "skills": "Current Skills",
        "years": "Time to Achieve Goal (Years)",
        "button": "Generate Roadmap",
        "provider": "🤖 Choose AI Provider",
        "apikey": "🔑 Gemini API Key (Optional - BYOK)",
        "success": "Roadmap Generated Successfully!",
        "warning": "Please enter a desired career."
    },

    "Hindi": {
        "title": "🚀 रिवर्स करियर प्लानर",
        "subtitle": "एआई द्वारा तैयार व्यक्तिगत करियर रोडमैप प्राप्त करें।",
        "career": "वांछित करियर",
        "skills": "वर्तमान कौशल",
        "years": "लक्ष्य प्राप्त करने का समय (वर्ष)",
        "button": "रोडमैप बनाएं",
        "provider": "🤖 एआई प्रदाता चुनें",
        "apikey": "🔑 Gemini API कुंजी (वैकल्पिक - BYOK)",
        "success": "रोडमैप सफलतापूर्वक तैयार किया गया!",
        "warning": "कृपया वांछित करियर दर्ज करें।"
    },

    "Telugu": {
        "title": "🚀 రివర్స్ కెరీర్ ప్లానర్",
        "subtitle": "AI ఆధారిత వ్యక్తిగత కెరీర్ రోడ్‌మ్యాప్‌ను పొందండి.",
        "career": "కావలసిన కెరీర్",
        "skills": "ప్రస్తుత నైపుణ్యాలు",
        "years": "లక్ష్యాన్ని చేరుకునే సమయం (సంవత్సరాలు)",
        "button": "రోడ్‌మ్యాప్ రూపొందించు",
        "provider": "🤖 AI ప్రొవైడర్‌ను ఎంచుకోండి",
        "apikey": "🔑 Gemini API కీ (ఐచ్ఛికం - BYOK)",
        "success": "రోడ్‌మ్యాప్ విజయవంతంగా రూపొందించబడింది!",
        "warning": "దయచేసి మీ కెరీర్ లక్ష్యాన్ని నమోదు చేయండి."
    }
}

t = translations[language]

st.title(t["title"])
st.write(t["subtitle"])

provider = st.radio(
    t["provider"],
    ["Gemini API", "Ollama (Local AI)"]
)

user_api_key = st.text_input(
    t["apikey"],
    type="password"
)

api_key = user_api_key if user_api_key else os.getenv("GEMINI_API_KEY")

career = st.text_input(
    t["career"],
    placeholder="Data Scientist"
)

years = st.slider(
    t["years"],
    1,
    10,
    3
)

skills = st.text_area(
    t["skills"],
    placeholder="Python, HTML, Communication"
)

if st.button(t["button"]):

    if not career:
        st.warning(t["warning"])
        st.stop()

    prompt = f"""
You are an expert career mentor.

IMPORTANT:
Generate the COMPLETE roadmap in {language}.

Use ONLY {language} language.

Do not switch to English unless English is selected.

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

Make the roadmap detailed and beginner friendly.
"""

    try:

        with st.spinner("Generating your roadmap..."):

            answer = None

            if provider == "Gemini API":

                if not api_key:
                    st.error("Please provide a Gemini API key.")
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

            else:

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=300
                )

                answer = response.json()["response"]

            if answer:

                st.success(t["success"])

                st.write(f"🌐 Language: {language}")
                st.write(f"🤖 AI Provider: {provider}")

                st.markdown(answer)

            else:

                st.warning("AI service is currently busy.")

    except Exception as e:

        st.error(f"Error: {e}")
