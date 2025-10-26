document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", (e) => {
    const username = form.querySelector("input[name='username']").value.trim();
    const password = form.querySelector("input[name='password']").value.trim();

    if (username.length < 3) {
      e.preventDefault();
      alert("⚠️ Username must be at least 3 characters long!");
      return;
    }

    if (password.length < 5) {
      e.preventDefault();
      alert("⚠️ Password must be at least 5 characters long!");
      return;
    }
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const passwordInput = document.querySelector("input[name='password']");
  const strengthMessage = document.createElement("div");
  strengthMessage.id = "strengthMessage";
  passwordInput.insertAdjacentElement("afterend", strengthMessage);

  passwordInput.addEventListener("input", () => {
    const val = passwordInput.value;
    let strength = "Weak";
    let color = "red";

    // Check strength
    if (val.length >= 8 && /[A-Z]/.test(val) && /[0-9]/.test(val) && /[^A-Za-z0-9]/.test(val)) {
      strength = "Strong";
      color = "green";
    } else if (val.length >= 6 && (/[A-Z]/.test(val) || /[0-9]/.test(val))) {
      strength = "Medium";
      color = "orange";
    }

    strengthMessage.textContent = `Password Strength: ${strength}`;
    strengthMessage.style.color = color;
  });
});
