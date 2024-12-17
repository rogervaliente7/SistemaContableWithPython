from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.auth import login_required
from .models import TipoTercero

bp = Blueprint('tipo_terceros', __name__, url_prefix='/terceros/tipos')

@bp.route('/')
def index():
	tipo_terceros = TipoTercero.query.all()
	return render_template('/terceros/tipos/index.html', tipo_terceros = tipo_terceros)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		nombre = request.form['nombre']

		tipo_tercero = TipoTercero(nombre)

		db.session.add(tipo_tercero)
		db.session.commit()
		flash('Tipo de tercero creado correctamente')
		return redirect(url_for('tipo_terceros.index'))
	return render_template('/terceros/tipos/create.html')

@bp.route('/update/<id_tipo_tercero>', methods = ('GET', 'POST'))
@login_required
def update(id_tipo_tercero):
	tipo_tercero = TipoTercero.query.get_or_404(id_tipo_tercero)
	if request.method == 'POST':
		tipo_tercero.nombre = request.form['nombre']

		db.session.commit()
		flash('Tipo de tercero modificado correctamente')
		return redirect(url_for('tipo_terceros.index'))
	return render_template('/terceros/tipos/update.html', tipo_tercero = tipo_tercero)

@bp.route('/delete/<id_tipo_tercero>')
@login_required
def delete(id_tipo_tercero):
	tipo_tercero = TipoTercero.query.get_or_404(id_tipo_tercero)
	db.session.delete(tipo_tercero)
	db.session.commit()
	flash('Tipo de tercero eliminado correctamente')
	return redirect(url_for('tipo_terceros.index'))

@bp.route('/get')
@login_required
def get():
	tipo_terceros = TipoTercero.query.all()
	lista_tipo_terceros = []
	for tipo_tercero in tipo_terceros:
		lista_tipo_terceros.append(tipo_tercero.serialize())
	return jsonify(lista_tipo_terceros)