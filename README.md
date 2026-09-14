# API UTN - Gestión de Correlativas

API REST desarrollada con Flask que permite consultar materias y calcular cuáles se pueden cursar en base a las correlativas regularizadas y aprobadas, siguiendo el plan de estudios 2023 de Ingeniería en Sistemas de Información (UTN).
##  Tecnologías

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
##  Estructura del proyecto

API_UTN_project/
├── API_UTN_project.py     # App principal: modelos y endpoints
├── plan2023_materias.py   # Datos del plan de estudios 2023 (materias y correlativas)
├── cargar_materias.py     # Script para cargar los datos iniciales a la base
└── requirements.txt       # Dependencias del proyecto
##  Instalación

   1. Clonar el repositorio:
      ```bash
      git clone https://github.com/santiporcell/API_UTN_project.git
      cd API_UTN_project
      ```

   2. Crear y activar un entorno virtual:
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

   5. Correr la aplicación:
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
      { "id": 1, "nombre": "Análisis Matemático I", "anio": 1 },
      { "id": 2, "nombre": "Sistemas y Procesamiento de Datos", "anio": 1 }
   ]
   }
   ```

   ### `GET /puedo-cursar/<regularizadas>/<aprobadas>`
   Calcula qué materias se pueden cursar según las materias regularizadas y aprobadas, respetando las correlativas de cada una.

   - `regularizadas`: IDs separados por coma de las materias regularizadas (ej: `1,3,5`). Si no hay ninguna, usar `0`.
   - `aprobadas`: IDs separados por coma de las materias aprobadas (ej: `2,4`). Si no hay ninguna, usar `0`.

   **Ejemplo de uso:**

   GET /puedo-cursar/1,3,5/2,4


   **Respuesta de ejemplo:**

   {
   "puede_cursar": ["Física I", "Álgebra y Geometría Analítica"]
   }


##  Roadmap

- [ ] Endpoint `POST` para cargar/actualizar materias desde la API (sin depender de `cargar_materias.py`)
- [ ] Manejo de errores (404 si la materia no existe, 400 si los IDs son inválidos)
- [ ] Tests con pytest
- [ ] Documentación interactiva (Swagger / Postman collection)
- [ ] Deploy (Render / Railway)

##  Autor

Santiago Porcel — Estudiante de Ingeniería en Sistemas (UTN)
