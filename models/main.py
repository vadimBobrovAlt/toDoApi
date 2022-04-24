from peewee import Model, MySQLDatabase
from peewee import TextField, DateTimeField, ForeignKeyField, BooleanField, PrimaryKeyField
from peewee import InternalError
import datetime
db = MySQLDatabase("toDo", host="127.0.0.1", port=3366, user="root", passwd="root")


class BaseModel(Model):
    id = PrimaryKeyField(null=False)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class User(BaseModel):
    username = TextField()
    password = TextField()
    name = TextField()
    chat_id = TextField(null=True)

    class Meta:
        db_table = 'users'


class Task(BaseModel):
    title = TextField()
    description = TextField(null=True)
    is_done = BooleanField(default=False)
    user = ForeignKeyField(User, backref='tasks')

    class Meta:
        db_table = 'tasks'


def init_db():
    try:
        db.connect()
        User.create_table()
        Task.create_table()
    except InternalError as px:
        print(str(px))
