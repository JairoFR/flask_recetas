from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.receta import Receta


@app.route("/recetas")
def recetas():
    recetas = Receta.get_all()
    return render_template('recetas.html', recetas=recetas)

@app.route("/recipes/new", methods=["GET", "POST"])
def new_recipes():

    if request.method == "GET":
        return render_template('add_recipes.html')
    
    if request.method == "POST":
        
        data={
            'nombre': request.form['nombre'],
            'usuario_creador': session['usuario_id'],
            'descripcion': request.form['descripcion'],
            'instruccion': request.form['instruccion'],
            'fecha_cocinado': request.form['fecha_cocinado'],
            'tiempo': request.form['tiempo']
        }
        if not Receta.validar_new_recipes(data):
            return redirect('/recipes/new')

        if not Receta.save(data):
            flash(f'error en el registro', 'error')
            return redirect('/recipes/new')

        return redirect("/recetas")
    
@app.route('/recipes/<int:id>')
def show_recipes(id):
    receta = Receta.get_by_id(id)
    return render_template('show_recipes.html', recetas=receta)

@app.route('/delete_recipes/<int:id>')
def delete_recipes(id):
    Receta.destroy(id)
    return redirect('/recetas')

@app.route('/recipes/edit/<int:id>', methods=["GET", "POST"])
def edit_recipes(id):
    if request.method == "GET":
        receta = Receta.get_by_id(id)
        return render_template('edit_recipes.html', recetas=receta)
    
    if request.method == "POST":
        
        data={
            'id': id,
            'nombre': request.form['nombre'],
            'usuario_creador': session['usuario_id'],
            'descripcion': request.form['descripcion'],
            'instruccion': request.form['instruccion'],
            'fecha_cocinado': request.form['fecha_cocinado'],
            'tiempo': request.form['tiempo']
        }
        if not Receta.validar_new_recipes(data):
            return redirect(f'/recipes/edit/{id}')

        Receta.update(data)
        return redirect("/recetas")