from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
import os

# class ProfileFeed(UserMixin, BaseModel):
#     user = pw.ForeignKeyField(User, backref='profile_feeds')
#     image_path = pw.CharField(unique=False null=True)

class Post(BaseModel):
    user = pw.ForeignKeyField(User, backref='posts')
    image_path = pw.CharField()
    # caption = pw.CharField(null=True)

    def validate(self):
        pass

    @hybrid_property
    def post_image_url(self):
        return os.environ.get("S3_LOCATION") + self.image_path