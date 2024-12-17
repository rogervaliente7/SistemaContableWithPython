from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.auth import login_required
from .models import CatalogoCuentas

bp = Blueprint('catalogo_cuentas', __name__, url_prefix='/cuentas/catalogo')

@bp.route('/')
@login_required
def index():
	catalogo_cuentas = CatalogoCuentas.query.all()
	return render_template('/cuentas/catalogo/index.html', catalogo_cuentas = catalogo_cuentas)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		cod_cuenta = request.form['cod_cuenta']
		nombre = request.form['nombre']

		cuenta = CatalogoCuentas(cod_cuenta, nombre)

		db.session.add(cuenta)
		db.session.commit()
		flash('Tipo de cuenta creada correctamente')
		return redirect(url_for('catalogo_cuentas.index'))
	return render_template('/cuentas/catalogo/create.html')

@bp.route('/update/<cod_cuenta>', methods = ('GET', 'POST'))
@login_required
def update(cod_cuenta):
	cuenta = CatalogoCuentas.query.get_or_404(cod_cuenta)
	if request.method == 'POST':
		cuenta.nombre = request.form['nombre']

		db.session.commit()
		flash('Tipo de cuenta modificada correctamente')
		return redirect(url_for('catalogo_cuentas.index'))
	return render_template('/cuentas/catalogo/update.html', cuenta = cuenta)

@bp.route('/delete/<cod_cuenta>')
@login_required
def delete(cod_cuenta):
	cuenta = CatalogoCuentas.query.get_or_404(cod_cuenta)
	db.session.delete(cuenta)
	db.session.commit()
	flash('Tipo de cuenta eliminada correctamente')
	return redirect(url_for('catalogo_cuentas.index'))

@bp.route('/get')
@login_required
def get():
	tipo_cuentas = CatalogoCuentas.query.all()
	catalogo = []
	for tipo_cuenta in tipo_cuentas:
		catalogo.append(tipo_cuenta.serialize())
	return jsonify(catalogo)