import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

def find_file_with_today_date(directory):
    today = datetime.now().strftime('%Y-%m-%d')
    target_filename = f"pizza_sales_{today}.xlsx"
    for filename in os.listdir(directory):
        if filename == target_filename:
            return os.path.join(directory, filename)
    return None

def send_daily_report(file_to_send):
    # Email server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'votre_email@gmail.com'
    smtp_password = 'votre_mot_de_passe'
    
    # Email content
    from_addr = smtp_username
    to_addr = 'votre_email@gmail.com'
    subject = 'Daily Report'
    body = 'This is the content of the daily report.'
    
    # Setup email
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Attaching the file
    if file_to_send:
        part = MIMEBase('application', 'octet-stream')
        with open(file_to_send, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(file_to_send))
        msg.attach(part)
    
    # Send email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()
    
    print("Email sent!")

if __name__ == '__main__':
    directory = 'E:/KETRIKA/script_py/data'  
    file_to_send = find_file_with_today_date(directory)
    if file_to_send:
        send_daily_report(file_to_send)
    else:
        print("No file found for today.")
