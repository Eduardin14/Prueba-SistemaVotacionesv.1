# Sistema de Votaciones - API RESTful

API RESTful construida con **FastAPI** + **SQLAlchemy** para gestionar un sistema de votaciones: registro de votantes, candidatos, emisión de votos y estadísticas de resultados.

## Tecnologías

- **Python 3.11+**
- **FastAPI** - framework web
- **SQLAlchemy 2.0** - ORM
- **SQLite** (desarrollo local, por defecto) / **PostgreSQL o MySQL** (producción, vía `DATABASE_URL`)
- **Pydantic v2** - validación de datos
- **Pandas + Matplotlib** - generación de gráfica de resultados
- **Uvicorn** - servidor ASGI

## Estructura del proyecto

```
votaciones/
├── main.py                  # Punto de entrada (uvicorn)
├── seed_db.py                # Script para poblar datos de prueba
├── generate_chart.py         # Genera grafica de votos por candidato (pandas)
├── requirements.txt
├── .env.example
└── src/
    ├── entities/              # Modelos SQLAlchemy (Voter, Candidate, Vote)
    ├── schemas/                # Schemas Pydantic (request/response)
    ├── crud/                   # Logica de negocio y acceso a datos
    ├── endpoints/               # Routers de FastAPI
    ├── core/                    # Config, excepciones, respuestas y error handlers
    ├── database/                 # Configuracion de conexion a BD
    └── utils/app.py              # App FastAPI principal
```

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/Eduardin14/Prueba-SistemaVotacionesv.1.git
cd Prueba-SistemaVotacionesv.1
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno (opcional)

```bash
cp .env.example .env
```

Por defecto, si no defines `DATABASE_URL` para usar tu version en la nube o local de PostgreSQL, el proyecto usa **SQLite** (`dev.db`) automáticamente — no necesitas instalar ni configurar nada más para probarlo localmente.

Para usar PostgreSQL define en `.env`:

```
DATABASE_URL=postgresql://usuario:password@localhost:5432/votaciones_db
```

### 4. Ejecutar la API

```bash
python main.py
```

La API quedará disponible en `http://127.0.0.1:8000`. Las tablas se crean automáticamente al iniciar (no requiere migraciones para esta prueba).

### 5. Documentación interactiva (Swagger)

Abre en el navegador:

```
http://127.0.0.1:8000/docs
```

### 6. (Opcional) Poblar con datos de prueba

```bash
python seed_db.py
```

Esto crea 3 candidatos, 5 votantes y 5 votos de ejemplo.

### 7. Generar la gráfica de resultados

```bash
python generate_chart.py
```

Esto genera `statistics_chart.png` en la raíz del proyecto con los votos actuales por candidato (usando pandas + matplotlib).

## Endpoints de la API

Todas las respuestas siguen el formato:

```json
{ "success": true, "data": { ... }, "message": "..." }
```

o en caso de error:

```json
{ "success": false, "error": { "code": "...", "message": "...", "details": null } }
```

### Votantes

**Registrar votante**
```bash
curl -X POST http://127.0.0.1:8000/voters \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan Perez", "email": "juan.perez@example.com"}'
```

**Listar votantes** (con paginación y filtro opcional)
```bash
curl "http://127.0.0.1:8000/voters?skip=0&limit=10&name=Juan"
```

**Eliminar votante**
```bash
curl -X DELETE http://127.0.0.1:8000/voters/<voter_id>
```

### Candidatos

**Registrar candidato**
```bash
curl -X POST http://127.0.0.1:8000/candidates \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana Torres", "party": "Partido Verde"}'
```

**Listar candidatos**
```bash
curl "http://127.0.0.1:8000/candidates?skip=0&limit=10"
```

### Votos

**Emitir un voto**
```bash
curl -X POST http://127.0.0.1:8000/votes \
  -H "Content-Type: application/json" \
  -d '{"voter_id": "<voter_id>", "candidate_id": "<candidate_id>"}'
```

**Listar todos los votos**
```bash
curl "http://127.0.0.1:8000/votes?skip=0&limit=10"
```

**Obtener estadísticas**
```bash
curl http://127.0.0.1:8000/votes/statistics
```

Respuesta de ejemplo:
```json
{
  "success": true,
  "data": {
    "total_votes": 5,
    "total_voters_voted": 5,
    "candidates": [
      { "candidate_id": "...", "name": "Ana Torres", "party": "Partido Verde", "votes": 3, "percentage": 60.0 },
      { "candidate_id": "...", "name": "Carlos Ruiz", "party": "Partido Azul", "votes": 1, "percentage": 20.0 },
      { "candidate_id": "...", "name": "Marta Gomez", "party": "Partido Rojo", "votes": 1, "percentage": 20.0 }
    ]
  },
  "message": null
}
```

## Validaciones implementadas

- Un votante no puede registrarse con un email ya existente.
- Un votante no puede registrarse si su nombre ya existe como candidato (y viceversa).
- Un votante no puede emitir más de un voto (`has_voted` se valida y actualiza automáticamente).
- El `candidate_id` de un voto debe existir, de lo contrario se retorna `404`.
- El candidato debe ser unico, por lo tanto no se pueden crear mas de un candidato con el mismo nombre/partido
- Al emitir un voto, se incrementa automáticamente el contador `votes` del candidato.
- Errores de validación (`422`), recursos no encontrados (`404`), conflictos (`409`) y solicitudes inválidas (`400`) devuelven respuestas estructuradas y consistentes.

## Capturas de las estadísticas

FALTA

## Notas de arquitectura

El proyecto sigue una arquitectura por capas:

- **entities**: modelos ORM (SQLAlchemy)
- **schemas**: contratos de entrada/salida (Pydantic)
- **crud**: reglas de negocio y acceso a datos
- **endpoints**: routers HTTP (FastAPI), delgados, delegan todo al CRUD
- **core**: configuración, excepciones de dominio y manejo global de errores

Esto facilita testing, mantenimiento y escalabilidad del código.
