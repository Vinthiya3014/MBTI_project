document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".btn");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      console.log(`➡️ Navigating to: ${btn.textContent.trim()}`);
    });
  });

  console.log("✅ Get Started page loaded successfully!");
});
