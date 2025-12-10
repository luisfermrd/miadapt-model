#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Flask
"""
import sys
import os

# Añadir el directorio raíz al path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Importar y ejecutar la aplicación
from app.main import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

