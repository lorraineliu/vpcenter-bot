import os
from peewee import *

ABS_DB_HOST = os.environ.get("DB_HOST", "")
ABS_DB_PORT = os.environ.get("DB_PORT", 3306)
ABS_DB_NAME = os.environ.get("DB_NAME", "")
ABS_DB_USER = os.environ.get("DB_USER", "")
ABS_DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

db = MySQLDatabase(ABS_DB_NAME, host=ABS_DB_HOST, port=ABS_DB_PORT, user=ABS_DB_USER, passwd=ABS_DB_PASSWORD)
db.connect()


class BaseModel(Model):

    class Meta:
        database = db


class Daydayup(BaseModel):
    email = CharField(primary_key=True, null=False)
    expire_in = DateTimeField(default="2099-06-04 00:05:00")


if __name__ == "__main__":
    user = Daydayup.get(email='100@qq.com')
    print(user)
