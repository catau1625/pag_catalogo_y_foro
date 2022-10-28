from flask import redirect, render_template, request, flash, session
from flask_base import app
from flask_base.models.viaje import Viaje
from flask import jsonify

@app.route("/viajes")
def viajes():
    return render_template('viajes/viajes.html', viajes=Viaje.get_all())

@app.route("/viajes_mios")
def viajes_mios():
    usuario = session['usuario_id']
    viajes =Viaje.get_all_by_user(usuario)
    return render_template('viajes/viajes_mios.html', viajes=viajes)

@app.route("/viajes_agregar")
def viajes_add():
    return render_template('viajes/viajes_add.html')

@app.route("/viajes/agregar/procesar", methods=["POST"])
def viajes_agregar():
    
    if Viaje.validar_existe('destino', request.form['destino']):
        flash('Lamentablemente ya tienes este destino', 'error')
        return redirect('/viajes_agregar')

    if not Viaje.validar(request.form):
        return redirect('/viajes_agregar')

    print("POR POST:", request.form)
    data = {
        'destino': request.form['destino'],
        'fecha': request.form['fecha'],
        'usuario_creador': session['usuario_id']
    }

    resultado = Viaje.save(data)

    if resultado:    
        flash("Viaje agregado con exito", 'success')
        return redirect('/viajes')
    else:
        flash('Lamentablemente ocurrió un problema', 'error')
        return redirect('/viajes_agregar')

@app.route("/viajes/eliminar/<id>")
def viajes_eliminar(id):
    viaje = Viaje.get_by_id(id)
    if viaje and viaje.usuario_creador == session['usuario_id']:
        Viaje.delete(id)
        flash("Viaje eliminado con exito", 'success')
    else:
        flash('Este no es tu viaje o viaje no existe', 'error')

    return redirect('/viajes')


@app.route("/api/viajes/eliminar/<id>")
def api_eliminar_viaje(id):
    viaje = Viaje.get_by_id(id)
    errores = ""
    is_valid = True
    if viaje and viaje.usuario_creador == session['usuario_id']:
        Viaje.delete(id)
        mensaje = "Viaje eliminado con exito"
    else:
        errores = 'Este no es tu viaje o viaje no existe'
        is_valid = False

    resultado={
        'ok': is_valid,
        'errores': errores,
        'mensaje': mensaje,
    }

    return jsonify(resultado)