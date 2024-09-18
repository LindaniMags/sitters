from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from models import User

def register_routes(app, db, bcrypt):
    @app.route("/")
    def index():
        users = User.query.all()
        return render_template("index.html", users=users)
    
    @app.route("/signup", methods = ["GET", "POST"])
    def signup():
        if request.method == "GET":
            return render_template("signup.html")
        elif request.method == "POST":
            username = request.form.get("username")
            age =request.form.get("age")
            password = request.form.get("password")
            location = request.form.get("location")
            services = request.form.get("services")

            hashed_password = bcrypt.generate_password_hash(password)

            user = User(username=username, age=age, password = hashed_password, location=location, services=services)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for("index"))

    @app.route("/login", methods = ["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter(User.username == username).first()

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("index"))
            else:
                return "Login Failed"

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/profile")
    def profile():
        if current_user.is_authenticated:
            return render_template("profile.html")
        else:
            return "Not logged in"


    @app.route("/update", methods=["GET","POST"])
    def update():
        if request.method == "GET":
            if current_user.is_authenticated:
                return render_template("update.html")
            else:
                return "Not logged in"
        elif request.method == "POST":
            current_user.username = request.form.get("username")
            current_user.age =request.form.get("age")
            current_user.location = request.form.get("location")
            current_user.services = request.form.get("services")

            db.session.commit()

            return redirect(url_for("index"))