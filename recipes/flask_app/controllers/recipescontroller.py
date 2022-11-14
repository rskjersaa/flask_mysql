from flask import app
from flask_app import app
from flask import render_template, redirect, request,session
from flask_app.models.user import User
from flask_app.models.recipes import Recipe
from flask import flash

@app.route('/recipes')
def dashboard():
    
    if 'userId' not in session:
        flash("You must be logged in to proceed")
        return redirect('/')
    print(session['userId'])
    data = {
        "id": session['userId']
    }
    user=User.get_by_id(data)

    return render_template('recipes.html',user=user,recipes=Recipe.get_all_recipes())


@app.route ('/create-recipe')
def r_create_recipe():
    if 'userId' not in session:
        flash("You must be logged in to proceed")
        return redirect('/')
    print(session['userId'])
    data = {
        "id": session['userId']
    }
    user=User.get_by_id(data)
    return render_template ('new_recipes.html', user=user,recipes=Recipe.get_all_recipes())

@app.route('/create_recipe', methods=["POST"])
def f_create_recipe():
    if not Recipe.validate_recipe(request.form):
        (print(request.form))
        return redirect('/create-recipe')
    Recipe.validate_recipe(request.form)
    new_recipe= {
        "name": request.form['name'],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_30_min": request.form["under_30_min"],
        "user_id": session["userId"]
    }
    session['userId']
    Recipe.create_recipe(new_recipe)
    return redirect ('/recipes')

@app.route ('/recipes/edit/<int:recipe_id>')
def r_edit_recipe(recipe_id):
    data ={
        "id" : recipe_id
    }
    print(data)
    recipe=Recipe.get_recipe_by_id(data)
    
    return render_template ('edit_recipes.html', recipe=recipe, user=User.get_by_id)

@app.route('/recipes/update/<int:recipe_id>', methods=["POST"])
def f_edit_recipe(recipe_id):
    valid_recipe =Recipe.validate_recipe(request.form)
    if not valid_recipe:
        return redirect(f'/recipes/edit/{recipe_id}')
    Recipe.update(request.form)
    return redirect ('/recipes')


@app.route('/recipes/view/<int:recipe_id>')
def r_view_recipe(recipe_id):
    data ={
        "id" : recipe_id
    }
    user_data = {
        "id" :session['userId']
    }
    user=User.get_by_id(user_data)
    recipe=Recipe.get_recipe_by_id(data)
    return render_template('view_recipes.html', user=user, recipe=recipe)

@app.route('/recipes/delete/<int:recipe_id>')
def delete_by_id(recipe_id):
    Recipe.delete(recipe_id)
    return redirect('/recipes')