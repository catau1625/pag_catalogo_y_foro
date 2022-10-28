from models import producto
from models.modelo_base import ModeloBase
from config.mysqlconnection import connectToMySQL
from flask import flash

class Bolsa():   
    def __init__(self,data):
        self.id = data['id']
        self.bolsa_actual = []
        
    @classmethod
    def bolsa_actual(cls,data):
        query = """SELECT * FROM productos 
                JOIN bolsa ON productos.id = bolsa.producto_id
                WHERE bolsa.id = %(bolsa_id)s;"""
        results = connectToMySQL('esquema_perfumes').query_db(query, data)
        productos_bolsa = []
        for info in results:
            datos_productos = {
                'nombre': info['nombre'],
                'descripcion': info['descripcion'],
                'precio': info['precio'],
                'created_at': info['updated_at'],
                'updated_at': info['updated_at'],
                'categoria_id': info['categoria_id']
            }
            productos_bolsa.append(producto.Producto(datos_productos))
        return productos_bolsa
    
    @classmethod
    def bolsa_abierta(cls):
        query = "SELECT bolsa.id FROM bolsa WHERE bolsa.id NOT IN (SELECT bolsa.id FROM bolsa JOIN compras ON bolsa.id = compras.bolsa_id);"
        results = connectToMySQL('esquema_perfumes').query_db(query)
        if not results:
            return False
        return results[0]
    
    def agregar_producto_a_una_bolsa(self,data):
        query = "SELECT * FROM productos WHERE productos.id = %(producto_id)s;"
        results = connectToMySQL('esquema_perfumes').query_db(query,data)
        for info in results:
            results_data = {
                "id": info['id'],
                "nombre": info['nombre'],
                "descripcion": info['descripcion'],
                "precio": info['precio'],
                "created_at": info['created_at'],
                "updated_at": info['updated_at'],
                "categoria_id": info['categoria_id']
            }
            self.bolsa_actual.append(producto.Producto(results_data))
        return self
    
    @classmethod
    def buscar_comuna_id(cls,data):
        pass
    
    @classmethod
    def buscar_region_id(cls,data):
        pass
    
    @classmethod
    def agregar_direccion_compra(cls,data):
        query = "INSERT INTO direcciones (calle,numero,referencia,nombre_de,region_id,comuna_id) VALUES (%(calle)s,%(numero)s,%(referencia)s,%(nombre_de)s,%(region_id)s,%(comuna_id)s);"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
        
    @classmethod
    def comprar_carrito(cls,data):
        query = "INSERT INTO compras (usuario_id,bolsa_id,direccion_id) VALUES (%(usuario_id)s,%(bolsa_id)s,%(direccion_id)s);"
        return connectToMySQL('esquema_perfumes').query_db(query,data)
    