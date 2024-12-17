from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.auth import login_required
from datetime import datetime
from .models import Producto
from .models import Tercero
from .models import Factura
from .models import DetalleFactura

bp = Blueprint('caja', __name__, url_prefix='/caja')

@bp.route('/')
@login_required
def index():
	productos = Producto.query.all()
	return render_template('/caja/index.html', productos = productos)

@bp.route('/venta', methods = ('GET', 'POST'))
@login_required
def venta():
	if request.method == 'POST':
		data = request.get_json()

		id_cliente = int(data['id_cliente'])
		fecha = datetime.now()
		detalles = data['detalles']
		total = 0

		cliente = Tercero.query.get_or_404(id_cliente)

		if cliente and detalles:
			factura = Factura(id_cliente, fecha.strftime('%d-%m-%Y'))
			db.session.add(factura)
			db.session.commit()

			for detalle in detalles:
				cod_producto = detalle['cod_producto']
				cantidad = int(detalle['cantidad'])

				producto = Producto.query.get_or_404(cod_producto)

				if producto:
					if producto.existencias >= cantidad:
						detalle_factura = DetalleFactura(factura.id_factura, cod_producto, producto.precio, cantidad)
						producto.existencias -= cantidad
						db.session.add(detalle_factura)
						db.session.commit()
						total += detalle_factura.monto

			factura.total = total
			db.session.commit()
			return jsonify({'id_factura':factura.id_factura})
	ventas = Factura.query.all();
	return render_template('/ventas/index.html', ventas = ventas)

@bp.route('/venta/get/<int:id_factura>')
@login_required
def get_venta(id_factura):
	if id_factura:
		factura = Factura.query.get_or_404(id_factura)
		return jsonify(factura.serialize())

@bp.route('/venta/<int:id_factura>')
def detalle(id_factura):
	venta = Factura.query.get_or_404(id_factura)
	print(venta.detalles)
	return render_template('/ventas/detalle.html', venta = venta)