import smtplib
from config import SMTP_ADRESS, SMTP_PORT

smtp_server = smtplib.SMTP(f'{SMTP_ADRESS}: {SMTP_PORT}')