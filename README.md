# 🧪 AI Prompt Testing Dashboard

> Compare, annotate and label LLM prompt outputs side by side

A full-stack AI tool for prompt engineering and data annotation.
Enter two prompts, get AI outputs side by side, label which performed
better and save results to database.

---

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/1_dashboard.png)

### Side by Side Comparison
![Comparison](screenshots/2_comparison.png)

### Annotation
![Annotation](screenshots/3_annotation.png)

### History
![History](screenshots/4_history.png)

---

## ✨ Features

- 🔀 Side-by-side prompt comparison
- 🤖 Powered by Groq LLaMA 3.1 API
- 🏷️ Annotate and label prompt outputs
- 📝 Add notes for each test
- 📋 View full test history
- 💾 Results saved to SQLite database

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, CSS |
| Backend | Python, Flask, Flask-CORS |
| AI | Groq API — LLaMA 3.1 8B Instant |
| Database | SQLite |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Anusha-Thotakura/prompt-dashboard.git
cd prompt-dashboard
```

### 2. Backend Setup
```bash
cd backend
pip install flask flask-cors requests python-dotenv
cp .env.example .env
# Add your GROQ_API_KEY to .env
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

App runs at `http://localhost:3000` 🚀

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/test-prompts` | Test two prompts against Groq AI |
| POST | `/save-result` | Save annotation to database |
| GET | `/history` | Load all saved test results |

---

## 👩‍💻 Author
**T. Anusha** — B.Tech CSE, Batch of 2026

## 📜 License
MIT