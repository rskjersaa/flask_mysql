from flask import app
from flask_app import app
from flask import render_template, redirect, request,session
from flask_app.models.user import User
from flask_app.models.recipes import Recipe
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/user', methods=["POST"])
def register():
    if not User.validate_registration(request.form):
        (print(request.form))
        return redirect('/')

    data = {
        # 'id': request.form['id'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }

    userId=User.save(data)
    session['userId'] = userId
    return redirect ('/recipes')



@app.route('/login', methods=['POST'])
def login():
        if not User.validate_login(request.form):

            return redirect('/')
        
        user=User.get_by_email(request.form)
        
        session['userId']=user.id
        return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
