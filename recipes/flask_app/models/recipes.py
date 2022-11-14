from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Recipe:
    db='recipe_schema'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_min = data['under_30_min']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data ['updated_at']
        self.user=None

    @staticmethod
    def validate_recipe(data):
        is_valid=True
        if len(data.get('name'))<=3:    
            flash('Name needs at least 3 letters')
            is_valid=False
        if len(data.get('description'))<=3:  
            flash('Descriptions needs at least 3 letters')  
            is_valid=False
        if len(data.get('instructions'))<=3:    
            flash('Instructions need at least 3 letters')
            is_valid=False
            
            print(f'''
        name is: {data.get("name")}
        band is:{data.get("description")}
        ''')
        return is_valid

#Create

    # @classmethod
    # def get_all_recipes(cls):
    #     query = "SELECT * FROM recipes;"
    #     results= connectToMySQL ('recipe_schema').query_db(query)
    #     all_recipes=[]
    #     for recipe in results:
    #         all_recipes.append(cls(recipe))
    #     return all_recipes

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN user ON user.id = recipes.user_id;"
        recipe_data = connectToMySQL ('recipe_schema').query_db(query)
        print('A')
        all_recipes=[]
        
        for recipe_all in recipe_data:

            recipe_obj = cls(recipe_all)
        
            recipe_obj.user = user.User(
                {
                    "id":recipe_all['user.id'],
                    "first_name":recipe_all['first_name'],
                    "last_name":recipe_all['last_name'],
                    "email":recipe_all['email'],
                    "password": '',
                    "created_at":recipe_all['user.created_at'],
                    "updated_at":recipe_all['user.updated_at']
                }
            )
            all_recipes.append(recipe_obj)
        return all_recipes  

    @classmethod
    def create_recipe(cls,data):
        query ="""INSERT INTO recipes (name, description, instructions, under_30_min, date_cooked, user_id) 
            VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30_min)s, %(date_cooked)s, %(user_id)s);"""
        return (connectToMySQL(cls.db).query_db(query,data))

    # @classmethod
    # def get_by_id_recipe(cls,data):
    #     query = "SELECT * FROM recipes WHERE id = %(id)s;"
    #     result = connectToMySQL('recipe_schema').query_db(query,data)
    #     return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, updated_at=NOW() WHERE id= %(id)s;"
        return connectToMySQL('recipe_schema').query_db(query,data)

    @classmethod
    def get_recipe_by_id(cls,data):
        
        query = "SELECT * FROM recipes JOIN user ON user.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result = connectToMySQL ('recipe_schema').query_db(query,data)
        print('A')
        result = result[0]
        recipe = cls(result) 
        
        recipe.user = user.User(
            {
                "id":result['user.id'],
                "first_name":result['first_name'],
                "last_name":result['last_name'],
                "email":result['email'],
                "password": '',
                "created_at":result['user.created_at'],
                "updated_at":result['user.updated_at']
            }
        )

        return recipe   

    @classmethod
    def delete(cls,id):
        data = {"id":id}
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipe_schema').query_db(query,data)