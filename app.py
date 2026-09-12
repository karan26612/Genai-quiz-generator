import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="Environmental Quiz Generator", page_icon="🌍")
st.title("🌍 Generative AI Environmental Quiz Generator")

topic = st.selectbox("Choose a topic", [
    "Climate Change", "Air Pollution", "Water Pollution", "Biodiversity",
    "Waste Management", "Renewable Energy", "Deforestation", "Water Conservation"
])
num_q = st.slider("Number of questions", 3, 10, 5)
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.answers = {}
    st.session_state.submitted = False


def generate_quiz(topic, num_q, difficulty):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-flash-latest")
    prompt = f"""
    Generate {num_q} multiple-choice questions about {topic} in environmental science,
    at {difficulty} difficulty level.
    Return ONLY valid JSON (no markdown, no extra text) in exactly this format:
    [
      {{
        "question": "...",
        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "correct_answer": "A",
        "explanation": "..."
      }}
    ]
    """
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)


if st.button("Generate Quiz"):
    with st.spinner("Generating quiz..."):
        try:
            st.session_state.quiz = generate_quiz(topic, num_q, difficulty)
            st.session_state.answers = {}
            st.session_state.submitted = False
        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.quiz:
    st.subheader(f"Quiz: {topic} ({difficulty})")
    for i, q in enumerate(st.session_state.quiz):
        st.write(f"**Q{i+1}. {q['question']}**")
        st.session_state.answers[i] = st.radio(
            f"Select answer for Q{i+1}", q["options"], key=f"q{i}", index=None
        )

    if st.button("Submit Quiz"):
        st.session_state.submitted = True

    if st.session_state.submitted:
        score = 0
        for i, q in enumerate(st.session_state.quiz):
            selected = st.session_state.answers.get(i)
            correct_letter = q["correct_answer"]
            is_correct = selected and selected.startswith(correct_letter)
            if is_correct:
                score += 1
                st.success(f"Q{i+1}: Correct! {q['explanation']}")
            else:
                st.error(f"Q{i+1}: Incorrect. Correct answer: {correct_letter}. {q['explanation']}")
        st.subheader(f"Final Score: {score}/{len(st.session_state.quiz)}")
