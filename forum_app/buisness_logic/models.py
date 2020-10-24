from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config import POSTGRES_URL
from databases import Database
from forum_app import app
import uuid

metadata = MetaData()
database = Database(POSTGRES_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


Users = Table(
    "Users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    # TODO add unique email
    # Column("email",String,unique=True),
    Column("email", String, unique=True),
    Column("password", String),
    Column("registration_confirmed", Boolean, default=False),
)

Sessions = Table(
    "Sessions", metadata,
    Column("user_id", Integer, ForeignKey("Users.id", ondelete="cascade")),
    # nullable не работает, почему?
    Column("token", UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False),
    # потому что нужно руками дропнуть таблицу в бд и перезапустить докер 
    # как это обходить?

    # trust no one
    Column("expires", DateTime)
)

Posts = Table(
    "Posts", metadata,
    Column("id", Integer, primary_key=True),
    Column("author_id", Integer, ForeignKey("Users.id")),
    # TODO сохранять посты с базовой html разметкой как, например, в telegra.ph
    # Column("content",HTML or Markdown)
    Column("content", String),
    # default=0 не робит, почему? потому что я вставляю не через sqlalchemy? но primary_key при этом работает...
    # может primary создается sqlalchemy при создании таблицы, а дефолт ставится самим фреймворком, а не бд?
    Column("views_counter", Integer, default=0),
    Column("likes_counter", Integer, default=0),
    Column("dislikes_counter", Integer, default=0),
    Column("comments_counter", Integer, default=0),
)

Comments = Table(
    "Comments", metadata,
    Column("id", Integer, primary_key=True),
    Column("post_id", Integer, ForeignKey("Posts.id", ondelete="cascade"), nullable=False),
    Column("author_id", Integer, ForeignKey("Users.id"), nullable=False),
    Column("content", String),
    Column("likes_counter", Integer, default=0),
    Column("dislikes_counter", Integer, default=0),
)

engine = create_engine(
    POSTGRES_URL
)
metadata.create_all(engine)
