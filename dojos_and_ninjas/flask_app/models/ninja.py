from flask_app.config.mysqlconnection import connectToMySQL

class Ninja:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_At']
        self.updated_at = data ['updated_At']

    

    @classmethod
    def save(cls,data):
        query ="INSERT INTO ninjas (first_name, last_name, age, dojo_id) VALUES (%(first_name)s,%(last_name)s,%(age)s,%(dojo_id)s);"
        result = connectToMySQL('dojosandninjas').query_db(query,data)
        return result

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM ninjas WHERE id = %(id)s;"
        result = connectToMySQL('dojosandninjas').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE ninjas SET first_name=%(first_name)s, last_name=%(last_name)s, age=%(age)s, updated_at=NOW() WHERE id= %(id)s;"
        return connectToMySQL('dojosandninjas').query_db(query,data)
        

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM ninjas WHERE id = %(id)s;"
        return connectToMySQL('dojosandninjas').query_db(query,data)