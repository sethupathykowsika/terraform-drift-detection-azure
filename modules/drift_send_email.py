import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# SMTP server details
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "awsraam@gmail.com"
# os.getenv("SMTP_USERNAME")  # Retrieve from environment variables
smtp_password = "ccxdjqxgupmaxqkc"
# os.getenv("SMTP_PASSWORD")  # Retrieve from environment variables

# Email details
sender_email = "awsraam@gmail.com"  # To Be Updated
receiver_email = ["awsraam@gmail.com","hariraam@cloudiq.io"]  # To Be Updated
subject = "Terraform Drift Report for Dev Infra"  # To Be Updated
drift_report_file = os.path.join(os.getenv("APP_FOLDER"), os.getenv("FILTERED_DRIFT_REPORT_FILE"))

# Read the drift report content
with open(drift_report_file, "r") as file:
    drift_report_content = file.read()

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = ", ".join(receiver_email)  # Display purpose
message["Subject"] = subject  # Set before converting to string

# Email body
body = f"""
Hello,

Please find below the details of the drift detected in the infrastructure:

{drift_report_content}

Regards,
DevOps Team
"""
message.attach(MIMEText(body, "plain"))

# Attach the drift report file
with open(drift_report_file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(drift_report_file)}",
    )
    message.attach(part)

# Convert the message to a string
text = message.as_string()

# Enforce TLS 1.2 or higher using modern syntax
context = ssl.create_default_context()
context.minimum_version = ssl.TLSVersion.TLSv1_2

try:
    # Connect to the SMTP server using TLS 1.2 only
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")
