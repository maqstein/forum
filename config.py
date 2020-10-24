import os

FORUM_DOCKER_HOST = os.getenv('FORUM_DOCKER_HOST') if os.getenv('FORUM_DOCKER_HOST') else '0.0.0.0'
FORUM_DOCKER_PORT = os.getenv('FORUM_DOCKER_PORT') if os.getenv('FORUM_DOCKER_PORT') else 8000
DOMAIN = os.getenv('DOMAIN') if os.getenv('DOMAIN') else 'localhost'
POSTGRES_URL = os.getenv('POSTGRES_URL')

SMTP_ADDRESS = os.getenv('SMTP_ADDRESS') if os.getenv('SMTP_ADDRESS') else "smtp.gmail.com"
SMTP_PORT = os.getenv('SMTP_PORT') if os.getenv('SMTP_PORT') else 587
NEWSLETTER_LOGIN = os.getenv('NEWSLETTER_LOGIN')
NEWSLETTER_PASSWORD = os.getenv('NEWSLETTER_PASSWORD')
