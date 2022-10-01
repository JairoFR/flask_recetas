import os
import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.base_modelo import BaseModelo

class Receta(BaseModelo): #Cambiar a nombre de modelo en singular  

    modelo = 'recetas' #nombre de tabla
    columnas_tabla = [ 'usuario_creador', 'nombre', 'descripcion', 'instruccion', 'fecha_cocinado', 'tiempo'] #campos de columnas sin creted_at y update_at

    def __init__( self , data ):
        self.id = data['id'] 
        self.usuario_creador= data['usuario_creador']
        self.nombre= data['nombre']
        self.usuario= data['usuario']
        self.descripcion = data['descripcion']
        self.instruccion = data['instruccion']
        self.fecha_cocinado= data['fecha_cocinado']
        self.tiempo= data['tiempo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def get_all(cls):
        query = """SELECT recetas.*, usuarios.nombre AS usuario FROM recetas
                    JOIN usuarios ON recetas.usuario_creador = usuarios.id;"""

        results = connectToMySQL(os.environ.get("BASE_DATOS_NOMBRE")).query_db(query)
        all_data = []

        for data in results:
            all_data.append( cls(data) )
        return all_data
    
    @classmethod
    def get_by_id(cls, id):
        query = """SELECT recetas.*, usuarios.nombre AS usuario FROM recetas
                    JOIN usuarios ON recetas.usuario_creador = usuarios.id where recetas.id = %(id)s;;"""
        data = { 'id' : id }
        results = connectToMySQL(os.environ.get("BASE_DATOS_NOMBRE")).query_db(query, data)
        all_data = []

        for data in results:
            print(data)
            all_data.append( cls(data) )
        return all_data

    @staticmethod
    def validar_new_recipes(data):
        is_valid = True

        if len(data['nombre']) <= 3:
            flash(f'El nombre de la receta no puede ser menor a 3', 'error')
            is_valid = False
        
        if len(data['descripcion']) <= 3:
            flash(f'La descripcion no puede ser menor a 3', 'error')
            is_valid = False
        
        if len(data['instruccion']) <= 3:
            flash(f'La instruccion no puede ser menor a 3', 'error')
            is_valid = False
        return is_valid