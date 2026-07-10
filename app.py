import os
import streamlit as st
import google.generativeai as genai

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Learning Buddy - Dimple",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Learning Buddy - Dimple")
st.write("Learn any topic with simple explanations, real-life examples, quizzes, and feedback.")

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

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

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

student_answer = ""
question = ""

if activity == "Evaluate Answer":
    question = st.text_area("Enter the Question")
    student_answer = st.text_area("Enter Student's Answer")

# -----------------------------
# Generate Button
# -----------------------------
if st.button("Generate"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
        st.stop()

    if activity == "Explain Concept":

        prompt = f"""
You are Dimple, a friendly AI tutor.

Explain {topic} in simple language for a beginner.

Use:
- Easy words
- One real-life analogy
- Short explanation
"""

    elif activity == "Real-Life Example":

        prompt = f"""
You are Dimple.

Give one real-life example of {topic}.

Explain it in beginner-friendly language.
"""

    elif activity == "Generate Quiz":

        prompt = f"""
You are Dimple.

Create 5 multiple-choice questions on {topic}.

Each question must contain:

A)

B)

C)

D)

After each question provide:

Correct Answer

Short Explanation
"""

    elif activity == "Evaluate Answer":

        prompt = f"""
You are Dimple.

Topic:
{topic}

Question:
{question}

Student Answer:
{student_answer}

Give encouraging feedback.

If the answer is wrong:

• Explain why.

• Give the correct answer.

• Explain in simple language.
"""

    else:

        prompt = topic

    try:

        with st.spinner("Generating..."):

            response = model.generate_content(prompt)

        st.success("Done!")

        st.write(response.text)

    except Exception as e:

        st.error(f"Error: {e}")
