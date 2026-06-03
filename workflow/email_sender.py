import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

#  Send email tool 
@tool
def send_email(
    receiver_email:str,
    video_path:str,
    caption:str
)->str:
    """Send edited video to user email."""

    sender_email = os.getenv(
        "SENDER_EMAIL"
    )

    sender_password = os.getenv(
        "APP_PASSWORD"
    )

    msg = EmailMessage()

    msg["Subject"] = "Your Edited Video"

    msg["From"] = sender_email

    msg["To"] = receiver_email

    msg.set_content(
f"""
Hello,

Your edited video is ready.

Generated Caption:
--------------------------

{caption}

Please find the edited video attached.

Thanks,
AI Video Assistant
"""
)

    print(video_path)
    print(os.path.exists(video_path))

    with open(
        video_path,
        "rb"
    ) as f:

        video_data = f.read()

    filename = os.path.basename(
        video_path
    )

    msg.add_attachment(
        video_data,
        maintype="video",
        subtype="mp4",
        filename=filename
    )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(msg)

    return "Email Sent Successfully."


VIDEO_PATH = os.path.join(
    BASE_DIR,
    "temp_videos",
    "video.mp4"
)
