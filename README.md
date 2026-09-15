# API UTN - Gestión de Correlativas

API REST desarrollada con Flask que permite consultar materias, marcar el progreso propio (pendiente / regular / aprobada) y calcular cuáles se pueden cursar en base a las correlativas, siguiendo el plan de estudios 2023 de Ingeniería en Sistemas de Información (UTN).

##  Tecnologías

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite

##  Estructura del proyecto

```
API_UTN_project/
├── API_UTN_project.py     # App principal: modelos y endpoints
├── plan2023_materias.py   # Datos del plan de estudios 2023 (materias y correlativas)
├── cargar_materias.py     # Script para cargar los datos iniciales a la base
└── requirements.txt       # Dependencias del proyecto
```

##  Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/santiporcell/API_UTN_project.git
   cd API_UTN_project
   ```

2. Crea y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Cargar los datos iniciales de materias y correlativas:
   ```bash
   python cargar_materias.py
   ```

5. Corrar la aplicación:
   ```bash
   python API_UTN_project.py
   ```

   La API queda disponible en `http://127.0.0.1:5000/`.

##  Endpoints

### `GET /materias`
Devuelve el listado completo de materias del plan de estudios.

**Respuesta de ejemplo:**
```json
{
  "materias": [
    { "id": 1, "nombre": "Analisis Matematico I", "anio": 1 },
    { "id": 2, "nombre": "Algebra y Geometria Analitica", "anio": 1 }
  ]
}
```

### `POST /materias/<id>/estado`
Marca (o actualiza) el estado de una materia: `pendiente`, `regular` o `aprobada`. Este estado queda guardado de forma permanente en la base y es lo que usa `/puedo-cursar` para calcular qué materias están disponibles.

**Body de ejemplo:**
```json
{ "estado": "aprobada" }
```

**Respuesta de ejemplo:**
```json
{ "materia_id": 1, "estado": "aprobada" }
```

Si el `id` no corresponde a ninguna materia, devuelve `404`. Si `estado` no es uno de los tres valores válidos, devuelve `400`.

### `GET /puedo-cursar`
Calcula qué materias se pueden cursar en base a los estados ya guardados (marcados previamente con `POST /materias/<id>/estado`), respetando las correlativas de cada una. No recibe parámetros: lee directamente el progreso guardado en la base.

**Respuesta de ejemplo:**
```json
{
  "puede_cursar": ["Analisis Matematico II", "Fisica II"]
}
```

## 🛣️ Roadmap

- [x] Guardar el estado de cada materia (pendiente / regular / aprobada) en la base
- [x] Endpoint `POST` para marcar el estado de una materia
- [x] `/puedo-cursar` calculado automáticamente a partir del estado guardado, sin parámetros en la URL
- [ ] Frontend simple con checkboxes para marcar materias aprobadas/regularizadas sin usar curl/Postman
- [ ] Manejo de errores más completo (validar que las correlativas referencien materias existentes)
- [ ] Tests con pytest
- [ ] Documentación interactiva (Swagger / Postman collection)
- [ ] Deploy (Render / Railway)

## 👤 Autor

Santiago Porcell — Estudiante de Ingeniería en Sistemas (UTN)