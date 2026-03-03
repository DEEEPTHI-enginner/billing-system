import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_invoice_email(to_email: str, invoice):
    try:
        subject = f"Invoice #{invoice.id} - Billing System"

        body = f"""
Hello,

Thank you for your purchase.

Invoice ID: {invoice.id}
Total Amount: {invoice.total_amount}
Total Tax: {invoice.total_tax}
Grand Total: {invoice.grand_total}
Paid Amount: {invoice.paid_amount}
Balance Given: {invoice.balance_amount}

Regards,
Billing System
        """

        msg = MIMEMultipart()
        msg["From"] = EMAIL_USERNAME
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, to_email, msg.as_string())
        server.quit()

        print("Invoice email sent successfully!")

    except Exception as e:
        print("Email sending failed:", str(e))
