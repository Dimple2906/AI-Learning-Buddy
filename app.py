import os
import streamlit as st
from google import genai

# ---------------------------
# Streamlit Page Configuration
# ---------------------------
st.set_page_config(
    page_title="AI Learning Buddy - Dimple",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Learning Buddy - Dimple")
st.write("Learn any topic with simple explanations, examples, quizzes, and AI guidance.")

# ---------------------------
# Get Gemini API Key
# ---------------------------
api_key = None

# First try Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key not found. Please add it in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------------------
# User Input
# ---------------------------
topic = st.text_input("📚 Enter a Topic")

option = st.selectbox(
    "Choose an Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Ask Anything"
    ]
)

# ---------------------------
# Generate Button
# ---------------------------
if st.button("Generate"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:

        if option == "Explain Concept":
            prompt = f"""
            Explain {topic} in simple language for a beginner.
            Use easy words and one real-life analogy.
            """

        elif option == "Real-Life Example":
            prompt = f"""
            Give one clear real-life example of {topic}.
            Explain it in simple language.
            """

        elif option == "Generate Quiz":
            prompt = f"""
            Create 5 multiple-choice questions on {topic}.
            Each question should have 4 options (A, B, C, D).
            After each question, provide the correct answer and a short explanation.
            """

        else:
            prompt = topic

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.success("Response Generated Successfully!")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
