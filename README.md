# API de Recomendación de Rutas de Aprendizaje

API REST desarrollada con FastAPI para recomendar rutas de aprendizaje personalizadas basadas en características del estudiante.

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Verificar archivos del modelo

Asegúrate de que los siguientes archivos estén en la carpeta `modelos/`:
- `modelo_recomendacion_*.pkl`
- `scaler_*.pkl`
- `metadata_*.json`

### 3. Ejecutar la API

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación

Una vez que la API esté corriendo, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs` - Documentación interactiva
- **ReDoc**: `http://localhost:8000/redoc` - Documentación alternativa

## 📡 Endpoints Disponibles

### GET `/`
Información general de la API y endpoints disponibles.

### GET `/health`
Verifica el estado de salud de la API y el modelo.

### GET `/model/info`
Obtiene información detallada sobre el modelo entrenado.

### POST `/predict`
Predice la ruta de aprendizaje recomendada para un estudiante.

**Ejemplo de request:**
```json
{
  "porcentaje_diagnostico_inicial": 65.5,
  "nivel_motivacion": 7,
  "ritmo_aprendizaje": "NORMAL",
  "estilo_dominante": "VISUAL"
}
```

### POST `/predict/batch`
Predice rutas para múltiples estudiantes en una sola petición.

**Ejemplo de request:**
```json
{
  "estudiantes": [
    {
      "porcentaje_diagnostico_inicial": 65.5,
      "nivel_motivacion": 7,
      "ritmo_aprendizaje": "NORMAL",
      "estilo_dominante": "VISUAL"
    }
  ]
}
```

## 📖 Documentación Completa

Para más detalles sobre los parámetros, ejemplos y respuestas, consulta el archivo `GUIA_API_MODELO.md`.

## 🏗️ Estructura del Proyecto

```
miadapt-predictor-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Archivo principal de FastAPI
│   ├── models.py            # Modelos Pydantic para validación
│   ├── predictor.py         # Clase para cargar y usar el modelo
│   └── utils.py             # Utilidades auxiliares
├── modelos/                 # Carpeta con los archivos del modelo
│   ├── modelo_recomendacion_*.pkl
│   ├── scaler_*.pkl
│   └── metadata_*.json
├── requirements.txt
├── README.md
└── GUIA_API_MODELO.md
```

## 🔧 Configuración

Puedes configurar el directorio de modelos usando la variable de entorno `MODELOS_DIR`:

```bash
export MODELOS_DIR="modelos"
uvicorn app.main:app --reload
```

Por defecto, se usa la carpeta `modelos/` en el directorio raíz.

## 📝 Notas

- El modelo espera exactamente las mismas features que se usaron en el entrenamiento
- Los campos opcionales que no se envíen se rellenarán con valores por defecto
- La validación de datos se realiza automáticamente usando Pydantic

