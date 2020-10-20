from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
mail = Mail(app)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


from blog.user.views import users as usersModule
app.register_blueprint(usersModule)

from blog.article.views import article as articleModule
app.register_blueprint(articleModule)