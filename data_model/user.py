from peewee import *

db = MySQLDatabase("ss3", host="data.ksdl.xyz", port=3306, user="daydayup", passwd="daydayup666.")
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
