from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///materias.db'
db= SQLAlchemy(app)

class Materia(db.Model):
    id = db. Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    anio = db.Column(db.Integer)
    hs = db.Column(db.Integer)
class Correlativa(db.Model): #creo la relacion entre una materia con a q se requiere para cursar,y si se req q este reg o aprob 
    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    requiere_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    tipo = db.Column(db.String(10))  # "regular" o "aprobada"
class EstadoMateria(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    materia_id=db.Column(db.Integer, db.ForeignKey('materia.id'), unique=True, nullable=False)
    estado=db.Column(db.String(20),nullable=False, default='pendiente')


@app.route('/materias')
def ver_materias():
    materias = Materia.query.all()
    resultado = [{"id": m.id, "nombre": m.nombre, "anio": m.anio} for m in materias]
    return {"materias": resultado}

@app.route('/materias/<int:id>/estado', methods=['POST'])
def marcar_estado(id):
    materia=Materia.query.get(id)
    if materia is None:
        return jsonify({"error":"Materia no encontrada"}), 404
    datos=request.get_json() #esto es lo que lee mi peticion POST y lo convierte a diccionario python 
    nuevo_estado=datos.get('estado')
    if nuevo_estado not in ('pendiente', 'regular', 'aprobada'):
        return jsonify({"error":"estado debe ser pendiente, regular o aprobada"}), 400

    estado_materia=EstadoMateria.query.filter_by(materia_id=id).first()
    if estado_materia is None:
        estado_materia = EstadoMateria(materia_id=id, estado=nuevo_estado)
        db.session.add(estado_materia)
    else:
        estado_materia.estado = nuevo_estado

    db.session.commit()
    return jsonify({"materia_id": id, "estado": estado_materia.estado}), 200

@app.route('/puedo-cursar')
def puedo_cursar():

    ids_regularizados = [e.materia_id for e in EstadoMateria.query.filter_by(estado='regular').all()]
    ids_aprobados = [e.materia_id for e in EstadoMateria.query.filter_by(estado='aprobada').all()]

    disponibles = []

    for materia in Materia.query.all():
        requisitos = Correlativa.query.filter_by(materia_id=materia.id).all()

        req_regulares = [r.requiere_id for r in requisitos if r.tipo == "regular"]
        req_aprobadas = [r.requiere_id for r in requisitos if r.tipo == "aprobada"]

        cumple_regulares = all(req in ids_regularizados or req in ids_aprobados for req in req_regulares)
        cumple_aprobadas = all(req in ids_aprobados for req in req_aprobadas)

        if cumple_regulares and cumple_aprobadas:
            disponibles.append(materia.nombre)

    return {"puede_cursar": disponibles}

if __name__ == '__main__':
    app.run(debug=True)
    