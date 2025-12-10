import os
import sys

# Ruta absoluta al proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Activar virtualenv creado por cPanel (si existe)
VENV_ACTIVATE = os.path.join(BASE_DIR, "venv", "bin", "activate_this.py")
if os.path.isfile(VENV_ACTIVATE):
    with open(VENV_ACTIVATE) as f:
        exec(f.read(), dict(__file__=VENV_ACTIVATE))

# Importar la app FastAPI
from app.main import app  # Tu aplicación FastAPI

# Convertir ASGI a WSGI usando Mangum
from mangum import Mangum
handler = Mangum(app)

def application(environ, start_response):
    """
    Application compatible con Passenger
    """
    return handler(environ, start_response)
