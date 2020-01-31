from models.base_model import BaseModel
from models.post import Post
import peewee as pw

class Endorsement(BaseModel):
    post = pw.ForeignKeyField(Post, backref='endorsements')
    amount = pw.DecimalField(decimal_places=2)

    def validate(self):
        pass