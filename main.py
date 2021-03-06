import uvicorn
from config import FORUM_DOCKER_HOST, FORUM_DOCKER_PORT, NEWSLETTER_LOGIN, NEWSLETTER_PASSWORD
from forum_app.buisness_logic.smtp import smtp_server

if __name__ == "__main__":
    uvicorn.run("forum_app:app", host=FORUM_DOCKER_HOST,port=FORUM_DOCKER_PORT,reload=True,debug=True)