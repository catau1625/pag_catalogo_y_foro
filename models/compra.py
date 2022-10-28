from foro_perfumes.models.modelo_base import ModeloBase
from config.mysqlconnection import connectToMySQL
from flask import flash
from utils.regex import REGEX_CORREO_VALIDO, REGEX_PASSWORD_SEGURA
import os

class Compra(ModeloBase):
    
    modelo = 'compras'
    campos = ['usuario_id','bolsa_id','direccion_id']
    
    def __init__(self,data):
        self.usuario_id = data['usuario_id']
        self.bolsa_id = data['bolsa_id']
        self.direccion_id = data['direccion_id']
        self.productos = []
        
    