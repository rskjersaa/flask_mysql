from flask_app import app
from flask import redirect, render_template, request
from flask_app.models import dojo, ninja  #ALWAYS ADD ALL CONTROLLERS
from flask_app.models.ninja import Ninja

#shows the create ninja form on page
@app.route('/ninjas')
def ninjas():
    return render_template("ninja.html", dojos=dojo.Dojo.get_all())

# route to SHOWS all ninjas and dojos table
@app.route('/dojos/')
def allNinjas():
    return render_template("dojo.html",all_dojos=dojo.Dojo.get_one())


# route to add ninja to database
@app.route('/create/ninja', methods=['POST'])
def createNinja():
    print(request.form)
    ninja.Ninja.save(request.form)
    return redirect('/')

@app.route('/edit/ninja/<int:ninja_id>/<int:dojo_id>')
def edit(ninja_id, dojo_id):
    data = {
            "id":ninja_id
    }
    ninja=Ninja.get_one(data)  
    return render_template ('editNinja.html', ninja=ninja)

# @app.route('/show/dojo/<int:id>')
# def show(id):
#     data = {
#         "id":id
#     }
#     return render_template("showDojo.html", dojo=Dojo.get_one(data))

@app.route('/update/ninja/', methods=["POST"])
def update (dojo_id):
    
    print(request.form)
    ninja.Ninja.update(request.form)
    return redirect(f'/dojo/{dojo_id}')

@app.route('/delete/ninja/<int:ninja_id>/<int:dojo_id>')
def delete(ninja_id,dojo_id):
    data = {
        'id':ninja_id
    }
    Ninja.delete(data)
    return redirect(f'/dojo/{dojo_id}')