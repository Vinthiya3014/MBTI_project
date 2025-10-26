function loginUser(event) {
  event.preventDefault();
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  // TODO: Add backend API for real authentication
  if (username && password) {
    localStorage.setItem("username", username);
    window.location.href = "questions.html";
  } else {
    alert("Invalid login details!");
  }
}
