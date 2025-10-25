import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/asistencias",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

    SERIAL_PORT = os.getenv("SERIAL_PORT", "COM3")
    SERIAL_BAUDRATE = int(os.getenv("SERIAL_BAUDRATE", "9600"))
    SERIAL_TIMEOUT = float(os.getenv("SERIAL_TIMEOUT", "0.2"))  # seconds
    REG_TIMEOUT = float(os.getenv("REG_TIMEOUT", "30"))  # seconds to wait for REG_OK/REG_FAIL
    TIMEZONE = os.getenv("TIMEZONE", "UTC")
    # Store timestamps in local timezone (naive) instead of UTC
    TIME_USE_LOCAL = os.getenv("TIME_USE_LOCAL", "1") in ("1", "true", "True")
    # Anti-rebote: ignorar FND repetido del mismo ID dentro de esta ventana (segundos)
    DUPLICATE_WINDOW_SEC = float(os.getenv("DUPLICATE_WINDOW_SEC", "60"))
    # Horario de entrada y tardanza
    START_TIME = os.getenv("START_TIME", "08:00")  # HH:MM (hora local)
    TARDINESS_TOL_MIN = int(os.getenv("TARDINESS_TOL_MIN", "10"))  # minutos de tolerancia
    # Mapeo opcional por grado en JSON: {"Preprimaria":"08:15","Primero":"08:00",...}
    SCHEDULE_BY_GRADE = os.getenv("SCHEDULE_BY_GRADE", "")
    # CSV delimiter for Excel compatibility (use ';' for many locales)
    CSV_DELIMITER = os.getenv("CSV_DELIMITER", ";")
