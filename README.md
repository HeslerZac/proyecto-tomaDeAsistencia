# Local Web Server for Fingerprint Reader (Flask + PostgreSQL)

Bridge between Arduino (fingerprint) via Serial and a PostgreSQL database with a simple web UI to register people and log attendance.

## Requirements
- Python 3.10+
- PostgreSQL local or remote
- Arduino connected over USB (sketch must follow the serial protocol)

## Install
1) Create venv and install deps:
```
python -m venv .venv
. .venv/Scripts/activate   # Windows PowerShell
pip install -r requirements.txt
```
2) Configure environment:
- Copy `.env.example` to `.env` and edit:
  - `DATABASE_URL=postgresql+psycopg://user:pass@host:5432/asistencias`
  - `SERIAL_PORT=COM3` (adjust to your system)
  - `SERIAL_BAUDRATE=9600` (must match Arduino Serial.begin)

3) Create DB if needed:
```
createdb asistencias
```

## Run
```
python app.py
```
- Open http://localhost:5000.
- The registration form sends `R,<ID>` to Arduino and waits for `REG_OK`/`REG_FAIL`.
- The serial worker logs `FND,<ID>` as attendance automatically.
- The People table shows a button to delete the stored fingerprint; it sends `E,<ID>` and waits for `DEL_OK`/`DEL_FAIL`.
- The People table also includes a button to delete the Person completely (DB + fingerprint). It attempts `E,<ID>` first and then removes the DB record (and their attendance). You can tick a checkbox to force DB deletion even if sensor deletion fails/timeouts.
 - Attendance auto-refreshes every 5s and can be exported as CSV respecting current filters via the "Exportar CSV" button (or `GET /api/asistencias.csv?desde=YYYY-MM-DD&hasta=YYYY-MM-DD&rol=...`).
 - UI timezone: set `TIMEZONE` in `.env` (default `UTC`); server renders dates in that zone and JSON includes `timestamp_utc`.

## Serial Protocol
- All commands end with `\n`:
  - Flask -> Arduino: `R,<ID>` (start registration)
  - Arduino -> Flask: `REG_OK,<ID>` | `REG_FAIL`
  - Arduino -> Flask: `FND,<ID>` when a finger is recognized
  - (Optional) Flask -> Arduino: `E,<ID>` and Arduino -> Flask: `DEL_OK,<ID>` | `DEL_FAIL`
  - Implemented UI button calls POST `/eliminar/<ID>` and updates `huella_guardada` on `DEL_OK`.
  - Full delete calls POST `/persona/<ID>/borrar` and removes DB rows (and tries sensor delete first).
  - CSV export (asistencias): `GET /api/asistencias.csv?desde=YYYY-MM-DD&hasta=YYYY-MM-DD&rol=ALUMNO|PROFESOR|PERSONAL&limit=...` returns `text/csv` with headers `id,person_id,persona_nombre,persona_rol,timestamp`. Single-day `fecha=YYYY-MM-DD` is also supported for compatibility.
  - CSV export (personas): `GET /api/personas.csv?desde=YYYY-MM-DD&hasta=YYYY-MM-DD` returns `text/csv` with headers `id,nombre,rol,huella_guardada,asistencias_count`.

## Structure
- `app.py`: Flask app, models, routes, serial worker (thread) and protocol handling.
- `templates/`: simple HTML (PicoCSS) for dashboard.
- `config.py`: configuration via environment variables.

## Notes
- The serial thread starts once and tries to reconnect if the port fails.
- `/registrar` waits up to 30s for `REG_OK`/`REG_FAIL` and updates/removes the Persona accordingly.
- Sensor IDs are the PK of `persona` table. The smallest free positive integer is assigned.
- Allowed roles: `ALUMNO`, `PROFESOR`, `PERSONAL`.

## Sketch compatibility
- Update Arduino sketch to:
  - Read lines from Serial ending with `\n`.
  - On `R,<ID>` call `registrarHuella(ID)` and send `REG_OK,<ID>` or `REG_FAIL`.
  - Inside `reconocerHuella()` when found, send `FND,<ID>` immediately.
- Serial speed: 9600 (matches `SERIAL_BAUDRATE`).

## Troubleshooting
- If serial cannot open, verify `SERIAL_PORT` (on Windows check Device Manager: COMx).
- With Flask `debug=True`, the reloader spawns twice; protected to avoid duplicate serial thread.
- For remote PostgreSQL, ensure firewall and credentials allow connection.
 - Check `/health` for serial status and available COM ports.
