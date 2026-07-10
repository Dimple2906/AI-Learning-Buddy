import os
import streamlit as st
from google import genai

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Learning Buddy - Dimple",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Learn with Dimple - AI Learning Buddy")
st.write(
    "Your friendly AI tutor that explains concepts, gives examples, "
    "creates quizzes, and provides feedback."
)

# -----------------------------
# Gemini API Key
# -----------------------------
api_key = None

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API Key not found.")
    st.info("Add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# New Gemini Client
client = genai.Client(api_key=api_key)

# -----------------------------
# User Input
# -----------------------------
topic = st.text_input("📚 Enter a Topic")

activity = st.selectbox(
    "Choose an Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Evaluate Answer",
        "Ask Anything"
    ]
)

question = ""
student_answer = ""

if activity == "Evaluate Answer":
    question = st.text_area("Enter the Question")
    student_answer = st.text_area("Enter Student Answer")


# -----------------------------
# Generate Response
# -----------------------------
if st.button("Generate"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
        st.stop()

    # Create Prompt
    if activity == "Explain Concept":

        prompt = f"""
You are Dimple, a friendly AI tutor.

Explain {topic} in simple language for beginners.

Use:
- Easy words
- One real-life analogy
- Short and clear explanation
"""

    elif activity == "Real-Life Example":

        prompt = f"""
You are Dimple.

Give one clear real-life example of {topic}.
Explain it in simple beginner-friendly language.
"""

    elif activity == "Generate Quiz":

        prompt = f"""
You are Dimple, an encouraging tutor.

Create 5 multiple-choice questions about {topic}.

Each question must have:
A)
B)
C)
D)

After each question provide:
- Correct Answer
- Short Explanation
"""

    elif activity == "Evaluate Answer":

        prompt = f"""
You are Dimple, a supportive tutor.

Topic:
{topic}

Question:
{question}

Student Answer:
{student_answer}

Give encouraging feedback.

If the answer is wrong:
- Explain the mistake
- Provide the correct answer
- Explain simply
"""

    else:

        prompt = f"""
Answer this question about {topic}
in a simple beginner-friendly way.
"""


    try:

        with st.spinner("Dimple is thinking..."):

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

        st.success("Response Generated Successfully!")

        st.markdown(response.text)

    except Exception as e:

        st.error(f"Error: {e}")
