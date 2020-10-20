from blog import db
from blog import Serializer
from blog import app

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    image_file = db.Column(db.String(20), nullable = False, default = "default.jpg")


    def __init__(self, name=None, email=None, password=None, image_file = None):
        self.name = name
        self.email = email
        self.password = password
        self.image_file = image_file
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({'user_id': self.id}).decode("utf-8")
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"], expires_in = 1800)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.name}','{self.email}')"

