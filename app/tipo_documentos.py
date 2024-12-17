from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.auth import login_required
from .models import TipoDocumento

bp = Blueprint('tipo_documentos', __name__, url_prefix='/documentos/tipos')

@bp.route('/')
@login_required
def index():
	tipo_documentos = TipoDocumento.query.all()
	return render_template('/documentos/tipos/index.html', tipo_documentos = tipo_documentos)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		nombre = request.form['nombre']

		tipo_documento = TipoDocumento(nombre)

		db.session.add(tipo_documento)
		db.session.commit()
		flash('Tipo de documento creado correctamente')
		return redirect(url_for('tipo_documentos.index'))
	return render_template('/documentos/tipos/create.html')

@bp.route('/update/<id_tipo_documento>', methods = ('GET', 'POST'))
@login_required
def update(id_tipo_documento):
	tipo_documento = TipoDocumento.query.get_or_404(id_tipo_documento)
	if request.method == 'POST':
		tipo_documento.nombre = request.form['nombre']

		db.session.commit()
		flash('Tipo de documento modificado correctamente')
		return redirect(url_for('tipo_documentos.index'))
	return render_template('/documentos/tipos/update.html', tipo_documento = tipo_documento)

@bp.route('/delete/<id_tipo_documento>')
@login_required
def delete(id_tipo_documento):
	tipo_documento = TipoDocumento.query.get_or_404(id_tipo_documento)
	db.session.delete(tipo_documento)
	db.session.commit()
	flash('Tipo de documento eliminado correctamente')
	return redirect(url_for('tipo_documentos.index'))

@bp.route('/get')
@login_required
def get():
	tipo_documentos = TipoDocumento.query.all()
	lista_tipo_documentos = []
	for tipo_documento in tipo_documentos:
		lista_tipo_documentos.append(tipo_documento.serialize())
	return jsonify(lista_tipo_documentos)