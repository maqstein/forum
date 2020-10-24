from forum_app import templates
from fastapi.responses import RedirectResponse
from forum_app.buisness_logic.data_generator import get_wall, get_user, get_post_by_id, \
    get_comment_by_post_id, get_data_from_table

from forum_app.exceptions import get_exception_info


def redirect(path: str, status_code=302):
    return RedirectResponse(path, status_code)


async def index_template(request, session_id):
    values = {"request": request}
    if session_id:
        user = await get_user(token=session_id)
        values['user'] = user

    wall = await get_wall()
    values['posts'] = wall

    return templates.TemplateResponse("index.html", values)


async def register_template(request, session_id):
    values = {"request": request}

    if session_id:
        user = await get_user(token=session_id)
        values['user'] = user

    return templates.TemplateResponse("register_user.html", values)


async def sign_in_template(request, session_id):
    return templates.TemplateResponse("sign_in.html", {"request": request})


async def create_post_template(request, session_id):
    values = {"request": request}
    if session_id:
        user = await get_user(token=session_id)
        values['user'] = user

    return templates.TemplateResponse("create_post.html", values)


async def render_post_template(request, post_id, session_id):
    try:
        values = {"request": request}
        if session_id:
            user = await get_user(token=session_id)
            values['user'] = user

        post = await get_post_by_id(post_id)
        values['post'] = post

        author = await get_user(id=post['author_id'])
        values['author'] = author

        comments = await get_comment_by_post_id(post_id)
        values['comments'] = comments

        return templates.TemplateResponse("post_view.html", values)

    except:
        print(get_exception_info())


async def render_user_view_template(request, user_id, session_id):
    try:
        values = dict(request=request)

        if session_id:
            user = await get_user(token=session_id)
            values['user'] = user

        posts = await get_data_from_table("Posts", author_id=user_id)
        values['posts'] = posts

        author = await get_user(id=user_id)
        values['author'] = author

        return templates.TemplateResponse("user_view.html", values)

    except:
        print(get_exception_info())


async def render_edit_post_template(request, post_id, session_id):
    try:
        values = dict(request=request)

        post = await get_data_from_table("Posts", fetch_one=True, id=post_id)
        values['post'] = post

        if session_id:
            user = await get_user(token=session_id)
            values['user'] = user
            if user['id'] != post['author_id']:
                return redirect("/enter")
        else:
            # юзверь не залогинился
            return redirect("/enter")

        return templates.TemplateResponse("edit_post.html", values)
    except:
        print(get_exception_info())


async def recover_password(request):
    try:
        values = dict(request=request)
        return templates.TemplateResponse("recover_password.html", values)
    except:
        print(get_exception_info())


async def render_about_template(request, session_id):
    try:
        values = dict(request=request)

        if session_id:
            user = await get_user(token=session_id)
            values['user'] = user

        return templates.TemplateResponse("about.html", values)
    except:
        print(get_exception_info())
