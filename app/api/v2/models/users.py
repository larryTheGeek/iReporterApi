"""This module contains the user model that adds a new user to the db"""
import datetime
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash
from functools import wraps

# local imports
from .db import Db


class User():
    """handles all the user model related opperations """
    def __init__(self, firstname, lastname, othername, email, phoneNumber,
                 username, password, isAdmin=False):
        self.registered = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.isAdmin = isAdmin
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.email = email
        self.phoneNumber = phoneNumber
        self.username = username
        self.password = generate_password_hash(password.strip())

    def __repr__(self):
        """Creates a string representation of the User object"""
        return {
            'username': self.username,
            'isAdmin': self.isAdmin,
            'email': self.email
        }

    @classmethod
    def check_username(cls, username):
        """checks if username already exists"""
        sql = "SELECT * FROM users WHERE users.username=\'%s\' " % (username)
        curr = Db().cur
        curr.execute(sql)
        output = curr.fetchone()
        return output

    @classmethod
    def check_email(cls, email):
        """checks if email is already in use"""
        sql = "SELECT * FROM users WHERE users.email=\'%s\' " % (email)
        curr = Db().cur
        curr.execute(sql)
        output = curr.fetchone()
        return output

    def register_user(self):
        """Registers a new user into the database"""
        sql = "INSERT INTO users (firstname,\
                                  lastname,\
                                  othername,\
                                  email,\
                                  phoneNumber,\
                                  username,\
                                  registered,\
                                  isAdmin,\
                                  password)\
                            VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\
                            \'%s\',\'%s\',\'%s\')" % (
            self.firstname,
            self.lastname,
            self.othername,
            self.email,
            self.phoneNumber,
            self.username,
            self.registered,
            self.isAdmin,
            self.password
        )
        conn = Db().con
        curr = conn.cursor()
        curr.execute(sql)
        print("addedd")
        conn.commit()

    @staticmethod
    def get_a_user(id):
        """gets a user by id"""
        sql = f"SELECT * FROM users WHERE users.id={id}"
        curr = Db().cur
        curr.execute(sql)
        output = curr.fetchone()
        return output

    @classmethod
    def promote_user(cls, username):
        """Promotes a normal user to an admin """
        sql = "UPDATE users SET isAdmin=True WHERE users.username=%s"
        conn = Db().con
        curr = conn.cursor()
        curr.execute(sql, (username,))
        conn.commit()

    @classmethod
    def create_admin(cls):
        """creates a default  admin"""
        try:
            admin = User('Larry', 'karani', 'kubende',
                         'karani@gmail.com', '0701043047',
                         'admin', '6398litein')
            admin.register_user()
            admin.promote_user('admin')
        except:
            return 'user already exists'


def admin_required(f):
    """creates a decorator to limit a functionality to admin only"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = User.check_username(get_jwt_identity())
        if not user[8]:
            return {'message': 'Only admim can change status'}, 401
        return f(*args, **kwargs)
    return wrapper
