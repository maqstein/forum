from forum_app import app, templates

from forum_app.buisness_logic.data_generator import get_user, create_user,\
print_all_users, create_session_token, create_post, create_comment, get_post_by_id,\
delete_post, update_post_content

from forum_app.buisness_logic.custom_response import redirect, index_template
from forum_app.buisness_logic.custom_response import index_template, register_template, sign_in_template, \
create_post_template, render_post_template, render_user_view_template, render_edit_post_template, recover_password, \
render_about_template


from forum_app.validation import CreatePostRequest, RegisterUser, SignIn, CreatePostModel, CreateCommentModel
from forum_app.exceptions import get_exception_info

from forum_app.buisness_logic.email import send_email

from fastapi import Request, Form, Response, Cookie, Query
from typing import Optional

#TODO нужно сделать отдельный файл(или класс?) для response
#TODO Сделать pop-up уведомления или что то подобное



@app.get("/")
async def index(request: Request, session_id : Optional[str] = Cookie(None)):
    return await index_template(request, session_id)


@app.get("/register")
async def register_user_index(request: Request, session_id : Optional[str] = Cookie(None)):
    return await register_template(request, session_id)


@app.post("/register")
async def register_user(request: Request):
    user_to_create = RegisterUser(**await request.form())
    await create_user(user_to_create)

    return redirect("enter")


@app.get("/enter")
async def get_sign_in_page(request: Request, session_id : Optional[str] = Cookie(None)):
    return await sign_in_template(request, session_id)


@app.post("/enter")
async def sign_in(request: Request): 
    user_to_login = SignIn(**await request.form())
    user = await get_user(email=user_to_login.email)

    if not user:
        return Response(content=123)

    if user['password'] == user_to_login.password:
        cookie_life_time = 30 # days 

        session_token = await create_session_token(user["id"])

        
        response = redirect("/")
        response.set_cookie(key="session_id", value=session_token, expires=60*60*24*cookie_life_time)

        return response

    # TODO invalid password form
    return Response(content=user_to_login.json())


@app.get("/create")
async def create_post_static(request: Request, session_id : Optional[str] = Cookie(None)):
    return await create_post_template(request,session_id)


@app.post("/create")
async def create_post_post(request: Request, session_id : Optional[str] = Cookie(None)):
    if not session_id:
        return redirect("enter")

    new_post = CreatePostModel(**await request.form())
    author = await get_user(token=session_id)
    
    await create_post(author,new_post.post_text)
    return redirect("/")


@app.get("/logout")
async def user_logout(request: Request):
    response = redirect("/")
    response.set_cookie(key="session_id", value=0, max_age = 0)
    return response


@app.post("/post/{post_id}")
async def create_comment_view(request: Request, post_id : int, comment_text : str = Form(...), session_id : Optional[str] = Cookie(None)):
    try:
        # TODO проверка на существование поста
        # TODO фильтр текста

        if not session_id:
            return redirect(f"/enter") # добавить сообщение об авторизации

        comment_author = await get_user(token=session_id)
        await create_comment(comment_author, post_id, comment_text)


        return redirect(f"/post/{post_id}")
    except:
        print(get_exception_info())


@app.get("/post/{post_id}")
async def get_post_template(request: Request, post_id : int, session_id : Optional[str] = Cookie(None)):
    return await render_post_template(request, post_id, session_id)


@app.get("/user/{user_id}")
async def user_view_template(request: Request, user_id: int, session_id : Optional[str] = Cookie(None)):
    return await render_user_view_template(request,user_id,session_id)


@app.post("/user/{user_id}")
async def user_action_to_his_posts(request: Request, user_id: int, session_id : Optional[str] = Cookie(None), Button : str = Form(...), post_id : int = Form(...)):
    if Button == "edit":
        return redirect(f"/edit/{post_id}")
    if bool(get_post_by_id(post_id)):
        await delete_post(post_id)
        return redirect(f"/user/{user_id}")
    return redirect("/error")


@app.get("/about")
async def about(request: Request, session_id : Optional[str] = Cookie(None)):
    # TODO implement "about" page
    return await render_about_template(request,session_id)


@app.get("/edit/{post_id}")
async def get_edit_template(request: Request, post_id : int, session_id : Optional[str] = Cookie(None)):
    return await render_edit_post_template(request,post_id,session_id)


@app.post("/edit/{post_id}")
async def update_post(request: Request, post_id : int, postUpdate : str = Form(...), session_id : Optional[str] = Cookie(None)):
    user = await get_user(token=session_id)
    post = await get_post_by_id(post_id)

    if post['author_id'] == user['id']:
        await update_post_content(post_id,postUpdate)
        return redirect(f"/post/{post_id}")

    return redirect("/enter")


@app.get("/password_recovery")
async def send_password_by_email_template(request: Request):
    return await recover_password(request)


@app.post("/password_recovery")
async def send_password_by_email(request: Request, email : str = Form(...)):
    user = await get_user(email=email)
    send_email(user['email'],user['password'])
    # if user:
    #     return await email_is_sent_template(request=Request, email=email)

    return await recover_password(request)
    # return await recover_password(request, alert="аккаунт с таким емаилом не существует")