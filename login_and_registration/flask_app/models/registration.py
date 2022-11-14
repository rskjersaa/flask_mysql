from flask_app import app
from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Registration:
    db='login_and_registration'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data ['updated_at']

#Create
    @classmethod
    def save(cls,data):
        query ="""INSERT INTO registrations (first_name, last_name, email, password) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query,data)

#Read
    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM registrations WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def getByEmail(cls, data):
        print(data)
        query = "SELECT * FROM registrations WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print (results)
        return results[0]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM registrations;"
        results = connectToMySQL(cls.db).query_db(query)
        registrants = []
        for row in results:
            registrants.append(cls.row)
            return registrants


#Update

#Delete

#Validate
    @staticmethod
    def validate_registration(registrant):
        is_valid = True
        query = "SELECT * FROM registrations WHERE email = %(email)s;"
        results = connectToMySQL(Registration.db).query_db(query,registrant)
        print(results)
        if len(results) >=1:
            flash("email is already taken")
            is_valid = False
        if len(registrant['first_name']) < 2:
            flash("First name must be at least two characters", "register")
            is_valid = False
        if len(registrant['last_name']) < 2:
            flash("Last name must be at least two characters", "register")
            is_valid = False
        if not EMAIL_REGEX.match(registrant['email']):
            flash("Invalid email format", "register")
            is_valid = False
        if len(registrant['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid = False
        if registrant['password'] != registrant['confirm']:
            flash("Passwords do not match","register")
            is_valid = False
            #test some things
            print("Validation - user is valid:", is_valid)
        return is_valid

    @staticmethod
    def validate_login(registrant):
        is_valid = True
        
        
        email=Registration.getByEmail(registrant)
        if not registrant['email'] :
            flash('invalid email or password', "login")
            is_valid = False
        if not bcrypt.check_password_hash(email['password'],registrant['password']):
            flash('invalid email or password', 'login')
            is_valid = False
        return is_valid