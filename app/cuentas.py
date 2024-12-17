from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.auth import login_required
from .models import Cuenta
from .models import CatalogoCuentas

bp = Blueprint('cuentas', __name__, url_prefix='/cuentas')

@bp.route('/')
@login_required
def index():
	cuentas = Cuenta.query.all()
	return render_template('cuentas/index.html', cuentas = cuentas)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		nombre = request.form['nombre']
		cod_tipo_cuenta = int(request.form['cod_tipo_cuenta'])
		debe = float(request.form['debe'])
		haber = float(request.form['haber'])

		cuenta = Cuenta(cod_tipo_cuenta, nombre, debe, haber)

		db.session.add(cuenta)
		db.session.commit()
		flash('Cuenta creada correctamente')
		return redirect(url_for('cuentas.index'))
	tipo_cuentas = CatalogoCuentas.query.all()
	return render_template('/cuentas/create.html', tipo_cuentas = tipo_cuentas)

@bp.route('/update/<int:id_cuenta>', methods = ('GET', 'POST'))
@login_required
def update(id_cuenta):
	cuenta = Cuenta.query.get_or_404(id_cuenta)
	if request.method == 'POST':
		cuenta.nombre = request.form['nombre']
		cuenta.cod_tipo_cuenta = int(request.form['cod_tipo_cuenta'])
		cuenta.debe = float(request.form['debe'])
		cuenta.haber = float(request.form['haber'])

		db.session.commit()
		flash('Cuenta modificada correctamente')
		return redirect(url_for('cuentas.index'))
	tipo_cuentas = CatalogoCuentas.query.all()
	return render_template('/cuentas/update.html', tipo_cuentas = tipo_cuentas, cuenta = cuenta)

@bp.route('/delete/<id_cuenta>')
@login_required
def delete(id_cuenta):
	cuenta = Cuenta.query.get_or_404(id_cuenta)
	db.session.delete(cuenta)
	db.session.commit()
	flash('Cuenta eliminada correctamente')
	return redirect(url_for('cuentas.index'))

@bp.route('/get')
@login_required
def get():
	cuentas = Cuenta.query.all()
	lista_cuentas = []
	for cuenta in cuentas:
		lista_cuentas.append(cuenta.serialize())
	return jsonify(lista_cuentas)