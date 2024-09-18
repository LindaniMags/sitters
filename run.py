from app import create_app

flask_app = create_app()
"""Runs the flask application from app.py"""
if __name__ == "__main__":
    flask_app.run(host = "0.0.0.0", debug = True)