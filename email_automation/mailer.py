import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()
logger = get_logger("email_automation")

class EmailAutomation:
    def __init__(self):
        self.host = os.getenv("SMTP_HOST", "")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME", "")
        self.password = os.getenv("SMTP_PASSWORD", "")
        self.use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in {"1","true","yes"}

    def render_template(self, template_path, **values):
        template = Path(template_path).read_text(encoding="utf-8")
        return template.format(**values)

    def send(self, sender, recipients, subject, body_html, dry_run=True):
        recipients = [recipients] if isinstance(recipients, str) else list(recipients)
        if dry_run:
            logger.info("DRY RUN email: sender=%s recipients=%s subject=%s",
                        sender, recipients, subject)
            return {"sent": False, "dry_run": True, "recipients": recipients}

        if not self.host or not self.username:
            raise RuntimeError("SMTP configuration is incomplete")

        msg = EmailMessage()
        msg["From"] = sender or self.username
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.set_content("This message contains HTML content.")
        msg.add_alternative(body_html, subtype="html")

        with smtplib.SMTP(self.host, self.port, timeout=30) as smtp:
            if self.use_tls:
                smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(msg)

        logger.info("Email sent to %s", recipients)
        return {"sent": True, "dry_run": False, "recipients": recipients}
