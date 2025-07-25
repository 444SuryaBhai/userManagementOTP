import aiosmtplib
from email.message import EmailMessage
from app.config.config import get_settings

settings = get_settings()

async def send_email_async(to: str, subject: str, body: str, html: str = None, attachments=None):
    msg = EmailMessage()
    msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
    msg["To"] = to
    msg["Subject"] = subject
    if html:
        msg.add_alternative(html, subtype="html")
    else:
        msg.set_content(body)
    if attachments:
        for att in attachments:
            msg.add_attachment(att["content"], maintype=att["maintype"], subtype=att["subtype"], filename=att["filename"])
    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    ) 