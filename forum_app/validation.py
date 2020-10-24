from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str


class SignIn(BaseModel):
    email: str
    password: str


class CreatePostRequest(BaseModel):
    username: str
    post_text: str


class CreatePostModel(BaseModel):
    post_text: str


class CreateCommentModel(BaseModel):
    comment_text: str
