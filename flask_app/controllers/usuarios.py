from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usuario import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/recetas')

    return render_template("login.html")

@app.route('/registrar', methods=['POST'])
def registrar():


    datos = {
        'nombre' : request.form['nombre'],
        'apellido' : request.form['apellido'],
        'email' : request.form['email']
    }

    dato ={
        'password' : request.form['password'],
        'cpassword' : request.form['cpassword'],
        'email' : request.form['email']
    }
    if not User.validar(datos):
        return redirect('/')

    if  not User.validar_pass(dato):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    resultado = User.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/")

    flash("Usuario creado correctamente", "success")
    return redirect('/')



@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = User.get_by_email(request.form['identificacion'])

    if not usuario:
        flash("Correo/Clave Invalidas", "error")
        return redirect("/")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Correo/Clave Invalidas", "error")
        return redirect("/")
    

    session['usuario'] = usuario.nombre
    session['usuario_id'] = usuario.id

    return redirect('/recetas')

@app.route('/logout')
def logout():
    session.clear()
    flash("Vuelve pronto", "success")
    return redirect('/')



#EDITAR
@app.route('/users/<int:id>', methods=['GET', 'POST'])
def editar_users(id): 

    if request.method == 'GET':

        users = User.get_by_id(id)
        # magazine= Magazine.get_all_id(id)
        # return render_template('edit.html', users=users, magazine=magazine)
    
    if request.method == 'POST':

        data = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'email': request.form['email'],
            'id': session['usuario_id']

        }
    print(request.form)

    if not User.validar(data):
        return redirect(f'/users/{id}')

    User.update(data)
    return redirect('/dashboard')