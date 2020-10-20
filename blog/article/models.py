from blog import db
from datetime import datetime

class Article(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    content = db.Column(db.String)
    created_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __init__(self, title=None, author=None, content=None):
        self.title = title
        self.author = author
        self.content = content


    def __repr__(self):
        return '<title %s>' % Article.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    message = db.Column(db.String)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship("Article", backref=db.backref('article', lazy=True))
    comment_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)


    def __init__(self, name=None, email=None, message=None, article_id=None):
        self.name = name
        self.email = email
        self.message = message
        self.article_id = article_id

    def __repr__(self):
        return '<email %s>' % Comment.email

    