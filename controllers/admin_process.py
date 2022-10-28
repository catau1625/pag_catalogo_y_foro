import re
from __init__ import app,bcrypt
from flask import render_template,flash,session,redirect,request,jsonify
from utils.utils import download_file
from models import admin,producto
from utils.utils import allowed_file
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime

# PAGINAS DE ADMIN
@app.route('/admin')
def admin_inicio():
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        return render_template('super_user.html',datos=1,super_user=1)
    else:
        flash('Error','error')
        return redirect('/')

# PROCESO AGREGAR SUSCRIPCION
@app.route('/agregar/suscripcion/process',methods=['POST'])
def agregar_suscripcion_process():
    data = {
        "tipo": request.form['tipo'],
        "precio": request.form['precio']
    }
    admin.Admin.agregar_suscripcion(data)
    flash('Suscripcion agregada correctamente','success')
    return redirect('/admin')

# PROCESO AGREGAR PRODUCTO
@app.route('/agregar/producto')
def agregar_producto():
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        return render_template('agregar_producto.html', datos=1,super_user=1)
    else:
        flash('Error','error')
        return redirect('/')

@app.route('/agregar/producto/process', methods=['GET', 'POST'])
def agregar_producto_process():
    if request.method == 'GET':
        return flash('Something went wrong','error')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No hay archivos','error')
            return redirect('/admin')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No hay archivos seleccionados','error')
            return redirect('/admin')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Archivo cargado correctamente','success')
            data = {
                "categoria": request.form['categoria']
            }
            if not admin.Admin.existe_categoria(data):
                num = admin.Admin.total_categorias()
                new_data = {
                    "categoria": request.form['categoria'],
                    "id": num+1
                }
                admin.Admin.agregar_categoria(new_data)
                flash('Categoria creada','success')
                id = admin.Admin.categoria_id(data)
                data_producto = {
                    "nombre": request.form['nombre'],
                    "descripcion": request.form['descripcion'],
                    "precio": request.form['precio'],
                    "categoria_id": id
                }
                admin.Admin.agregar_producto(data_producto)
                flash('Producto agregado sin errores','success')
                return redirect('/admin')
            else:
                id = admin.Admin.categoria_id(data)
                data_producto = {
                    "nombre": request.form['nombre'],
                    "descripcion": request.form['descripcion'],
                    "precio": request.form['precio'],
                    "categoria_id": id
                }
                admin.Admin.agregar_producto(data_producto)
                flash('Producto agregado sin errores','success')
                return redirect('/admin')
            
# INICIO PRODUCTOS
@app.route('/insumos')
def insumos():
    data_envases = {
        "categoria": 'envase'
    }
    data_aceites_esenciales = {
        "categoria": 'aceite_esencial'
    }
    data_capsulas = {
        "categoria": 'capsula'
    }
    data_pastilleros = {
        "categoria": 'pastillero'
    }
    id_pastilleros = admin.Admin.categoria_id(data_pastilleros)
    data_id_pastilleros = {
        "categoria_id": id_pastilleros
    }
    id_envases = admin.Admin.categoria_id(data_envases)
    data_id_envases = {
        "categoria_id": id_envases
    }
    id_aceites_esenciales = admin.Admin.categoria_id(data_aceites_esenciales)
    data_id_aceites_esenciales = {
        "categoria_id": id_aceites_esenciales
    }
    id_capsulas = admin.Admin.categoria_id(data_capsulas)
    data_id_capsulas = {
        "categoria_id": id_capsulas
    }
    pastilleros = admin.Admin.productos_por_categoria_id(data_id_pastilleros)
    envases = admin.Admin.productos_por_categoria_id(data_id_envases)
    aceites_esenciales = admin.Admin.productos_por_categoria_id(data_id_aceites_esenciales)
    capsulas = admin.Admin.productos_por_categoria_id(data_id_capsulas)
    if 'user_id' in session:
        if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
            return render_template('productos.html',datos=1,
                               envases = envases,
                               aceites_esenciales = aceites_esenciales,
                               capsulas = capsulas,
                               pastilleros = pastilleros,
                               super_user=1)
        return render_template('productos.html',datos=1,
                               envases = envases,
                               aceites_esenciales = aceites_esenciales,
                               capsulas = capsulas,
                               pastilleros = pastilleros,
                               super_user=0)
    return render_template('productos.html',datos=0,
                           envases = envases,
                           aceites_esenciales = aceites_esenciales,
                           capsulas = capsulas,
                           pastilleros = pastilleros,
                           super_user=0)
    
@app.route('/producto/<int:producto_id>')
def show_producto_by_id(producto_id):
    data = {
        "id": producto_id
    }
    producto = admin.Admin.producto_by_id(data)
    if 'user_id' in session:
        if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
            return render_template('un_producto.html',datos=1,super_user=1,producto=producto)
        return render_template('un_producto.html',datos=1,super_user=0,producto=producto)
    return render_template('un_producto.html',datos=0,super_user=0,producto=producto)

# FORM AGREGAR SUSCCRIPCION
@app.route('/agregar/suscripcion')
def agregar_suscripcion():
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        return render_template('agregar_suscripcion.html',datos=1,super_user=1)
    else:
        flash('Error','error')
        return redirect('/')
    
# MODIFICAR/ELIMINAR SUSCRIPCION
@app.route('/modificar/suscripcion')
def modificar_suscripcion():
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        suscripciones = admin.Admin.mostrar_suscripciones()
        return render_template('modificar_suscripcion_select.html',datos=1,super_user=1,suscripciones=suscripciones)
    else:
        return redirect('/')
    
@app.route('/modificar/suscripcion/select',methods=['POST'])
def modificar_suscripcion_select():
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        data = {
            "id": request.form['suscripcion_editable']
        }
        suscripcion = admin.Admin.mostrar_suscripcion_id(data)
        return render_template('modificar_suscripcion_form.html',datos=1,super_user=1,suscripcion=suscripcion)
    else:
        return redirect('/')
    
@app.route('/modificar/suscripcion/process',methods=['POST'])
def modificar_suscripcion_process():
    data = {
        "id": request.form['id'],
        "tipo": request.form['new_tipo'],
        "precio": request.form['new_precio']
    }
    admin.Admin.actualizar_suscripcion(data)
    flash('Información actualizada','info')
    return redirect('/admin')

# 
@app.route('/modificar/producto')
def modificar_producto():
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        categorias = admin.Admin.mostrar_categorias()
        return render_template('modificar_producto_select.html',datos=1,super_user=1,categorias=categorias)
    else:
        return redirect('/')

@app.route('/modificar/producto/form',methods=['POST'])
def modificar_producto_select2():
    data = {
        "id": request.form['producto_id']
    }
    producto = admin.Admin.producto_by_id(data)
    categorias = admin.Admin.mostrar_categorias()
    return render_template('modificar_producto_form.html',datos=1,super_user=1,producto=producto,categorias=categorias)

@app.route('/modificar/producto/process',methods=['POST'])
def modificar_producto_process():
    data = {
        "id": request.form['id'],
        "nombre": request.form['new_nombre'],
        "descripcion": request.form['new_descripcion'],
        "precio": request.form['new_precio'],
        "categoria_id": request.form['new_categoria_id']
    }
    producto.Producto.actualizar_producto(data)
    flash('Producto actualizado sin errores','success')
    return redirect('/admin')

@app.route('/eliminar/suscripcion/<int:suscripcion_id>')
def eliminar_suscripcion(suscripcion_id):
    data = {
        "suscripcion_id": suscripcion_id
    }
    admin.Admin.eliminar_suscripcion(data)
    flash('Suscripcion eliminada','success')
    return redirect('/admin')

@app.route('/eliminar/producto/<int:producto_id>')
def eliminar_producto(producto_id):
    data = {
        "producto_id": producto_id
    }
    producto.Producto.eliminar_producto(data)
    flash('Producto eliminado','success')
    return redirect('/admin')

@app.route('/agregar/tema')
def agregar_tema():
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        return render_template('agregar_tema.html',datos=1,super_user=1)
    flash('Error','error')
    return redirect('/')

@app.route('/agregar/tema/process', methods=['GET', 'POST'])
def agregar_tema_process():
    if request.method == 'GET':
        return flash('Something went wrong','error')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No hay archivos','error')
            return redirect('/admin')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No hay archivos seleccionados','error')
            return redirect('/admin')
        if file and allowed_file(file.filename):
            filename = f"{int(datetime.utcnow().timestamp())}{secure_filename(file.filename)}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Archivo cargado correctamente','success')
            data = {
                "titulo": request.form['titulo'],
                "descripcion": request.form['descripcion'],
                "nombre_portada": filename
            }
            admin.Admin.agregar_tema(data)
            flash('Tema agregado','success')
            return redirect('/admin')

@app.route('/todos/productos/<int:categoria_id>')
def todos_productos(categoria_id):
    data = {
        "categoria_id": categoria_id
    }
    productos = admin.Admin.productos_por_categoria_id(data)
    print(productos)
    productos_lista = []
    for item in productos:
        item_data = {
            "id": item.id,
            "nombre": item.nombre,
            "decripcion": item.descripcion,
            "precio": item.precio,
            "categoria_id": item.categoria_id
        }
        productos_lista.append(item_data)
    return jsonify(productos_lista)

@app.route('/modificar/tema')
def modificar_tema():
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        temas = admin.Admin.mostrar_temas()
        return render_template('modificar_temas.html',datos=1,super_user=1,temas=temas)
    flash('Error','error')
    return redirect('/')

@app.route('/modificar/tema/form',methods=['POST'])
def modificar_tema_form():
    data = {
        "id": request.form['categoria_id']
    }
    tema = admin.Admin.tema_by_id(data)
    return render_template('modificar_tema_form.html',datos=1,super_user=1,tema=tema)

@app.route('/modificar/tema/process',methods=['POST'])
def modificar_tema_process():
    data = {
        "id": request.form['id'],
        "titulo": request.form['new_titulo'],
        "descripcion": request.form['new_descripcion'],
        "nombre_portada": request.form['new_nombre_portada']
    }
    admin.Admin.actualizar_tema(data)
    flash('Tema actualizado sin errores','success')
    return redirect('/admin')

@app.route('/eliminar/tema/<int:tema_id>')
def eliminar_tema_by_id(tema_id):
    data = {
        "id": tema_id
    }
    admin.Admin.eliminar_tema(data)
    flash('Tema eliminado sin errores','success')
    return redirect('/admin')
               
