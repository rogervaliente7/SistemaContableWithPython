from app import db

#	Tabla: usuario
class Usuario(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	password = db.Column(db.Text, nullable = False)

	def __init__(self, username, password):
		self.username = username
		self.password = password

#	Tabla: productos
class Producto(db.Model):
	cod_producto = db.Column(db.String(20), primary_key = True)
	nombre = db.Column(db.String(50), unique = True, nullable = False)
	precio = db.Column(db.Float, nullable = False)
	existencias = db.Column(db.Integer, nullable = False)
	
	def __init__(self, cod_producto, nombre, precio, existencias):
		self.cod_producto = cod_producto
		self.nombre = nombre
		self.precio = precio
		self.existencias = existencias

	def serialize(self):
		return {
			'cod_producto':self.cod_producto,
			'nombre':self.nombre,
			'precio':self.precio,
			'existencias':self.existencias
		}

#	Tabla: tipo_terceros
class TipoTercero(db.Model):
	id_tipo_tercero = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(50), nullable = False)
	
	def __init__(self, nombre):
		self.nombre = nombre

	def serialize(self):
		return {
			'id_tipo_tercero':self.id_tipo_tercero,
			'nombre':self.nombre,
		}

#	Tabla: tercero
class Tercero(db.Model):
	id_tercero = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(100), nullable = False)
	direccion = db.Column(db.Text)
	telefono = db.Column(db.String(20), unique = True)
	email = db.Column(db.String(100), unique = True)
	id_tipo_tercero = db.Column(db.Integer, db.ForeignKey('tipo_tercero.id_tipo_tercero'), nullable = False)
	tipo_tercero = db.relationship('TipoTercero', backref='tercero')

	def __init__(self, nombre, direccion, telefono, email, id_tipo_tercero):
		self.nombre = nombre
		self.direccion = direccion
		self.telefono = telefono
		self.email = email
		self.id_tipo_tercero = id_tipo_tercero

	def serialize(self):
		return {
			'id_tercero':self.id_tercero,
			'nombre':self.nombre,
			'direccion':self.direccion,
			'telefono':self.telefono,
			'email':self.email,
			'tipo_tercero':self.tipo_tercero.nombre
		}

#	Tabla: tipo_documento
class TipoDocumento(db.Model):
	id_tipo_documento = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(50), unique = True, nullable = False)

	def __init__(self, nombre):
		self.nombre = nombre

	def serialize(self):
		return {
			'id_tipo_documento':self.id_tipo_documento,
			'nombre':self.nombre,
		}

#	Tabla: catalogo_cuentas
class CatalogoCuentas(db.Model):
	cod_cuenta = db.Column(db.String(20), primary_key = True)
	nombre = db.Column(db.String(50), unique = True, nullable = False)

	def __init__(self, cod_cuenta, nombre):
		self.cod_cuenta = cod_cuenta
		self.nombre = nombre

	def serialize(self):
		return {
			'cod_cuenta':self.cod_cuenta,
			'nombre':self.nombre,
		}

#	Tabla: cuenta
class Cuenta(db.Model):
	id_cuenta = db.Column(db.Integer, primary_key = True)
	cod_tipo_cuenta = db.Column(db.Integer, db.ForeignKey('catalogo_cuentas.cod_cuenta'), nullable = False)
	nombre = db.Column(db.String(100), nullable = False)
	debe = db.Column(db.Float)
	haber = db.Column(db.Float)
	tipo_cuenta = db.relationship('CatalogoCuentas', backref='cuenta')

	def __init__(self, cod_tipo_cuenta, nombre, debe, haber):
		self.cod_tipo_cuenta = cod_tipo_cuenta
		self.nombre = nombre
		self.debe = debe
		self.haber = haber
		
	def serialize(self):
		return {
			'id_cuenta':self.id_cuenta,
			'tipo':self.tipo_cuenta.nombre,
			'nombre':self.nombre,
			'debe':self.debe,
			'haber':self.haber
		}

#	Tabla: Soporte
class Soporte(db.Model):
	cod_soporte = db.Column(db.Integer, primary_key = True)
	fecha_soporte = db.Column(db.String(20), nullable = False)
	id_tercero = db.Column(db.Integer, db.ForeignKey('tercero.id_tercero'), nullable = False)
     
	def __init__(self, cod_soporte, fecha_soporte, id_tercero):
		self.cod_soporte
		self.fecha_soporte
		self.id_tercero

	def	serialize(self):
		return {
			'cod_soporte':self.cod_soporte,
			'fecha_soporte':self.fecha_soporte,
			'id_tercero':self.id_tercero
		}	

#	Tabla: Documentos
class Documento(db.Model):
	num_documento = db.Column(db.Integer, primary_key = True)
	fecha_creacion = db.Column(db.String(20), nullable = False)

	def __init__(self, num_documento, fecha_creacion):
		self.num_documento = num_documento
		self.fecha_creacion = fecha_creacion

	def	serialize(self):
		return {
			'num_documento':self.num_documento,
			'fecha_creacion':self.fecha_creacion
		}

#	Tabla: factura
class Factura(db.Model):
	id_factura = db.Column(db.Integer, primary_key = True)
	id_tercero = db.Column(db.Integer, db.ForeignKey('tercero.id_tercero'), nullable = False)
	fecha = db.Column(db.String(20), nullable = False)
	tercero = db.relationship('Tercero', backref='factura')
	total = db.Column(db.Float, nullable = False)
	detalles = db.relationship('DetalleFactura', backref='factura')

	def __init__(self, id_tercero, fecha):
		self.id_tercero = id_tercero
		self.fecha = fecha
		self.total = 0

	def serialize_detalles(self):
		list_detalles = []
		for detalle in self.detalles:
			list_detalles.append(detalle.serialize())
		return list_detalles

	def	serialize(self):
		return {
			'id_factura':self.id_factura,
			'tercero':self.tercero.serialize(),
			'fecha':self.fecha,
			'detalle': self.serialize_detalles(),
			'total':self.total
		}

#	Tabla: detalle_factura
class DetalleFactura(db.Model):
	id_detalle_factura = db.Column(db.Integer, primary_key = True)
	id_factura = db.Column(db.Integer, db.ForeignKey('factura.id_factura'), nullable = False)
	cod_producto = db.Column(db.Integer, db.ForeignKey('producto.cod_producto'), nullable = False)
	precio_venta = db.Column(db.Float, nullable = False)
	cantidad = db.Column(db.Integer, nullable = False)
	monto = db.Column(db.Float, nullable = False)
	producto = db.relationship('Producto', backref='detalle_factura')

	def __init__(self, id_factura, cod_producto, precio_venta, cantidad):
		self.id_factura = id_factura
		self.cod_producto = cod_producto
		self.precio_venta = precio_venta
		self.cantidad = cantidad
		self.monto = precio_venta*cantidad

	def	serialize(self):
		return {
			'id_detalle_factura':self.id_detalle_factura,
			'id_factura':self.id_factura,
			'cod_producto':self.cod_producto,
			'nombre_producto':self.producto.nombre,
			'precio_venta':self.precio_venta,
			'cantidad':self.cantidad,
			'monto':self.monto
		}

#	Tabla: compra
class Compra(db.Model):
	id_compra = db.Column(db.Integer, primary_key = True)
	id_tercero = db.Column(db.Integer, db.ForeignKey('tercero.id_tercero'), nullable = False)
	fecha = db.Column(db.String(20), nullable = False)
	total = db.Column(db.Float, nullable = False)
	tercero = db.relationship('Tercero', backref='compra')
	detalles = db.relationship('DetalleCompra', backref='compra')

	def __init__(self, id_tercero, fecha):
		self.id_tercero = id_tercero
		self.fecha = fecha
		self.total = 0

	def serialize_detalles(self):
		list_detalles = []
		for detalle in self.detalles:
			list_detalles.append(detalle.serialize())
		return list_detalles

	def	serialize(self):
		return {
			'id_compra':self.id_compra,
			'tercero':self.tercero.serialize(),
			'fecha':self.fecha,
			'detalle': self.serialize_detalles(),
			'total':self.total
		}

class DetalleCompra(db.Model):
	id_detalle_compra = db.Column(db.Integer, primary_key = True)
	id_compra = db.Column(db.Integer, db.ForeignKey('compra.id_compra'), nullable = False)
	cod_producto = db.Column(db.Integer, db.ForeignKey('producto.cod_producto'), nullable = False)
	costo = db.Column(db.Float, nullable = False)
	cantidad = db.Column(db.Integer, nullable = False)
	monto = db.Column(db.Float, nullable = False)
	producto = db.relationship('Producto', backref='detalle_compra')

	def __init__(self, id_compra, cod_producto, costo, cantidad):
		self.id_compra = id_compra
		self.cod_producto = cod_producto
		self.costo = costo
		self.cantidad = cantidad
		self.monto = costo*cantidad

	def	serialize(self):
		return {
			'id_detalle_compra':self.id_detalle_compra,
			'id_compra':self.id_compra,
			'cod_producto':self.cod_producto,
			'nombre_producto':self.producto.nombre,
			'costo':self.costo,
			'cantidad':self.cantidad,
			'monto':self.monto
		}