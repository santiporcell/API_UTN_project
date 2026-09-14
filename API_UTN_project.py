from flask import Flask
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

@app.route('/materias')
def ver_materias():
    materias = Materia.query.all()
    resultado = [{"id": m.id, "nombre": m.nombre, "anio": m.anio} for m in materias]
    return {"materias": resultado}

@app.route('/puedo-cursar/<regularizadas>/<aprobadas>')
def puedo_cursar(regularizadas, aprobadas): # todo loq yoponga en el navegador en <regularizas seran ahora los datos de las materias que regularicé y lo mismo para las aprobadas

    ids_regularizados = [int(x) for x in regularizadas.split(',')] if regularizadas != '0' else []
    ids_aprobados = [int(x) for x in aprobadas.split(',')] if aprobadas != '0' else []
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
    