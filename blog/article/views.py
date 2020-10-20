from flask import Blueprint, render_template, flash, redirect, url_for,g,session, request
from blog import db, mail
from blog.article.models import Article, Comment
from blog.user.decorators import login_required
from blog.user.models import User

article = Blueprint('articles', __name__, url_prefix='/')


@article.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session["user_id"])

@article.route("/")
def index():
    return render_template("blog/index.html")

@article.route("/about")
def about():
    return render_template("blog/about.html")

@article.route("/articles")
@login_required
def articles():
    articlesAll = Article.query.all()
    return render_template("blog/articles.html", articlesAll = articlesAll)

@article.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Successfully Logout", "warning")
    return redirect(url_for('users.login'))

@article.route('/article/<string:id>', methods=["GET","POST"])
@login_required
def articleFirst(id):
    articleFirst = Article.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(article_id=id).all()
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        comment = Comment(name=name, email=email, message=message, article_id = id)
        db.session.add(comment)
        flash("Thank you for your coment", "success")
        db.session.commit()
        return redirect(request.url)
    return render_template('blog/article.html', articleFirst = articleFirst, comments = comments)
