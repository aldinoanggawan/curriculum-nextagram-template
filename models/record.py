from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Record(BaseModel):
    follower = pw.ForeignKeyField(User, backref='followings')
    following = pw.ForeignKeyField(User, backref='followers')
    approved = pw.BooleanField(default=False)

    def validate(self):
        pass