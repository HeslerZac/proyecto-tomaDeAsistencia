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
