from config.mysqlconnection import connectToMySQL
from flask import flash
from models.modelo_base import ModeloBase
from models import producto
from utils.regex import REGEX_CORREO_VALIDO, REGEX_PASSWORD_SEGURA

class Admin(ModeloBase):
        
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.nombre_usuario = data['nombre_usuario']
        self.email = data['email']
        self.password = data['password']
        self.suscripcion_id = 1
        
    @classmethod
    def agregar_suscripcion(cls,data):
        query = "INSERT INTO suscripciones (tipo,precio,created_at,updated_at) VALUES (%(tipo)s,%(precio)s,NOW(),NOW());"
        return connectToMySQL('esquema_perfumes').query_db(query,data)

    @classmethod
    def eliminar_suscripcion(cls,data):
        query = "DELETE FROM suscripciones WHERE id=%(suscripcion_id)s;"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def mostrar_suscripciones(cls):
        query = "SELECT * FROM suscripciones;"
        results = connectToMySQL('esquema_perfumes').query_db(query)
        suscripciones = []
        for info in results:
            susc_info = {
                "id": info['id'],
                "tipo": info['tipo'],
                "precio": info['precio']
            }
            suscripciones.append(susc_info)
        return suscripciones
    
    @classmethod
    def mostrar_suscripcion_id(cls,data):
        query = "SELECT * FROM suscripciones WHERE id = %(id)s;"
        results = connectToMySQL('esquema_perfumes').query_db(query,data)
        suscripcion = []
        for info in results:
            suscripcion_data = {
                "id": info['id'],
                "tipo": info['tipo'],
                "precio": info['precio']
            }
            suscripcion.append(suscripcion_data)
        return suscripcion[0]
    
    @classmethod
    def actualizar_suscripcion(cls,data):
        query = "UPDATE suscripciones SET tipo = %(tipo)s, precio = %(precio)s WHERE id = %(id)s;"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def agregar_categoria(cls,data):
        query = "INSERT INTO categorias (id,tipo) VALUES (%(id)s,%(categoria)s);"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def existe_categoria(cls,data):
        query = "SELECT tipo FROM categorias where tipo=%(categoria)s;"
        results = connectToMySQL('esquema_perfumes').query_db(query,data)
        if results:
            return True
        else:
            return False
    
    @classmethod
    def total_categorias(cls):
        query = "SELECT COUNT(*) AS total FROM categorias;"
        results = connectToMySQL('esquema_perfumes').query_db(query)
        return int(results[0]['total'])
    
    @classmethod
    def categoria_id(cls,data):
        query = "SELECT categorias.id FROM categorias WHERE tipo = %(categoria)s;"
        results = connectToMySQL('esquema_perfumes').query_db(query,data)
        if not results:
            return False
        return results[0]['id']
    
    @classmethod
    def mostrar_categorias(cls):
        query = "SELECT * FROM categorias;"
        results = connectToMySQL('esquema_perfumes').query_db(query)
        categorias = []
        for info in results:
            results_data = {
                "id": info['id'],
                "tipo": info['tipo']
            }
            categorias.append(results_data)
        return categorias
    
    @classmethod
    def agregar_producto(cls,data):
        query = "INSERT INTO productos (nombre,descripcion,precio,created_at,updated_at,categoria_id) VALUES (%(nombre)s,%(descripcion)s,%(precio)s,NOW(),NOW(),%(categoria_id)s);"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def productos_por_categoria_id(cls,data):
        query = "SELECT * FROM productos JOIN categorias ON productos.categoria_id = categorias.id WHERE categorias.id = %(categoria_id)s;"
        results = connectToMySQL('esquema_perfumes').query_db(query,data)
        productos_encontrados = []
        if not results:
            return False
        for info in results:
            producto_data = {
                "id": info['id'],
                "nombre": info['nombre'],
                "descripcion": info['descripcion'],
                "precio": info['precio'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at'],
                "categoria_id": info['categoria_id']
            }
            productos_encontrados.append(producto.Producto(producto_data))
        return productos_encontrados
    
    @classmethod
    def producto_by_id(cls,data):
        query = "SELECT * FROM productos WHERE id = %(id)s;"
        results = connectToMySQL('esquema_perfumes').query_db(query,data)
        prod_final = []
        for info in results:
            prod_data = {
                "id": info['id'],
                "nombre": info['nombre'],
                "descripcion": info['descripcion'],
                "precio": info['precio'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at'],
                "categoria_id": info['categoria_id']
            }
            prod_final.append(producto.Producto(prod_data))
        return prod_final[0]
    
    @classmethod
    def agregar_tema(cls,data):
        query = "INSERT INTO temas (titulo,descripcion,nombre_portada) VALUES (%(titulo)s,%(descripcion)s,%(nombre_portada)s);"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def mostrar_temas(cls):
        query = "SELECT * FROM temas;"
        results = connectToMySQL('esquema_perfumes').query_db(query)
        temas = []
        for info in results:
            tema_data = {
                "id": info['id'],
                "titulo": info['titulo'],
                "descripcion": info['descripcion'],
                "nombre_portada": info['nombre_portada']
            }
            temas.append(tema_data)
        return temas
    
    @classmethod
    def tema_by_id(cls,data):
        query = "SELECT * FROM temas WHERE id = %(id)s;"
        results = connectToMySQL('esquema_perfumes').query_db(query,data)
        tema = []
        for info in results:
            tema_data = {
                "id": info['id'],
                "titulo": info['titulo'],
                "descripcion": info['descripcion'],
                "nombre_portada": info['nombre_portada']
            }
            tema.append(tema_data)
        return tema[0]

    @classmethod
    def actualizar_tema(cls,data):
        query = "UPDATE temas SET titulo=%(titulo)s,descripcion=%(descripcion)s,nombre_portada=%(nombre_portada)s WHERE id=%(id)s;"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    
    @classmethod
    def eliminar_tema(cls,data):
        query = "DELETE FROM temas WHERE id = %(id)s;"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    