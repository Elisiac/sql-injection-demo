from flask_login import UserMixin

from app import db

###
# The following file contains our database definition. This is where we indicate what tables we have
# and what field they each contain.
# Note: We would normally use a hash for the password with a salt but for the purpose
# of this demo, we intentionally removed all encryption.
###

class User(db.Model, UserMixin):
    """
    Represents a database model of a user with columns 'id', 'username',
    'password'.
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        """
        Set the password of the user with the value provided.
        """
        self.password = password


    def check_password(self, password):
        """
        Check the given plaintext password with the password stored in the user record.
        """
        return self.password == password

    @classmethod
    def get_by_username(cls, username):
        """
        Returns the User associated with the given username.
        """
        return cls.query.filter_by(username=username).first()


class Record(db.Model):

    """
    Represents a database model of a record with columns 'id', 'description',
    'date', 'amount' and as foreign key the 'user_id'.
    """

    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    date = db.Column(db.Date)
    amount = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='user')
