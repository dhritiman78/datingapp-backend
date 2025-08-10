import smtplib
from email.message import EmailMessage

sender = "planit.team.224@gmail.com"
password = "lfcz szsi mfhk ohyt"  # App Password from Gmail (keep safe!)

def send_email(to: str, subject: str, html_body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    msg.set_content("This email requires HTML support.")
    msg.add_alternative(html_body, subtype='html')

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

def send_registration_confirmation(receiver: str):
    subject = "🎉 Welcome to TU Dating App – Registration Successful!"
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 30px;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 25px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h2 style="color: #d63384; text-align: center;">Welcome to TU Dating App! ❤️</h2>
            <p>Hi there,</p>
            <p>Thank you for registering with <strong>TU Dating App</strong>. We're excited to help you find amazing connections within our campus community.</p>
            <div style="background-color: #fce8f1; padding: 15px; border-radius: 5px; margin-top: 15px; font-size: 16px;">
                <strong>Status:</strong> Your profile is <span style="color: #ff4081;">under verification</span>.<br>
                You will be notified by email once it is successfully verified.
            </div>
            <p style="margin-top: 20px;">In the meantime, stay excited! We’re working behind the scenes to ensure everyone’s safety and a great experience.</p>
            <p style="color: #555;">With love,<br><strong>Team TU Dating App 💖</strong></p>
        </div>
    </body>
    </html>
    """

    send_email(receiver, subject, html_body)