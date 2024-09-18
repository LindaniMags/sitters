from flask_login import UserMixin

from app import db

class User(db.Model, UserMixin):
    __tablename__="users"

    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer)
    password = db.Column(db.String, nullable = False)
    location = db.Column(db.String)
    services = db.Column(db.String)

    def __repr__(self):
        """Return a string representation of the User.

        The string is in the format of:
        <User: username, Role: services>

        Parameters:
        None

        Returns:
        str
        """
        return f"<User: {self.username}, Role: {self.services}>"
    
    def get_id(self):
        """Return the user's id.

        Parameters:
        None

        Returns:
        int
        """
        return self.uid
    
