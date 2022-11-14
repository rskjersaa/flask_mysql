from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from .ninja import Ninja

class Dojo:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_At']
        self.updated_at = data ['updated_At']
        self.ninjas = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('dojosandninjas').query_db(query)
        dojos = []
        pprint(results,sort_dicts=False, width=1)
        for i in results:
            dojos.append(cls(i))
        return dojos

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        result = connectToMySQL ('dojosandninjas').query_db(query, data)
        return result

    @classmethod
    def get_one_with_ninja(cls,data):
        # query = "SELECT * FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s;"
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s;"
        results = connectToMySQL ('dojosandninjas').query_db(query,data)
        print('A')
        pprint(results,sort_dicts=False, width=1)
        dojo = cls(results[0]) 
        for row_in_db in results:
            if row_in_db ['ninjas.id'] == None:
                return dojo
            ninja_data = {
                "id":row_in_db['ninjas.id'],
                "first_name":row_in_db['first_name'],
                "last_name":row_in_db['last_name'],
                "age":row_in_db['age'],
                "created_At":row_in_db['ninjas.created_At'],
                "updated_At":row_in_db['ninjas.updated_At']
            }
            dojo.ninjas.append(Ninja(ninja_data))
        print(dojo.ninjas)
        return dojo