import sys
import os
from mangum import Mangum

# Añadir el path correcto para importar el proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Importar FastAPI desde app/main.py
try:
    from app.main import app
    # Adaptador para que Passenger -> WSGI -> ASGI (FastAPI)
    handler = Mangum(app)
except Exception as e:
    # Si hay error al importar, crear un handler de error
    def application(environ, start_response):
        status = "500 Internal Server Error"
        headers = [("Content-Type", "text/plain")]
        start_response(status, headers)
        return [f"Error loading FastAPI app: {e}".encode()]
else:
    # Si la importación fue exitosa, crear el handler WSGI
    def application(environ, start_response):
        """
        Passenger requiere un callable WSGI.
        Mangum convierte la petición a ASGI para FastAPI.
        Esto mantiene compatibilidad con Passenger.
        """
        try:
            return handler(environ, start_response)
        except Exception as e:
            start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
            return [str(e).encode("utf-8")]
