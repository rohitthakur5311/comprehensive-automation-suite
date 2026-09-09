from datetime import datetime
from .mailer import EmailAutomation

class Campaign:
    def __init__(self, mailer=None):
        self.mailer = mailer or EmailAutomation()

    def run(self, sender, recipients, subject, template_path, values=None, dry_run=True):
        values = values or {"name": "there", "message": "Automated message"}
        body = self.mailer.render_template(template_path, **values)
        return self.mailer.send(sender, recipients, subject, body, dry_run=dry_run)

    @staticmethod
    def stats(sent, recipients, opens=0, clicks=0):
        recipient_count = max(len(recipients), 1)
        return {
            "emails_sent": sent,
            "recipients": len(recipients),
            "open_rate_percent": round(opens / recipient_count * 100, 2),
            "click_rate_percent": round(clicks / recipient_count * 100, 2),
            "generated_at": datetime.now().isoformat(timespec="seconds")
        }
