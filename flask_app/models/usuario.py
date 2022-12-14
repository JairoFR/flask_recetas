import os
import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.base_modelo import BaseModelo
from flask_bcrypt import Bcrypt        


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User(BaseModelo): #Cambiar a nombre de modelo en singular  

    modelo = 'usuarios' #nombre de tabla
    columnas_tabla = [ 'nombre', 'apellido', 'email', 'password'] #campos de columnas sin creted_at y update_at

    def __init__( self , data ):
        self.id = data['id'] 
        self.nombre = data['nombre']
        self.apellido= data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
   
    @classmethod
    def get_by_email(cls, data):
        
        query = "SELECT * FROM usuarios WHERE  email = %(data)s"
        data = { 'data': data }
        results = connectToMySQL(os.environ.get("BASE_DATOS_NOMBRE")).query_db(query, data)
    
        # no se encontrĂ³ un usuario coincidente
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    @classmethod
    def get_by_id(cls, data):
        
        query = "SELECT * FROM usuarios WHERE  id = %(data)s"
        data = { 'data': data }
        results = connectToMySQL(os.environ.get("BASE_DATOS_NOMBRE")).query_db(query, data)

        # no se encontrĂ³ un usuario coincidente
        all_data = []

        for data in results:
            all_data.append( cls(data) )
        return all_data
    

    @classmethod
    def update(cls,data):
        query = f"UPDATE usuarios SET nombre = %(nombre)s, apellido = %(apellido)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
        resultado = connectToMySQL(os.environ.get("BASE_DATOS_NOMBRE")).query_db(query, data)
        print(resultado)
        return resultado
    

    @staticmethod
    def validar(data): 
        is_valid = True
   
        
        if len(data['nombre']) <= 3:
            flash(f'El nombre no puede ser menor a 3', 'error')
            is_valid = False

        if len(data['apellido']) < 3:
            is_valid = False
            flash("El apellido no puede ser menor a 3", 'error')

        if not EMAIL_REGEX.match(data['email']): 
            flash("Direccion de email invalida!","error")
            is_valid = False

        return is_valid

    @staticmethod
    def validar_pass(data): 
        is_valid = True

        query = "SELECT * FROM usuarios WHERE email = %(data)s;"
        dato = {'data': data['email']}
        results = connectToMySQL(os.environ.get("BASE_DATOS_NOMBRE")).query_db(query,dato) 
      

        if len(results) >= 1:
            flash("Email ya existe.","error")
            is_valid=False
        
        if data['password'] != data['cpassword']:
            is_valid = False
            flash("Las contraseĂ±as no coinciden!","error")
        
        if len(data['password']) < 8:
            is_valid = False
            flash("La contraseĂ±a debe tener minimo de 8 caracteres", 'error')

        return is_valid
