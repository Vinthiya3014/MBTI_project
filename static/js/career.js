document.addEventListener("DOMContentLoaded", async function () {
  try {
    const res = await fetch("/api/career");
    const data = await res.json();

    if (data.ok) {
      document.getElementById("learning-style").textContent = data.learning;

      let list = document.getElementById("career-list");
      data.careers.forEach(career => {
        let li = document.createElement("li");
        li.textContent = career;
        list.appendChild(li);
      });
    } else {
      document.getElementById("learning-style").textContent = "Error loading recommendations.";
    }
  } catch (err) {
    console.error("Error:", err);
    document.getElementById("learning-style").textContent = "Error connecting to server.";
  }
});
