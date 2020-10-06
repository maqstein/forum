from forum_app.buisness_logic.smtp import smtp_server
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import NEWSLETTER_LOGIN, NEWSLETTER_PASSWORD
# будет ли лучше оставить тут функцию и потом ее вызывать из main.py?
# def login_smtp():
#     server = smtp_server()
#     server.login(email, password)



def send_email(send_to_adress,password):
    smtp_server.starttls()
    smtp_server.login(NEWSLETTER_LOGIN, NEWSLETTER_PASSWORD)
    msg = MIMEMultipart()
    msg['From'] = NEWSLETTER_LOGIN
    msg['To'] = send_to_adress
    msg['Subject'] = "password"
    msg.attach(MIMEText(f"your password is {password}",'Plain'))
    print(msg.as_string())
    smtp_server.sendmail(msg['From'],msg['To'],msg.as_string())
    
    smtp_server.quit()