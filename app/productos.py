from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.auth import login_required
from .models import Producto

bp = Blueprint('productos', __name__, url_prefix='/productos')

@bp.route('/')
@login_required
def index():
	productos = Producto.query.all()
	return render_template('productos/index.html', productos = productos)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		codigo = request.form['cod_producto']
		nombre = request.form['nombre']
		precio = request.form['precio']
		existencias = 0

		producto = Producto(codigo, nombre, precio, existencias)

		db.session.add(producto)
		db.session.commit()
		flash('Producto creado correctamente')
		return redirect(url_for('productos.index'))
	return render_template('productos/create.html')

@bp.route('/update/<cod_producto>', methods = ('GET', 'POST'))
@login_required
def update(cod_producto):
	producto = Producto.query.get_or_404(cod_producto)
	if request.method == 'POST':
		producto.nombre = request.form['nombre']
		producto.precio = request.form['precio']
		producto.existencias = 0

		db.session.commit()
		flash('Producto modificado correctamente')
		return redirect(url_for('productos.index'))
	return render_template('productos/update.html', producto = producto)

@bp.route('/delete/<cod_producto>')
@login_required
def delete(cod_producto):
	producto = Producto.query.get_or_404(cod_producto)
	db.session.delete(producto)
	db.session.commit()
	flash('Producto eliminado correctamente')
	return redirect(url_for('productos.index'))

@bp.route('/get')
@bp.route('/get/<cod_producto>')
@login_required
def get(cod_producto = None):
	if cod_producto:
		producto = Producto.query.get_or_404(cod_producto).serialize()
		return jsonify(producto)
	productos = Producto.query.all()
	lista_productos = []
	for producto in productos:
		lista_productos.append(producto.serialize())
	return jsonify(lista_productos)

