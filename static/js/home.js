document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".links a");

  links.forEach(link => {
    link.addEventListener("mouseover", () => {
      link.style.transform = "scale(1.05)";
    });
    link.addEventListener("mouseout", () => {
      link.style.transform = "scale(1)";
    });
  });

  console.log("✅ Home page loaded and interactive!");
});
