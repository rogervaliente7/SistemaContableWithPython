from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.auth import login_required
from .models import Tercero
from .models import TipoTercero

bp = Blueprint('terceros', __name__, url_prefix='/terceros')

@bp.route('/')
@login_required
def index():
	terceros = Tercero.query.all()
	return render_template('terceros/index.html', terceros = terceros)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		nombre = request.form['nombre']
		direccion = request.form['direccion']
		telefono = request.form['telefono']
		email = request.form['email']
		id_tipo_tercero = int(request.form['id_tipo_tercero'])

		tercero = Tercero(nombre, direccion, telefono, email, id_tipo_tercero)

		db.session.add(tercero)
		db.session.commit()
		flash('Tercero creado correctamente')
		return redirect(url_for('terceros.index'))
	tipo_terceros = TipoTercero.query.all()
	return render_template('/terceros/create.html', tipo_terceros = tipo_terceros)

@bp.route('/update/<int:id_tercero>', methods = ('GET', 'POST'))
@login_required
def update(id_tercero):
	tercero = Tercero.query.get_or_404(id_tercero)
	if request.method == 'POST':
		tercero.nombre = request.form['nombre']
		tercero.direccion = request.form['direccion']
		tercero.telefono = request.form['telefono']
		tercero.email = request.form['email']
		tercero.id_tipo_tercero = int(request.form['id_tipo_tercero'])

		db.session.commit()
		flash('Tercero modificado correctamente')
		return redirect(url_for('terceros.index'))
	tipo_terceros = TipoTercero.query.all()
	return render_template('/terceros/update.html', tipo_terceros = tipo_terceros, tercero = tercero)

@bp.route('/delete/<id_tercero>')
@login_required
def delete(id_tercero):
	tercero = Tercero.query.get_or_404(id_tercero)
	db.session.delete(tercero)
	db.session.commit()
	flash('Tercero eliminado correctamente')
	return redirect(url_for('terceros.index'))

@bp.route('/get')
@login_required
def get():
	terceros = Tercero.query.all()
	lista_terceros = []
	for tercero in terceros:
		lista_terceros.append(tercero.serialize())
	return jsonify(lista_terceros)