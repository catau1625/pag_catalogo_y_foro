from models.modelo_base import ModeloBase
from config.mysqlconnection import connectToMySQL
from flask import flash
from utils.regex import REGEX_CORREO_VALIDO, REGEX_PASSWORD_SEGURA
import os

class Producto():
    
    modelo = 'productos'
    campos = ['nombre','descripcion','precio','categoria_id']
    
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.precio = data['precio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.categoria_id = data['categoria_id']
    
    @classmethod
    def actualizar_producto(cls,data):
        query = "UPDATE productos SET nombre=%(nombre)s,descripcion=%(descripcion)s,precio=%(precio)s,categoria_id=%(categoria_id)s WHERE id=%(id)s;"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def eliminar_producto(cls,data):
        query = "DELETE FROM productos WHERE id=%(producto_id)s;"
        return connectToMySQL('esquema_perfumes').query_db(query,data)