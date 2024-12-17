from flask import Flask, render_template, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
	
	app = Flask(__name__)

	#	CONFIGURACION DE LA APLICACION
	app.config.from_mapping(
		DEBUG = True,
		SECRET_KEY = 'dev',
		SQLALCHEMY_DATABASE_URI = 'sqlite:///contablesdb.db'
	)

	db.init_app(app)

	#	BLUEPRINTS 
	from . import auth
	app.register_blueprint(auth.bp)

	from . import productos
	app.register_blueprint(productos.bp)

	from . import tipo_terceros
	app.register_blueprint(tipo_terceros.bp)

	from . import tipo_documentos
	app.register_blueprint(tipo_documentos.bp)

	from . import catalogo_cuentas
	app.register_blueprint(catalogo_cuentas.bp)

	from . import terceros
	app.register_blueprint(terceros.bp)

	from . import cuentas
	app.register_blueprint(cuentas.bp)

	from . import caja
	app.register_blueprint(caja.bp)
	
	from . import documentos
	app.register_blueprint(documentos.bp)

	from . import inventario
	app.register_blueprint(inventario.bp)

	# PAGINA PRINCIPAL
	@app.route('/')
	def index():
		if g.usuario:
			return render_template('index.html')
		else:
			return render_template('auth/login.html')

	with app.app_context():
		db.create_all()

	return app
