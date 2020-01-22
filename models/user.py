from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        password_input = self.password

        if duplicate_username:
            self.errors.append("Username is being used, try other username!")
        if duplicate_email:
            self.errors.append("Email is being used, try to log in using this email or click forgot password!")
        
        if len(password_input) < 6:
            self.errors.append("Password should be longer than 6 characters")
        if re.search('[A-Z]', password_input) is None:
            self.errors.append("Password should have both uppercase and lowercase characters")
        if re.search('[!@#$%^&*_?-]', password_input) is None:
            self.errors.append("Password should have at least one special character")
        else:
            self.password = generate_password_hash(password_input)