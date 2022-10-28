from models.modelo_base import ModeloBase
from config.mysqlconnection import connectToMySQL
from flask import flash
from utils.regex import REGEX_CORREO_VALIDO, REGEX_PASSWORD_SEGURA

class Usuario(ModeloBase):
    
    modelo = 'usuarios'
    campos = ['nombre','apellido','nombre_usuario','email','password','created_at','updated_at','suscripcion_id']
    
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.nombre_usuario = data['nombre_usuario']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.suscripcion_id = data['suscripcion_id']
        
    @classmethod
    def buscar(cls, data):
        query = "SELECT * FROM usuarios WHERE nombre_usuario = %(nombre_usuario)s;"
        results = connectToMySQL('esquema_perfumes').query_db(query, data)
        usuario = []
        if not results:
            return False
        for info in results:
            datos = {
                "id": info['id'],
                "nombre": info['nombre'],
                "apellido": info['apellido'],
                "nombre_usuario": info['nombre_usuario'],
                "email": info['email'],
                "password": info['password'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at'],
                "suscripcion_id": info['suscripcion_id']
            }
            usuario.append(Usuario(datos))
            print(datos,info)
        return usuario[0]
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (nombre,apellido,nombre_usuario,email,password,created_at,updated_at,suscripcion_id) VALUES (%(nombre)s,%(apellido)s,%(nombre_usuario)s,%(email)s,%(password)s,NOW(),NOW(),2);"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL('esquema_perfumes').query_db(query,data)
        users = []
        for info in results:
            datos = {
                "id": info['id'],
                "nombre": info['nombre'],
                "apellido": info['apellido'],
                "nombre_usuario": info['nombre_usuario'],
                "email": info['email'],
                "password": info['password'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at']
            }
            users.append(Usuario(datos))
        return users

    @classmethod
    def update(cls,data):
        query = """UPDATE usuarios 
                        SET nombre = %(nombre)s,
                        SET apellido = %(apellido)s,
                        SET email = %(email)s,
                        SET password = %(password)s,
                        SET nombre_usuario = %(nombre_usuario)s,
                        SET updated_at=NOW(),
                        SET suscripcion_id = %(suscripcion_id)s
                    WHERE id = %(id)s;"""
        resultado = connectToMySQL('esquema_perfumes').query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del {campo} no puede ser menor o igual {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True

        is_valid = cls.validar_largo(data, 'nombre', 3)
        is_valid = cls.validar_largo(data, 'nombre_usuario', 3)

        if not REGEX_CORREO_VALIDO.match(data['email']):
            flash('El correo no es válido', 'error')
            is_valid = False

        if not REGEX_PASSWORD_SEGURA.match(data['password']):
            flash('Contraseña débil', 'error')
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash('Las contraseñas no coinciden', 'error')
            is_valid = False

        if cls.validar_existe('nombre_usuario', data['nombre_usuario']):
            flash('Este nombre de usuario ya esta siendo usado', 'error')
            is_valid = False

        if cls.validar_existe('email', data['email']):
            flash('El correo ingresado ya está siendo usado', 'error')
            is_valid = False

        return is_valid