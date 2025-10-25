# Proyecto de Asistencias (Flask + PostgreSQL + Arduino)

Servidor local (web) que integra un lector de huella en Arduino vía Serial, guarda asistencias en PostgreSQL y ofrece un dashboard para registrar personas, tomar asistencia, reportar y exportar.

## Tecnologías
- Python 3.10+
- Flask, Flask-SQLAlchemy, Flask-Login, Flask‑WTF
- PostgreSQL (driver psycopg v3)
- pyserial (hilo de lectura Serial)
- openpyxl (exportación XLSX)
- PicoCSS (UI simple y responsiva)

## Requisitos
- Python 3.10+ en Windows
- PostgreSQL en local (o remoto)
- Arduino (UNO u otro) conectado por USB con el sketch incluido (protocolo serie)

## Instalación
1) Crear entorno e instalar dependencias:
`
python -m venv .venv
. .venv/Scripts/activate   # PowerShell
pip install -r requirements.txt
`
2) Configurar variables:
- Copia .env.example a .env y ajusta credenciales de DB y Serial. Ejemplo:
`
DATABASE_URL=postgresql+psycopg://postgres:TU_PASSWORD@localhost:5432/asistencias
SERIAL_PORT=COM10
SERIAL_BAUDRATE=9600
FLASK_ENV=production
FLASK_DEBUG=0
TIMEZONE=America/Guatemala
TIME_USE_LOCAL=1
DUPLICATE_WINDOW_SEC=60
START_TIME=08:00
TARDINESS_TOL_MIN=10
SCHEDULE_BY_GRADE={"Preprimaria":"08:15","Primero":"08:00","Segundo":"08:00","Tercero":"08:00","Cuarto":"07:45","Quinto":"07:45","Sexto":"07:45"}
CSV_DELIMITER=;
`
3) Crear base (si no existe) y usuario (opcional):
`
psql -U postgres -h localhost -d postgres -c "CREATE DATABASE asistencias;"
`

## Ejecutar
`
python app.py
`
Abre http://localhost:5000. Login por defecto: crea usuario en /users o setea ADMIN_USERNAME/ADMIN_PASSWORD en .env (se crea solo al iniciar si la tabla está vacía).

## Protocolo Serial
- Comandos con \n:
  - Flask → Arduino: R,<ID> (registrar), E,<ID> (eliminar)
  - Arduino → Flask: REG_OK,<ID> | REG_FAIL | DEL_OK,<ID> | DEL_FAIL | FND,<ID>
- El servidor ignora FND duplicado del mismo ID durante DUPLICATE_WINDOW_SEC.

## Funcionalidades
- Personas: registro con rol (ALUMNO/PROFESOR/PERSONAL), grado (Preprimaria–Sexto), sección (A/B), documento (único), activar/desactivar, CSV/XLSX por alumno.
- Toma: asistencias en vivo (panel), modo pantalla completa.
- Reportes: filtros por fechas, rol, grado, sección y nombre; cálculo de tardanza (según horario y tolerancia); exportación CSV/XLSX (incluye hojas Resumen y Resumen por alumno).
- Mensajes: log TX/RX del serial. Health: /health (puertos disponibles, estado del serial).

## Notas de uso
- Cierra el Monitor Serie del IDE para liberar el COM antes de usar la app.
- Si el COM cambia (al reconectar), actualiza SERIAL_PORT o usa SERIAL_PORT=AUTO.
- El sketch Arduino evita duplicar una misma huella entre personas (chequeo tras el primer escaneo).

## Problemas frecuentes
- Serial “Acceso denegado”: otra app tiene abierto el puerto (cerrar Monitores Serie / reiniciar). Ejecutar sin reloader (FLASK_ENV=production).
- CSV en una columna: usa CSV_DELIMITER=; (por defecto) o añade ?delim=, a la URL para coma.
- XLSX 501: instalar dependencias pip install -r requirements.txt (openpyxl).

## Licencia
Proyecto bajo licencia MIT (ver LICENSE).
