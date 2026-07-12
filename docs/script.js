// Set this to wherever the Flask backend (app.py) is deployed, e.g. Render/Railway URL.
const BACKEND_URL = "https://YOUR-BACKEND-URL.example.com/submit";

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js");
  });
}

const form = document.getElementById("burnForm");
const status = document.getElementById("status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  status.textContent = "Sending...";
  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      body: new FormData(form),
    });
    if (!response.ok) throw new Error("Server error");
    status.textContent = "Application emailed. Thank you.";
    form.reset();
  } catch (err) {
    status.textContent = "Could not send the application. Please try again.";
  }
});
