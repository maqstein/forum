import smtplib
from config import SMTP_ADDRESS, SMTP_PORT

smtp_server = smtplib.SMTP(f'{SMTP_ADDRESS}: {SMTP_PORT}')
