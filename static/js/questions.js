let questions = [];
let current = 0;
let answers = [];

// Load questions dynamically from backend
async function loadAll() {
  try {
    const r = await fetch("/api/questions");
    const data = await r.json();
    questions = data.questions;

    if (questions.length === 0) {
      document.getElementById("question").innerText = "No questions available.";
      return;
    }

    document.getElementById("question").innerText = questions[current];
  } catch (err) {
    console.error("Error loading questions:", err);
    document.getElementById("question").innerText = "Failed to load questions.";
  }
}

// Handle next button click
function nextQuestion() {
  const sel = document.querySelector("input[name='answer']:checked");
  if (!sel) return alert("Please select an answer!");

  answers.push(parseInt(sel.value));
  sel.checked = false;
  current++;

  if (current < questions.length) {
    document.getElementById("question").innerText = questions[current];
  } else {
    // Send answers to backend
    fetch("/api/submit_answers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers })
    }).then(() => location.href = "/result");
  }
}

window.onload = loadAll;
