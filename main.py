
import os
import smtplib
from pathlib import Path
from fastapi import APIRouter
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.models.modelsApi import (
    SendEmail,
)
load_dotenv()
router = APIRouter(prefix="/mail")
#bertrand.frottier@sanofi.com
# Configurez FastMail avec la connexion SMTP
conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("MAIL_FROM"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT")),
    MAIL_SERVER=os.environ.get("MAIL_SERVER"), 
    # MAIL_HOST=os.environ.get("MAIL_HOST") 
    MAIL_STARTTLS=False,  
    MAIL_SSL_TLS=True,   
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

@router.get("/all", response_model=str, tags=["mail"])
def get_mail():
    return "Hello World"
    


@router.post("/send_email_fastapi_mail", response_model=dict, tags=["mail"])
async def send_verification_email_(
    send: SendEmail,
) -> dict:

    template_path = Path(__file__).parent.parent / "template" / "index.html"
    message = MessageSchema(
        subject="FastApi-mail test",
        recipients=[send.email],
        body=None,
        html=template_path,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {
        "message": "The FastApi-mail has been sent successfully",
    }


@router.post("/send_email", response_model=dict, tags=["mail"])
async def send_verification_email(send: SendEmail) -> dict:
    template_path = Path(__file__).parent.parent / "template" / "index.html"

    with open(template_path, "r") as file:
        template_content = file.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'smtplib test by karim'

    html_part = MIMEText(template_content, 'html')
    msg.attach(html_part)

    s = smtplib.SMTP(host=os.environ.get("MAIL_HOST"))
    s.login(os.environ.get("MAIL_USERNAME"), os.environ.get("MAIL_PASSWORD"))
    s.sendmail(os.environ.get("MAIL_FROM"), send.email, msg.as_string())
    s.quit()

    return {"message": "The smtplib mail has been sent successfully"}
