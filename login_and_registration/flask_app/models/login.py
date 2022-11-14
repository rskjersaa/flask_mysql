from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL

class Login:
    def __init__(self,data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_At']
        self.updated_at = data ['updated_At']