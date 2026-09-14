import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="EcoSpark", page_icon="🌿", layout="centered")

# ---------- Visual theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

h1, h2, h3 { font-family: 'Fraunces', serif !important; }

.terra-hero {
    padding: 1.75rem 2rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #16241A 0%, #1E3324 100%);
    border: 1px solid #2C4A34;
    margin-bottom: 1.5rem;
}
.terra-hero h1 {
    color: #F0EDE4;
    font-size: 3rem;
    margin: 0 0 0.4rem 0;
    line-height: 1.15;
}
.terra-hero p {
    color: #9FB8A6;
    font-size: 1.15rem;
    margin: 0;
}

[data-testid="stSelectbox"] label, [data-testid="stSlider"] label {
    color: #C9D9CD !important;
    font-weight: 500;
    font-size: 0.9rem;
}

[data-testid="stButton"] button {
    background-color: #3A7D44;
    color: #F0EDE4;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.4rem;
    font-weight: 600;
    transition: background-color 0.15s ease;
}
[data-testid="stButton"] button:hover {
    background-color: #4E9457;
    color: #F0EDE4;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    border: 1px solid #2C4A34 !important;
    background-color: #16241A;
}

.q-number {
    display: inline-block;
    background-color: #3A7D44;
    color: #F0EDE4;
    font-weight: 600;
    font-size: 0.8rem;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    margin-bottom: 0.5rem;
}

.score-banner {
    text-align: center;
    padding: 1.5rem;
    border-radius: 14px;
    background: linear-gradient(135deg, #1E3324 0%, #2C4A34 100%);
    border: 1px solid #3A7D44;
    margin-top: 1rem;
}
.score-banner h2 {
    color: #F0EDE4;
    margin: 0;
    font-size: 1.8rem;
}
.score-banner p {
    color: #9FB8A6;
    margin: 0.3rem 0 0 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="terra-hero">
    <h1>🌿 EcoSpark</h1>
    <p>Test your environmental science knowledge with a fresh quiz every time.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Settings card ----------
with st.container(border=True):
    topic = st.selectbox("Topic", [
        "Climate Change", "Air Pollution", "Water Pollution", "Biodiversity",
        "Waste Management", "Renewable Energy", "Deforestation", "Water Conservation"
    ])
    col1, col2 = st.columns(2)
    with col1:
        num_q = st.slider("Number of questions", 3, 20, 5)
    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    generate_clicked = st.button("Generate Quiz", use_container_width=True)

if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.used_questions = []


def generate_quiz(topic, num_q, difficulty, avoid_list):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        "gemini-3.1-flash-lite",
        generation_config={"temperature": 1.0}
    )
    avoid_text = ""
    if avoid_list:
        avoid_text = (
            "Do NOT repeat or closely rephrase any of these previously used questions:\n"
            + "\n".join(f"- {q}" for q in avoid_list[-30:])
        )
    prompt = f"""
    Generate {num_q} multiple-choice questions about {topic} in environmental science,
    at {difficulty} difficulty level. Make them varied in angle (facts, causes, effects,
    solutions, statistics, real-world examples) rather than the most obvious textbook question.
    {avoid_text}
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


if generate_clicked:
    with st.spinner("Generating quiz..."):
        try:
            st.session_state.quiz = generate_quiz(
                topic, num_q, difficulty, st.session_state.used_questions
            )
            st.session_state.used_questions.extend(
                q["question"] for q in st.session_state.quiz
            )
            st.session_state.answers = {}
            st.session_state.submitted = False
        except Exception as e:
            st.error(f"Error: {e}")

# ---------- Quiz ----------
if st.session_state.quiz:
    st.markdown(f"### {topic} · {difficulty}")
    for i, q in enumerate(st.session_state.quiz):
        with st.container(border=True):
            st.markdown(f'<span class="q-number">Question {i+1}</span>', unsafe_allow_html=True)
            st.markdown(f"**{q['question']}**")
            st.session_state.answers[i] = st.radio(
                f"answer_{i}", q["options"], key=f"q{i}", index=None,
                label_visibility="collapsed"
            )

    if st.button("Submit Quiz", use_container_width=True):
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

        st.markdown(f"""
        <div class="score-banner">
            <h2>{score} / {len(st.session_state.quiz)}</h2>
            <p>Final score</p>
        </div>
        """, unsafe_allow_html=True)
