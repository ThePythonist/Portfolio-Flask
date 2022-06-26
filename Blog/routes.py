from flask import render_template, url_for, redirect, flash, request
from Blog.forms import RegistrationForm, LoginForm
from Blog.models import User, Post
from Blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "author":"Arash",
        "title":"JS Tutorial",
        "content":"Lorem ipsum dolor sit amet, consectetur adipisicing elit. Delectus eligendi inventore laborum maiores numquam omnis veritatis. Cupiditate ipsam magnam numquam rem vero! A cum ducimus earum minus vel veritatis voluptatibus!",
        "date":"Dec 25",
        "id":"1",
        "cover":"./static/images/js-cover.jpg",
    },
    {
        "author":"Arash",
        "title":"PYTHON Tutorial",
        "content":"Lorem ipsum dolor sit amet, consectetur adipisicing elit. Delectus eligendi inventore laborum maiores numquam omnis veritatis. Cupiditate ipsam magnam numquam rem vero! A cum ducimus earum minus vel veritatis voluptatibus!",
        "date":"Dec 25",
        "id":"2",
        "cover":"./static/images/python-cover.jpg",
    },
    {
        "author":"Arash",
        "title":"C# Tutorial",
        "content":"Lorem ipsum dolor sit amet, consectetur adipisicing elit. Delectus eligendi inventore laborum maiores numquam omnis veritatis. Cupiditate ipsam magnam numquam rem vero! A cum ducimus earum minus vel veritatis voluptatibus!",
        "date":"Dec 25",
        "id":"3",
        "cover":"./static/images/Csharp-cover.png",
    },
]


@app.route("/")
@app.route("/Home")
def Home():
    return render_template("Home.html",title='Home')


@app.route("/Blog")
def Blog():
    return render_template("Blog.html", title='Blog', posts=posts)


@app.route("/Resume")
def Resume():
    return render_template("Resume.html", title='Resume')


@app.route("/About")
def About():
    return render_template("About.html", title='About')


@app.route("/Contact")
def Contact():
    return render_template("Contact.html", title='Contact')


@app.route("/Register", methods=["GET","POST"])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for("Home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.casefold(), password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created','success')
        return redirect(url_for("Login"))

    return render_template("Register.html", title='Register', form=form)


@app.route("/Login", methods=["GET","POST"])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for("Home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.casefold()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) :
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Successfully Logged In','success')
            return redirect(next_page) if next_page else redirect(url_for("Home"))
        else :
            flash('Invalid Credentials','fail')

    return render_template("Login.html", title='Login', form=form)


@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for("Home"))


@app.route("/Dashboard")
@login_required
def Dashboard():
    return render_template("Dashboard.html", title='User Dashboard')
