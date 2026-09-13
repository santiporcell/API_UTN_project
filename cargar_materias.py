from API_UTN_project import app, db, Materia, Correlativa  # desde el archivo de tu servidor "app.py" importas el servidor y la tabla
from plan2023_materias import materias, correlativas

with app.app_context():
    db.create_all()  # mira q clases hice y crea las tablas 

    for m in materias:
        nueva = Materia(id=m["id"], nombre=m["nombre"], anio=m["anio"], hs=m["hs"])
        db.session.add(nueva) #pone la materia en esera lista para guardar

    db.session.commit()# se sube todo al archiv
    print("Materias cargadas con exito")

    for c in correlativas:
        materia_id = c["materia_id"]

        for req_id in c["regulares"]:
            db.session.add(Correlativa(materia_id=materia_id, requiere_id=req_id, tipo="regular"))

        for req_id in c["aprobadas"]:
            db.session.add(Correlativa(materia_id=materia_id, requiere_id=req_id, tipo="aprobada"))

    db.session.commit()  # segundo commit: ya con las correlativas cargadas
    print("Materias y correlativas cargadas con éxito")

#Si necesitás resetear, borrás materias.db y lo volvés a correr.