import os
from peewee import *

ABS_DB_HOST = os.environ.get("ABS_DB_HOST", "data.ksdl.xyz")
ABS_DB_PORT = os.environ.get("ABS_DB_PORT", 3306)
ABS_DB_NAME = os.environ.get("ABS_DB_NAME", "ss3")
ABS_DB_USER = os.environ.get("ABS_DB_USER", "daydayup")
ABS_DB_PASSWORD = os.environ.get("ABS_DB_PASSWORD", "daydayup666.")

db = MySQLDatabase(ABS_DB_NAME, host=ABS_DB_HOST, port=ABS_DB_PORT, user=ABS_DB_USER, passwd=ABS_DB_PASSWORD)

db.connect()


class BaseModel(Model):

    class Meta:
        database = db


class Daydayup(BaseModel):
    email = CharField(primary_key=True, null=False)
    expire_in = DateTimeField(default="2099-06-04 00:05:00")


if __name__ == "__main__":
    user = Daydayup.get(email='1@qq.com')
    print(user.expire_in)
