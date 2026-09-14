# 🌿 EcoSpark — GenAI Quiz Generator

EcoSpark is a Streamlit web app that generates fresh, AI-powered multiple-choice quizzes on environmental science topics using Google's Gemini API. Pick a topic, set the difficulty and number of questions, and get an instant quiz with explanations and a final score.

## Features

- **AI-generated questions** — Uses Google Gemini to generate varied, non-repetitive multiple-choice questions (facts, causes, effects, solutions, statistics, real-world examples).
- **8 environmental topics** — Climate Change, Air Pollution, Water Pollution, Biodiversity, Waste Management, Renewable Energy, Deforestation, and Water Conservation.
- **Adjustable difficulty & length** — Choose Easy, Medium, or Hard, and 3–20 questions per quiz.
- **No repeat questions** — Tracks previously generated questions in the session and asks Gemini to avoid repeating or closely rephrasing them.
- **Instant grading** — Submit your answers to see per-question feedback (correct/incorrect with explanations) and a final score.
- **Clean, custom UI** — A dark, nature-themed interface built with Streamlit and custom CSS.

## Demo

> Add a screenshot or GIF of the app here once you have one, e.g.:
>
> `![EcoSpark demo](docs/demo.png)`

## Tech Stack

- [Streamlit](https://streamlit.io/) — web app framework
- [google-generativeai](https://pypi.org/project/google-generativeai/) — Gemini API SDK
- Python 3.9+

## Getting Started

### Prerequisites

- Python 3.9 or later
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/karan26612/Genai-quiz-generator.git
   cd Genai-quiz-generator
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

The app reads your Gemini API key from Streamlit secrets. Create a `.streamlit/secrets.toml` file in the project root:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

> ⚠️ **Never commit `secrets.toml` to version control.** Add it to your `.gitignore`.

### Running the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## How It Works

1. You select a topic, difficulty, and number of questions.
2. The app builds a prompt (including a list of previously used questions to avoid repeats) and sends it to the Gemini `gemini-3.1-flash-lite` model.
3. Gemini returns the quiz as structured JSON: question text, four options, the correct answer, and an explanation.
4. Streamlit renders the quiz, collects your answers, and grades them on submit — showing explanations and a final score.

## Project Structure

```
Genai-quiz-generator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md            # Project documentation
```

## Deployment

This app can be deployed for free on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push this repo to your own GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app pointing at `app.py`.
3. In the app's **Settings → Secrets**, add:

   ```toml
   GEMINI_API_KEY = "your-gemini-api-key-here"
   ```

4. Deploy — Streamlit Cloud installs `requirements.txt` automatically.

## Roadmap / Ideas

- [ ] Add more subject areas beyond environmental science
- [ ] Export quiz results as PDF/CSV
- [ ] Add a leaderboard or quiz history
- [ ] Support for timed quizzes
- [ ] Unit tests for quiz generation/parsing logic

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

No license has been specified yet. Consider adding one (e.g., [MIT](https://choosealicense.com/licenses/mit/)) so others know how they can use this project.

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini](https://ai.google.dev/)
