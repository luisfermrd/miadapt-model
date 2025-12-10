import sys
import os

# Ruta del proyecto
PROJECT_PATH = '/home/rparjemb/miadapt.com/backend/python'
sys.path.insert(0, PROJECT_PATH)

# Ruta del virtualenv de Python
VENV_PATH = '/home/rparjemb/virtualenv/miadapt.com/backend/python/3.8'

# Activar el virtualenv correctamente
activate_this = os.path.join(VENV_PATH, 'bin', 'activate_this.py')
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Importar la app FastAPI
from app.main import app as application
