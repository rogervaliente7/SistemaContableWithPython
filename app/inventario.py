from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.auth import login_required
from datetime import datetime
from .models import Producto
from .models import Tercero
from .models import Compra
from .models import DetalleCompra

bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@bp.route('/')
@login_required
def index():
	compras = Compra.query.all()
	return render_template('/inventario/index.html', compras = compras)

@bp.route('/compra', methods = ('GET', 'POST'))
@login_required
def compra():
	if request.method == 'POST':
		data = request.get_json()

		id_proveedor = int(data['id_proveedor'])
		fecha = datetime.now()
		detalles = data['detalles']
		total = 0

		proveedor = Tercero.query.get_or_404(id_proveedor)

		if proveedor and detalles:
			compra = Compra(id_proveedor, fecha.strftime('%d-%m-%Y'))
			db.session.add(compra)
			db.session.commit()

			for detalle in detalles:
				cod_producto = detalle['cod_producto']
				costo = float(detalle['costo'])
				cantidad = int(detalle['cantidad'])
				
				producto = Producto.query.get_or_404(cod_producto)

				if producto:
					detalle_compra = DetalleCompra(compra.id_compra, cod_producto, costo, cantidad)
					producto.existencias += cantidad
					db.session.add(detalle_compra)
					db.session.commit()
					total += detalle_compra.monto

			compra.total = total
			db.session.commit()
			return jsonify({'id_compra':compra.id_compra})
	productos = Producto.query.all()
	return render_template('/inventario/compra.html', productos = productos)

@bp.route('/compra/get/<int:id_compra>')
@login_required
def get_compra(id_compra):
	if id_compra:
		compra = Compra.query.get_or_404(id_compra)
		return jsonify(compra.serialize())

@bp.route('/compra/<int:id_compra>')
def detalle(id_compra):
	compra = Compra.query.get_or_404(id_compra)
	return render_template('/inventario/detalle.html', compra = compra)