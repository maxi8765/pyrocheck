import os
import smtplib
from email.message import EmailMessage

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TO_EMAIL = os.environ.get("TO_EMAIL", "robertmuir440@gmail.com")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")


@app.route("/")
def index():
    return "PyroCheck backend is running."


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "")
    address = request.form.get("address", "")
    phone = request.form.get("phone", "")
    email = request.form.get("email", "")
    purpose = request.form.get("purpose", "")
    photos = request.files.getlist("photos")

    msg = EmailMessage()
    msg["Subject"] = f"PyroCheck Burn Permit Application - {name}"
    msg["From"] = SMTP_USER or TO_EMAIL
    msg["To"] = TO_EMAIL
    msg.set_content(
        f"Name: {name}\n"
        f"Property Address: {address}\n"
        f"Phone: {phone}\n"
        f"Email: {email}\n"
        f"Purpose: {purpose}\n"
    )

    for photo in photos:
        if photo and photo.filename:
            data = photo.read()
            if data:
                msg.add_attachment(
                    data,
                    maintype="image",
                    subtype=photo.mimetype.split("/")[-1] or "jpeg",
                    filename=photo.filename,
                )

    if not SMTP_USER or not SMTP_PASS:
        return "Email not sent: SMTP_USER / SMTP_PASS not configured on server.", 500

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
