from __init__ import app, bcrypt
from flask import render_template,session,flash,redirect,request,url_for
from models import usuario, admin

# PAGINA DE INICIO
@app.route('/')
def inicio():
    if 'user_id' not in session:
        return render_template('inicio.html',datos=0,super_user=0)
    else:
        if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
            return render_template('inicio.html',datos=1,super_user=1)
        return render_template('inicio.html',datos=1,super_user=0)

# LOGIN
@app.route('/login')
def login():
    if 'user_id' in session:
        flash('Ya hay una sesión iniciada','info')
        return redirect('/')
    suscripciones = admin.Admin.mostrar_suscripciones()
    return render_template('login.html',suscripciones=suscripciones)

# CERRAR SESION
@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión finalizada','info')
    return redirect('/')

# PROCESO DATOS REGISTRO USUARIO
@app.route('/registro/process',methods=['POST'])
def registro_process():
    if not usuario.Usuario.validar(request.form):
        return redirect('/login')
    if request.form['password'] == request.form['confirm_password']:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
    else:
        flash('Las contraseñas no coinciden','error')
        return redirect('/login')
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "nombre_usuario": request.form['nombre_usuario'],
        "email": request.form['email'],
        "password": pw_hash,
        "suscripcion_id": request.form['suscripcion']
    }
    usuario.Usuario.save(data)
    flash('Usuario creado correctamente','success')
    return redirect('/login')

# PROCESO DATOS LOGIN USUARIO
@app.route('/login/process',methods=['POST'])
def login_process():
    data = {
        "nombre_usuario": request.form['nombre_usuario']
    }
    user_data = usuario.Usuario.buscar(data)
    if not user_data:
        flash('Usuario invalido','error')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_data.password,request.form['password']):
        flash('Usuario/Contraseña invalidos','error')
        return redirect('/login')
    session['user_id'] = user_data.id
    session['user_nombre'] = user_data.nombre
    session['user_apellido'] = user_data.apellido
    session['user_nombre_usuario'] = user_data.nombre_usuario
    session['user_email'] = user_data.email
    session['user_suscripcion'] = user_data.suscripcion_id
    if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
        return redirect('/admin')
    flash('Sesión iniciada','success')
    return redirect('/')


# INICIO FORO
@app.route('/foro')
def foro():
    temas = admin.Admin.mostrar_temas()
    if 'user_id' in session:
        if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
            return render_template('foro_tema.html',datos=1,super_user=1,temas=temas)
        return render_template('foro_tema.html',datos=1,super_user=0,temas=temas)
    return render_template('foro_tema.html',datos=0,super_user=0,temas=temas)

# PAGINA DE POSTS DE ALGUN TEMA SELECCIONADO
@app.route('/foro/tema')
def foro_tema():
    if 'user_id' in session:
        if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
            return render_template('foro_post_todos.html',datos=1,super_user=1)
        return render_template('foro_post_todos.html',datos=1,super_user=0)
    return render_template('foro_post_todos.html',datos=0,super_user=0)

# PAGINA DE ALGUN POST SELECCIONADO
@app.route('/foro/post')
def foro_post():
    if 'user_id' in session:
        if session['user_nombre_usuario'] == 'cata.ubilla00@gmail.com':
            return render_template('foro_post_uno.html',datos=1,super_user=1)
        return render_template('foro_post_uno.html',datos=1,super_user=0)
    return render_template('foro_post_uno.html',datos=0,super_user=0)




