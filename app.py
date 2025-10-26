# app.py
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, jsonify
)
from functools import wraps
import os
import sqlite3

# -------------------- Flask Config --------------------
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# -------------------- Database Init --------------------
DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------- Auth Helper --------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

# -------------------- MBTI Questions --------------------
QUESTIONS = [
    "I prefer spending time with a group rather than alone.",
    "I enjoy discussing abstract theories more than practical details.",
    "I make decisions based on logic rather than emotions.",
    "I like having a structured plan rather than being spontaneous.",
    "I recharge my energy by being around people.",
    "I focus on possibilities and the 'big picture' more than facts.",
    "I value fairness and rules over harmony in decision making.",
    "I prefer a to-do list and deadlines rather than going with the flow.",
    "I find it easy to talk to strangers.",
    "I often think about future possibilities rather than present realities.",
    "I prioritize efficiency over people's feelings.",
    "I feel more comfortable when my schedule is organized.",
    "I prefer group activities over solitary ones.",
    "I trust my imagination more than my senses.",
    "I believe rules and systems are more important than empathy.",
    "I prefer making plans to improvising."
]
NUM_Q = len(QUESTIONS)

DIM_MAP = {
    "IE": [0, 4, 8, 12],
    "NS": [1, 5, 9, 13],
    "TF": [2, 6, 10, 14],
    "JP": [3, 7, 11, 15],
}

# -------------------- MBTI Calculation --------------------
def calculate_mbti_from_answers(answers):
    if not answers or len(answers) != NUM_Q:
        raise ValueError(f"Incomplete answers ({len(answers)}/{NUM_Q})")

    a = [int(x) for x in answers]

    def score_dimension(idx_list):
        s = sum(a[i] for i in idx_list)
        max_s = 5 * len(idx_list)
        frac = s / max_s
        return round(frac * 100, 1)

    raw = {
        "I": score_dimension(DIM_MAP["IE"]),
        "N": score_dimension(DIM_MAP["NS"]),
        "T": score_dimension(DIM_MAP["TF"]),
        "J": score_dimension(DIM_MAP["JP"]),
    }

    scores = {
        "I": raw["I"], "E": 100 - raw["I"],
        "N": raw["N"], "S": 100 - raw["N"],
        "T": raw["T"], "F": 100 - raw["T"],
        "J": raw["J"], "P": 100 - raw["J"],
    }

    mbti = (
        ("I" if scores["I"] >= scores["E"] else "E") +
        ("N" if scores["N"] >= scores["S"] else "S") +
        ("T" if scores["T"] >= scores["F"] else "F") +
        ("J" if scores["J"] >= scores["P"] else "P")
    )

    print(f"✅ MBTI calculated: {mbti} {scores}")
    return mbti, scores


def predict_with_model(answers):
    # Skip model (use rule-based MBTI logic)
    return calculate_mbti_from_answers(answers)

# -------------------- Routes --------------------
@app.route("/")
def root():
    return render_template("home.html")

@app.route("/get_started")
def get_started():
    return render_template("get_started.html")

# ---------- Register ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            conn.close()
            return render_template("register.html", error="User already exists!")

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------- Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------- Home ----------
@app.route("/home")
@login_required
def home():
    return render_template("home.html")

# ---------- Questions ----------
@app.route("/questions")
@login_required
def questions():
    return render_template("questions.html", questions=QUESTIONS)

@app.route("/api/questions")
@login_required
def api_questions():
    return jsonify({"count": NUM_Q, "questions": QUESTIONS})

@app.route("/api/submit_answers", methods=["POST"])
@login_required
def submit_answers():
    data = request.get_json(silent=True) or {}
    answers = data.get("answers", [])
    print("DEBUG: Received answers:", answers)

    if not answers or len(answers) != NUM_Q:
        return jsonify({"ok": False, "error": "Incomplete or missing answers"}), 400

    try:
        mbti, scores = predict_with_model(answers)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    session["mbti_type"] = mbti
    session["mbti_scores"] = scores
    return jsonify({"ok": True, "type": mbti, "scores": scores})

# ---------- Result ----------
@app.route("/result")
@login_required
def result():
    if "mbti_type" not in session:
        return redirect(url_for("questions"))

    mbti_type = session["mbti_type"]
    scores = session["mbti_scores"]
    return render_template("result.html", mbti_type=mbti_type, scores=scores)

@app.route("/api/result")
@login_required
def api_result():
    if "mbti_type" not in session:
        return jsonify({"ok": False, "error": "No result yet"}), 400
    return jsonify({
        "ok": True,
        "type": session["mbti_type"],
        "scores": session["mbti_scores"]
    })

# ---------- Career ----------
@app.route("/career")
@login_required
def career():
    if "mbti_type" not in session:
        return redirect(url_for("questions"))
    return render_template("career.html")

@app.route("/api/career")
@login_required
def api_career():
    mbti = session.get("mbti_type", "INTJ")
    learning_styles = {
        "INTJ": "Independent, structured, and goal-oriented learning.",
        "ENFP": "Creative, interactive, and exploratory learning.",
        "ISTJ": "Clear instructions, checklists, and practice.",
        "ENTP": "Debate, experimentation, and open-ended projects."
    }
    careers = {
        "INTJ": ["Data Scientist", "Software Engineer", "Research Analyst", "Product Manager"],
        "ENFP": ["Marketing Specialist", "Teacher", "Entrepreneur", "Public Relations"],
        "ISTJ": ["Accountant", "Operations Manager", "Quality Engineer", "Civil Engineer"],
        "ENTP": ["Consultant", "Startup Founder", "UX Researcher", "Innovation Lead"]
    }
    return jsonify({
        "ok": True,
        "type": mbti,
        "learning": learning_styles.get(mbti, "Balanced, multimodal learning."),
        "careers": careers.get(mbti, ["Analyst", "Engineer", "Consultant"])
    })

# -------------------- Run --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
