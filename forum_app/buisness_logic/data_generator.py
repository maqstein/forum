from forum_app.buisness_logic.models import database
from forum_app.buisness_logic.models import Users, Sessions, Posts, Comments
from forum_app.exceptions import NoArgumentsPassedError, get_exception_info

from datetime import datetime, timedelta
import uuid


async def get_data_from_table(table_name, fetch_one=False, **kwargs):
    try:
        if not kwargs:
            raise NoArgumentsPassedError

        query = f'SELECT * FROM "{table_name}" WHERE'
        query_value = dict()

        for key, value in kwargs.items():
            query += f' {key} = :{key}'
            query_value[key] = value

        if fetch_one:
            return await database.fetch_one(query=query, values=query_value)

        return await database.fetch_all(query=query, values=query_value)

    except:
        print(get_exception_info())


async def get_wall():
    posts = []
    query = 'SELECT * FROM "Posts" limit 10'
    posts_in_db = await database.fetch_all(query=query)
    for post in posts_in_db:
        # async for post in database.iterate(query=query):
        author = await get_user(id=post['author_id'])

        thumbnail = f"{post['content'][:100]}"
        if len(post['content']) > 100:
            thumbnail += "..."

        posts.append({
            "id": post['id'],
            # только первые 100 символов поста видны при прокрутке поста на главной
            "thumbnail_text": thumbnail,
            "author_name": author['username'],
            "author_id": author['id'],
            "likes": post['likes_counter'],
            "dislikes": post['dislikes_counter'],
            "comments_counter": post['comments_counter'],
        })
    return posts


async def get_user(**kwargs):
    """
    gets users from database sorted by given arguments
    e.g.
    get_user(id=228)
    get_user(email=hellothere@frick.you)
    get_user(registration_confirmed=False)
    get_user(token="a_token_here")
    """
    try:
        if not kwargs:
            raise NoArgumentsPassedError

        if "token" in kwargs.keys():
            return await get_user_by_token(kwargs['token'])

        query = 'SELECT * FROM "Users" WHERE'
        query_value = dict()

        for key, value in kwargs.items():
            query += f' {key} = :{key}'
            query_value[key] = value

        user = await database.fetch_one(query=query, values=query_value)
        return user

    except:
        print(get_exception_info())


async def get_post_by_id(post_id):
    query = 'SELECT * FROM "Posts" WHERE id = :id'
    values = dict(id=post_id)
    return await database.fetch_one(query=query, values=values)


async def get_comment_by_post_id(post_id):
    try:
        query = 'SELECT * FROM "Comments" WHERE post_id = :id'
        values = dict(id=post_id)
        # these comments are lonely because of them not having authors yet
        lonely_comments = await database.fetch_all(query=query, values=values)

        happy_comments = list()

        for comment in lonely_comments:
            comment_author = await get_user(id=comment['author_id'])

            happy_comment = dict(comment)
            happy_comment['author'] = comment_author
            happy_comments.append(happy_comment)

        return happy_comments

    except:
        print(get_exception_info())


async def create_user(user_to_create):
    try:
        if user_to_create:
            query = Users.insert().values(
                username=user_to_create.username,
                email=user_to_create.email,
                password=user_to_create.password
            )
            await database.execute(query)

        else:
            raise NoArgumentsPassedError
    except:
        print(get_exception_info())
    # except DuplicateError:
    #     TODO()


async def print_all_users():
    try:
        query = Users.select()
        users = await database.fetch_all(query)
        for user in users:
            print(user['email'], user['password'])
    except:
        print(get_exception_info())


async def create_session_token(user_id, days_to_expire=30):
    await delete_previous_token(user_id)
    return await create_new_token(user_id, days_to_expire=days_to_expire)


async def delete_previous_token(user_id):
    try:
        query = 'DELETE FROM "Sessions" WHERE user_id = :user_id'
        value = {'user_id': user_id}
        await database.execute(query=query, values=value)
    except:
        print(get_exception_info())


async def create_new_token(user_id, days_to_expire):
    try:
        new_token = uuid.uuid4()
        query = Sessions.insert().values(
            user_id=user_id,
            token=new_token,
            expires=datetime.now() + timedelta(days=days_to_expire)
        )
        await database.execute(query)
        return new_token
    except:
        print(get_exception_info())


async def get_user_by_token(token):
    # TODO Сделать проверку на время жизни куки
    try:
        token = uuid.UUID(token)
        query = 'SELECT * FROM "Sessions" WHERE token = :token'
        value = {"token": token}
        session = await database.fetch_one(query=query, values=value)
        # DO NOT GET USER BY TOKEN IN HERE
        return await get_user(id=session['user_id'])
    except:
        print(get_exception_info())


async def create_post(author, content):
    try:
        # TODO добавить экранирование и проверку содержания поста
        query = Posts.insert().values(
            author_id=author["id"],
            content=content,
            likes_counter=0,
            dislikes_counter=0,
            comments_counter=0,
        )
        await database.execute(query)
    except:
        print(get_exception_info())


async def create_comment(author, post_id, text):
    try:
        await increment_comment_counter(post_id)
        query = Comments.insert().values(
            post_id=post_id,
            author_id=author['id'],
            content=text,
            likes_counter=0,
            dislikes_counter=0,
        )
        await database.execute(query)
    except:
        print(get_exception_info())


async def increment_comment_counter(post_id):
    try:
        query = 'UPDATE "Posts" SET comments_counter = comments_counter+1 where id=:post_id'
        values = dict(post_id=post_id)
        await database.execute(query=query, values=values)
    except:
        print(get_exception_info())


async def delete_post(post_id):
    try:
        query = 'DELETE FROM "Posts" WHERE id=:post_id'
        values = dict(post_id=post_id)
        await database.execute(query=query, values=values)
    except:
        print(get_exception_info())


async def update_post_content(post_id, content_to_add):
    try:
        # query = 'UPDATE "Posts" SET content=content||E\':content_to_add\' WHERE id=:post_id'
        query = 'UPDATE "Posts" SET content=content||:content_to_add WHERE id=:post_id'
        # добавить счетчик апдейтов
        values = dict(content_to_add=f"\nUPD : {content_to_add}", post_id=post_id)
        await database.execute(query=query, values=values)

    except:
        print(get_exception_info())
