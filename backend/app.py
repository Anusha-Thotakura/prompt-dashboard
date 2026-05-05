import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)

# ── Paste your Groq API key directly here temporarily ──
GROQ_API_KEY = "your_actual_groq_key_here"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ── Database setup ──────────────────────────────
def init_db():
    conn = sqlite3.connect("prompts.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_a TEXT,
            prompt_b TEXT,
            output_a TEXT,
            output_b TEXT,
            label TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ── Call Groq API ────────────────────────────────
def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }
    try:
        response = requests.post(GROQ_URL, json=body, headers=headers)
        data = response.json()
        print("Groq response status:", response.status_code)
        print("Groq response data:", data)

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"API Error: {data['error']['message']}"
        else:
            return f"Unexpected response: {str(data)}"
    except Exception as e:
        return f"Request failed: {str(e)}"

# ── Routes ───────────────────────────────────────
@app.route("/test-prompts", methods=["POST"])
def test_prompts():
    data = request.json
    prompt_a = data.get("prompt_a", "")
    prompt_b = data.get("prompt_b", "")
    output_a = call_groq(prompt_a)
    output_b = call_groq(prompt_b)
    return jsonify({
        "output_a": output_a,
        "output_b": output_b
    })

@app.route("/save-result", methods=["POST"])
def save_result():
    data = request.json
    conn = sqlite3.connect("prompts.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO tests (prompt_a, prompt_b, output_a, output_b, label, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["prompt_a"], data["prompt_b"],
        data["output_a"], data["output_b"],
        data["label"], data.get("notes", "")
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Saved successfully"})

@app.route("/history", methods=["GET"])
def history():
    conn = sqlite3.connect("prompts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tests ORDER BY created_at DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "prompt_a": row[1],
            "prompt_b": row[2],
            "output_a": row[3],
            "output_b": row[4],
            "label": row[5],
            "notes": row[6],
            "created_at": row[7]
        })
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)