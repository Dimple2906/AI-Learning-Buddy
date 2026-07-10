import streamlit as st
from google import genai

# Page settings
st.set_page_config(
    page_title="Learn with Dimple: AI Learning Buddy",
    page_icon="🎓"
)

st.title("🎓Learn with Dimple: AI Learning Buddy")
st.write("Learn any topic with simple explanations, examples and quizzes.")

# Get API Key from Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Properly initialize the current client
client = genai.Client(api_key=api_key)

# User Input
topic = st.text_input("Enter a Topic")

option = st.selectbox(
    "Choose Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Ask Anything"
    ]
)

if st.button("Generate"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    else:
        if option == "Explain Concept":
            prompt = f"""
You are Dimple, a friendly AI tutor.

Explain {topic} in simple language for beginners.
Use easy words and one real-life analogy.
"""

        elif option == "Real-Life Example":
            prompt = f"""
Give one clear real-life example of {topic}.
Explain it in simple beginner-friendly language.
"""

        elif option == "Generate Quiz":
            prompt = f"""
Create 5 MCQ questions about {topic}.

Each question should have:
A)
B)
C)
D)

Give the correct answer and explanation.
"""

        else:
            prompt = topic

        try:
            # Using the active, supported standard model
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            st.success("Generated Successfully!")
            st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
