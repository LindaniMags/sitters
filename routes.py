from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from models import User

def register_routes(app, db, bcrypt):
    """
    This function registers routes for the following endpoints:
        - /
        - /signup
        - /login
        - /logout
        - /profile
        - /update

    Each route is responsible for rendering a template and handling post requests
    for the respective endpoint. The routes also handle authentication and
    authorization for the endpoints.

    Parameters:
    app (Flask): The Flask application instance.
    db (SQLAlchemy): The SQLAlchemy database instance.
    bcrypt (Bcrypt): The Bcrypt instance for hashing passwords.

    Returns:
    None
    """
    @app.route("/")
    def index():        
        """
        The root route for the application.

        This route is responsible for rendering the 'index.html' template and
        passing all users in the database to the template.

        Returns:
        The rendered 'index.html' template with all users in the database.
        """
        users = User.query.all()
        return render_template("index.html", users=users)
    
    @app.route("/signup", methods = ["GET", "POST"])
    def signup():
        """
        The signup route for the application.

        This route is responsible for rendering the 'signup.html' template and
        handling post requests for the signup endpoint. The route also handles
        creating a new user in the database and hashing their password.

        Parameters:
        None

        Returns:
        The rendered 'signup.html' template on GET requests. Redirects to the
        index route on POST requests.
        """
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
        """
        The login route for the application.

        This route is responsible for rendering the 'login.html' template and
        handling post requests for the login endpoint. The route also handles
        authenticating a user and logging them in.

        Parameters:
        None

        Returns:
        The rendered 'login.html' template on GET requests. Redirects to the
        index route if the login is successful, otherwise returns "Login Failed"
        on POST requests.
        """
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
        """
        The logout route for the application.

        This route is responsible for logging out the current user and
        redirecting them to the index route.

        Parameters:
        None

        Returns:
        A redirect to the index route.
        """

        logout_user()
        return redirect(url_for("index"))

    @app.route("/profile")
    def profile():
        """
        The profile route for the application.

        This route is responsible for rendering the 'profile.html' template if the
        user is authenticated, otherwise it returns "Not logged in".

        Parameters:
        None

        Returns:
        The rendered 'profile.html' template on GET requests or "Not logged in" if
        the user is not authenticated.
        """
        if current_user.is_authenticated:
            return render_template("profile.html")
        else:
            return "Not logged in"


    @app.route("/update", methods=["GET","POST"])
    def update():
        """
        The update route for the application.

        This route is responsible for rendering the 'update.html' template if the
        user is authenticated and the request method is GET, otherwise it returns
        "Not logged in".

        If the request method is POST, the route updates the current user's
        information in the database with the posted data and redirects to the
        index route.

        Parameters:
        None

        Returns:
        The rendered 'update.html' template on GET requests or a redirect to the
        index route on POST requests.
        """

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