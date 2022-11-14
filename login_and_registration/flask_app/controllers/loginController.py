from flask import app
from flask_app import app
from flask import render_template, redirect, request,session
from flask_app.models.registration import Registration
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/user', methods=["POST"])
def register():
    if not Registration.validate_registration(request.form):
        (print(request.form))
        return redirect('/')

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }

    registrationId=Registration.save(data)
    session['registrationId'] = registrationId
    return redirect ('/success')

@app.route('/success')
def dashboard():
    
    if 'registrationId' not in session:
        
        return redirect('/')
    print(session['registrationId'])
    data = {
        "id": session['registrationId']

    }
    user=Registration.getById(session['registrationId'])

    return render_template('success.html',user=user)


@app.route('/login', methods=['POST'])
def login():
        if not Registration.validate_login(request.form):
            # flash("Invalid Email","login")
            return redirect('/')
        # if not bcrypt.check_password_hash(registration.password,request.form['password']):
        #     flash('invalid email or password', 'login')
        #     return redirect('/')
        registrationId=Registration.getByEmail(request.form)
        print("controller" +registrationId ['email'])
        session['registrationId']=registrationId ['id']
        return redirect('/success')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
