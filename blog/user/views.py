from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from blog import db, mail
from blog.article.models import Article
from blog.user.forms import LoginForm, RegisterForm, ArticleForm, RequestResetForm, ResetPasswordForm
from blog.user.models import User
from blog.user.decorators import login_required, login_management

users = Blueprint('users', __name__, url_prefix='/users')



@users.route("/profile")
@login_required
def profile():
    articles = Article.query.filter_by(author = session['user_name']).all()
    return render_template("user/profile.html", user = g.user, articles = articles)

@users.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session["user_id"])

@users.route("/login", methods=["GET","POST"])
@login_management
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash('welcome %s' % user.name, "primary")
            return redirect(url_for('users.profile'))
        flash("wrong username or password", 'danger')
    return render_template('user/login.html', form = form)

@users.route('/register', methods=["GET","POST"])
@login_management
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        flash("Thanks for registering", "success")
        return redirect(url_for('users.profile'))
    return render_template("user/register.html", form = form)

@users.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Successfully Logout", "warning")
    return redirect(url_for('users.login'))

@users.route("/addarticle", methods=["POST","GET"])
@login_required
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST":
        title = request.form.get('title')
        author = session['user_name']
        content = request.form.get('content')
        newArticle = Article(title=title, author=author, content=content)
        db.session.add(newArticle)
        db.session.commit()
        flash("Teşekkürler %s" % session['user_name'], "primary")
        return redirect(url_for("users.profile"))
    return render_template("user/addarticle.html", form = form)

@users.route("/edit/<string:id>", methods=["POST","GET"])
@login_required
def edit(id):
    articleId = Article.query.filter_by(id = id).first()
    if request.method == "GET":
        form = ArticleForm()
        form.title.data = articleId.title
        form.content.data = articleId.content
        return render_template("user/edit.html", form = form)
    elif request.method == "POST":
        form = ArticleForm(request.form)
        articleId.title = form.title.data
        articleId.content = form.content.data
        db.session.commit()
        flash("Article updated successfully", "warning")
        return redirect(url_for("users.profile"))

@users.route("/delete/<string:id>")
@login_required
def delete(id):
    articleId = Article.query.filter_by(id = id).first()
    db.session.delete(articleId)
    db.session.commit()
    flash("Article deleted successfully", "secondary")
    return redirect(url_for("users.profile"))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password reset request", sender='noreply@info.com', recipients=[user.email])
    msg.body = f"To reset your password visit following link: {url_for('users.reset_token', token = token, _external=True)}"
    mail.send(msg)

@users.route("/reset_password", methods = ["GET","POST"])
def reset_request():
    if "user_id" in session:
        return redirect(url_for("articles.index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email has been sent", 'info')
        return redirect(url_for("users.login"))
    return render_template("user/reset_request.html", form = form)

@users.route("/reset_password/<string:token>", methods=["GET","POST"])
def reset_token(token):
    if "user_id" in session:
        return redirect(url_for("articles.index"))
    user = User.verify_reset_token(token=token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pasww = generate_password_hash(form.password.data)
        user.password = hashed_pasww
        db.session.commit()
        flash("Password changed", "success")
        return redirect(url_for('users.login'))
    return render_template("user/reset_token.html", form = form)


@users.route("profile/account", methods = ["GET","POST"])
@login_required
def account():
    user_image = User.query.filter_by(image_file = User.image_file).first()
    image_file = url_for('static', filename='img/profile_pics/'+ user_image.image_file)
    return render_template("user/account.html", image_file = image_file)

    
    
    
