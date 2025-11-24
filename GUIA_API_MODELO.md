# Guía para Crear API de Recomendación de Rutas

## 📋 Archivos Necesarios en tu API

Para que tu API funcione, necesitas copiar estos archivos desde la carpeta `modelos/`:

1. **`modelo_recomendacion_[timestamp].pkl`** - El modelo entrenado
2. **`scaler_[timestamp].pkl`** - El normalizador de features
3. **`metadata_[timestamp].json`** - Metadatos del modelo (features, métricas, etc.)

## 🏗️ Estructura Recomendada del Proyecto API

```
tu-proyecto-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Archivo principal de FastAPI
│   ├── models.py            # Modelos Pydantic para validación
│   ├── predictor.py         # Clase para cargar y usar el modelo
│   └── utils.py             # Utilidades auxiliares
├── modelos/                 # Carpeta con los archivos exportados
│   ├── modelo_recomendacion_*.pkl
│   ├── scaler_*.pkl
│   └── metadata_*.json
├── requirements.txt
└── README.md
```

## 📦 Dependencias Necesarias (requirements.txt)

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pandas==2.1.3
numpy==1.26.2
scikit-learn==1.3.2
python-multipart==0.0.6
```

## 🔧 Archivos de Código para tu API

### 1. `app/predictor.py` - Clase para Manejar el Modelo

Este es el archivo MÁS IMPORTANTE. Contiene la lógica para cargar y usar el modelo.

### 2. `app/models.py` - Modelos de Validación

Define los esquemas de entrada y salida de la API.

### 3. `app/main.py` - Endpoints de la API

Define las rutas y endpoints de FastAPI.

## 🚀 Pasos para Implementar

1. Copiar los 3 archivos del modelo a tu proyecto API
2. Instalar dependencias: `pip install -r requirements.txt`
3. Crear los archivos de código según la guía
4. Ejecutar: `uvicorn app.main:app --reload`

## 📡 Endpoints Disponibles y Parámetros

### 1. **GET /** - Información General de la API

**Descripción**: Endpoint raíz que devuelve información sobre la API y los endpoints disponibles.

**Método**: `GET`

**URL**: `http://localhost:8000/`

**Parámetros**: Ninguno

**Respuesta**:
```json
{
  "message": "API de Recomendación de Rutas de Aprendizaje",
  "version": "1.0.0",
  "status": "active",
  "endpoints": {
    "/docs": "Documentación interactiva (Swagger UI)",
    "/redoc": "Documentación alternativa (ReDoc)",
    "/health": "Estado de salud de la API",
    "/predict": "POST - Predecir ruta para un estudiante",
    "/predict/batch": "POST - Predecir rutas para múltiples estudiantes",
    "/model/info": "GET - Información del modelo"
  }
}
```

---

### 2. **GET /health** - Estado de Salud

**Descripción**: Verifica que la API y el modelo estén funcionando correctamente.

**Método**: `GET`

**URL**: `http://localhost:8000/health`

**Parámetros**: Ninguno

**Respuesta Exitosa** (200):
```json
{
  "status": "healthy",
  "modelo_cargado": true,
  "features_esperadas": 45
}
```

**Respuesta de Error** (503):
```json
{
  "detail": "Modelo no disponible"
}
```

---

### 3. **GET /model/info** - Información del Modelo

**Descripción**: Obtiene información detallada sobre el modelo entrenado (métricas, fecha, etc.).

**Método**: `GET`

**URL**: `http://localhost:8000/model/info`

**Parámetros**: Ninguno

**Respuesta**:
```json
{
  "modelo": "RandomForestClassifier",
  "fecha_entrenamiento": "2025-01-27 12:00:00",
  "metricas": {
    "accuracy_train": 0.95,
    "accuracy_val": 0.87,
    "accuracy_test": 0.85
  },
  "num_features": 45,
  "num_clases": 80
}
```

---

### 4. **POST /predict** - Predecir Ruta para un Estudiante

**Descripción**: Endpoint principal para obtener la ruta de aprendizaje recomendada para un estudiante.

**Método**: `POST`

**URL**: `http://localhost:8000/predict`

**Content-Type**: `application/json`

#### Parámetros del Body (JSON):

##### Campos OBLIGATORIOS:

| Campo | Tipo | Rango/Valores | Descripción |
|-------|------|---------------|-------------|
| `porcentaje_diagnostico_inicial` | `float` | 0-100 | Porcentaje de diagnóstico inicial del estudiante |
| `nivel_motivacion` | `int` | 1-9 | Nivel de motivación del estudiante (escala 1-9) |
| `ritmo_aprendizaje` | `string` | "LENTO", "NORMAL", "RAPIDO" | Ritmo de aprendizaje del estudiante |
| `estilo_dominante` | `string` | "VISUAL", "AUDITIVO", "KINESTESICO", "MIXTO" | Estilo de aprendizaje dominante |

##### Campos OPCIONALES (recomendados para mejor precisión):

| Campo | Tipo | Rango | Descripción |
|-------|------|-------|-------------|
| `velocidad_progreso` | `float` | ≥ 0 | Velocidad de progreso del estudiante |
| `ratio_intentos_exitosos` | `float` | 0-1 | Ratio de intentos exitosos (0.0 a 1.0) |
| `mejora_tendencia` | `float` | Cualquiera | Tendencia de mejora (positivo = mejora, negativo = empeora) |
| `estilo_visual` | `float` | 0-100 | Porcentaje de preferencia por estilo visual |
| `estilo_auditivo` | `float` | 0-100 | Porcentaje de preferencia por estilo auditivo |
| `estilo_kinestesico` | `float` | 0-100 | Porcentaje de preferencia por estilo kinestésico |
| `puntuacion_concepto_basico_promedio` | `float` | 0-100 | Puntuación promedio en conceptos básicos |
| `puntuacion_concepto_intermedio_promedio` | `float` | 0-100 | Puntuación promedio en conceptos intermedios |
| `puntuacion_concepto_avanzado_promedio` | `float` | 0-100 | Puntuación promedio en conceptos avanzados |
| `tasa_aciertos_basicos` | `float` | 0-1 | Tasa de aciertos en nivel básico |
| `tasa_aciertos_intermedios` | `float` | 0-1 | Tasa de aciertos en nivel intermedio |
| `tasa_aciertos_avanzados` | `float` | 0-1 | Tasa de aciertos en nivel avanzado |
| `lecciones_completadas` | `int` | ≥ 0 | Número de lecciones completadas |
| `lecciones_totales` | `int` | ≥ 1 | Número total de lecciones disponibles |
| `tiempo_promedio_por_sesion_min` | `float` | ≥ 0 | Tiempo promedio por sesión en minutos |
| `confianza_promedio` | `float` | 0-1 | Confianza promedio del estudiante |

#### Ejemplo de Request:

```json
{
  "porcentaje_diagnostico_inicial": 65.5,
  "nivel_motivacion": 7,
  "ritmo_aprendizaje": "NORMAL",
  "estilo_dominante": "VISUAL",
  "velocidad_progreso": 4.5,
  "ratio_intentos_exitosos": 0.75,
  "mejora_tendencia": 0.15,
  "estilo_visual": 50,
  "estilo_auditivo": 29,
  "estilo_kinestesico": 21,
  "puntuacion_concepto_basico_promedio": 78.3,
  "puntuacion_concepto_intermedio_promedio": 68.9,
  "puntuacion_concepto_avanzado_promedio": 65.9,
  "tasa_aciertos_basicos": 0.78,
  "tasa_aciertos_intermedios": 0.69,
  "tasa_aciertos_avanzados": 0.66,
  "lecciones_completadas": 18,
  "lecciones_totales": 20,
  "tiempo_promedio_por_sesion_min": 27.2,
  "confianza_promedio": 0.61
}
```

#### Ejemplo Mínimo (solo campos obligatorios):

```json
{
  "porcentaje_diagnostico_inicial": 55.0,
  "nivel_motivacion": 5,
  "ritmo_aprendizaje": "NORMAL",
  "estilo_dominante": "AUDITIVO"
}
```

#### Respuesta Exitosa (200):

```json
{
  "success": true,
  "data": {
    "ruta_recomendada_id": 32,
    "ruta_recomendada_nombre": "Ruta Canónica 32 - Desarrollo Intermedio",
    "confidence": 0.85,
    "probabilidades": {
      "32": 0.85,
      "22": 0.10,
      "21": 0.05
    },
    "mensaje": "Ruta recomendada basada en diagnóstico 65.5%, ritmo NORMAL, motivación 7"
  },
  "error": null
}
```

**Campos de la Respuesta**:
- `success` (boolean): Indica si la operación fue exitosa
- `data.ruta_recomendada_id` (int): ID de la ruta recomendada (1-80)
- `data.ruta_recomendada_nombre` (string, opcional): Nombre de la ruta (si está disponible el catálogo)
- `data.confidence` (float, 0-1): Nivel de confianza de la predicción
- `data.probabilidades` (object, opcional): Top 3 rutas más probables con sus probabilidades
- `data.mensaje` (string, opcional): Mensaje descriptivo sobre la recomendación
- `error` (string, null): Mensaje de error si hubo algún problema

#### Respuestas de Error:

**400 Bad Request** - Datos inválidos:
```json
{
  "detail": [
    {
      "loc": ["body", "porcentaje_diagnostico_inicial"],
      "msg": "value is not a valid float",
      "type": "type_error.float"
    }
  ]
}
```

**503 Service Unavailable** - Modelo no disponible:
```json
{
  "detail": "Modelo no disponible. Verifica que los archivos del modelo estén en la carpeta 'modelos/'"
}
```

**500 Internal Server Error** - Error en la predicción:
```json
{
  "detail": "Error al realizar la predicción: [mensaje de error]"
}
```

---

### 5. **POST /predict/batch** - Predecir Rutas para Múltiples Estudiantes

**Descripción**: Permite obtener recomendaciones de rutas para varios estudiantes en una sola petición.

**Método**: `POST`

**URL**: `http://localhost:8000/predict/batch`

**Content-Type**: `application/json`

#### Parámetros del Body (JSON):

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `estudiantes` | `array` | Lista de objetos `DatosEstudiante` (mismos parámetros que `/predict`) |

#### Ejemplo de Request:

```json
{
  "estudiantes": [
    {
      "porcentaje_diagnostico_inicial": 65.5,
      "nivel_motivacion": 7,
      "ritmo_aprendizaje": "NORMAL",
      "estilo_dominante": "VISUAL"
    },
    {
      "porcentaje_diagnostico_inicial": 45.0,
      "nivel_motivacion": 4,
      "ritmo_aprendizaje": "LENTO",
      "estilo_dominante": "AUDITIVO"
    },
    {
      "porcentaje_diagnostico_inicial": 80.0,
      "nivel_motivacion": 8,
      "ritmo_aprendizaje": "RAPIDO",
      "estilo_dominante": "KINESTESICO"
    }
  ]
}
```

#### Respuesta Exitosa (200):

```json
{
  "success": true,
  "total": 3,
  "predicciones": [
    {
      "ruta_recomendada_id": 32,
      "ruta_recomendada_nombre": "Ruta Canónica 32 - Desarrollo Intermedio",
      "confidence": 0.85,
      "probabilidades": {
        "32": 0.85,
        "22": 0.10,
        "21": 0.05
      }
    },
    {
      "ruta_recomendada_id": 15,
      "ruta_recomendada_nombre": "Ruta Canónica 15 - Fundamentos Básicos",
      "confidence": 0.78,
      "probabilidades": {
        "15": 0.78,
        "16": 0.15,
        "14": 0.07
      }
    },
    {
      "ruta_recomendada_id": 45,
      "ruta_recomendada_nombre": "Ruta Canónica 45 - Avanzado Acelerado",
      "confidence": 0.92,
      "probabilidades": {
        "45": 0.92,
        "44": 0.06,
        "46": 0.02
      }
    }
  ]
}
```

---

## 🔧 Cómo Definir un Nuevo Endpoint

Si quieres agregar un nuevo endpoint a la API, sigue este patrón en `app/main.py`:

```python
@app.get("/tu-endpoint")  # o @app.post, @app.put, @app.delete
async def tu_funcion(parametro: TipoParametro):
    """
    Descripción de lo que hace el endpoint.
    
    Args:
        parametro: Descripción del parámetro
        
    Returns:
        Descripción de la respuesta
    """
    try:
        # Tu lógica aquí
        resultado = hacer_algo(parametro)
        
        return {
            "success": True,
            "data": resultado
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )
```

### Tipos de Endpoints en FastAPI:

- **`@app.get("/ruta")`** - Para obtener datos (GET)
- **`@app.post("/ruta")`** - Para crear/enviar datos (POST)
- **`@app.put("/ruta")`** - Para actualizar datos (PUT)
- **`@app.delete("/ruta")`** - Para eliminar datos (DELETE)

### Parámetros en FastAPI:

1. **Query Parameters** (en la URL):
```python
@app.get("/usuarios")
async def obtener_usuarios(limite: int = 10, offset: int = 0):
    # URL: /usuarios?limite=20&offset=0
```

2. **Path Parameters** (en la ruta):
```python
@app.get("/usuarios/{usuario_id}")
async def obtener_usuario(usuario_id: int):
    # URL: /usuarios/123
```

3. **Body Parameters** (en el cuerpo de la petición):
```python
@app.post("/usuarios")
async def crear_usuario(usuario: DatosUsuario):  # Usa un modelo Pydantic
    # Body: JSON con los datos del usuario
```

---

## 📝 Notas Importantes

- El modelo espera exactamente las mismas features que se usaron en el entrenamiento
- El orden de las features debe ser el mismo
- Los datos de entrada deben ser preprocesados igual que en el entrenamiento
- El scaler debe aplicarse antes de hacer predicciones
- Los campos opcionales que no se envíen se rellenarán con valores por defecto (0 o None)
- La validación de datos se realiza automáticamente usando Pydantic
- Los valores fuera de rango generarán errores de validación (400 Bad Request)

---

## 🧪 Ejemplos de Uso

### Con cURL:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "porcentaje_diagnostico_inicial": 65.5,
    "nivel_motivacion": 7,
    "ritmo_aprendizaje": "NORMAL",
    "estilo_dominante": "VISUAL"
  }'
```

### Con Python (requests):

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "porcentaje_diagnostico_inicial": 65.5,
    "nivel_motivacion": 7,
    "ritmo_aprendizaje": "NORMAL",
    "estilo_dominante": "VISUAL"
}

response = requests.post(url, json=data)
resultado = response.json()
print(f"Ruta recomendada: {resultado['data']['ruta_recomendada_id']}")
```

### Con JavaScript (fetch):

```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    porcentaje_diagnostico_inicial: 65.5,
    nivel_motivacion: 7,
    ritmo_aprendizaje: "NORMAL",
    estilo_dominante: "VISUAL"
  })
})
.then(response => response.json())
.then(data => console.log('Ruta recomendada:', data.data.ruta_recomendada_id));
```

---

## 📚 Documentación Interactiva

Una vez que la API esté corriendo, puedes acceder a la documentación interactiva:

- **Swagger UI**: `http://localhost:8000/docs` - Interfaz interactiva para probar endpoints
- **ReDoc**: `http://localhost:8000/redoc` - Documentación alternativa

En estas interfaces podrás:
- Ver todos los endpoints disponibles
- Ver los esquemas de datos (modelos Pydantic)
- Probar los endpoints directamente desde el navegador
- Ver ejemplos de requests y responses

