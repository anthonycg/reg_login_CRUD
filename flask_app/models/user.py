from flask_bcrypt import Bcrypt
from flask import flash
import re
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL 
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('reg_login').query_db(query)
        users = []
        for user in users:
            users.append(cls(user))
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('reg_login').query_db(query, data)
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s, NOW(), NOW())"
        results = connectToMySQL('reg_login').query_db(query, data)
        return results

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('reg_login').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(form):
        is_valid = True
        if len(form['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(form['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid Email address!")
            is_valid = False
        if form['confirm_password'] != form['password']:
            flash("Passwords do not match!")
        if len(form['password']) < 6:
            flash("Password Must be at least 6 characters.")
            is_valid = False
        return is_valid
