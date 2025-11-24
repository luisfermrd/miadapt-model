# Documentación del Endpoint de Predicción

## POST /predict

Endpoint principal para obtener la ruta de aprendizaje recomendada para un estudiante basándose en sus características y desempeño.

---

## 📍 URL

```
POST http://localhost:8000/predict
```

---

## 📋 Descripción

Este endpoint analiza las características de un estudiante y devuelve la ruta de aprendizaje más adecuada para su perfil. El modelo utiliza un algoritmo de Machine Learning (Random Forest) entrenado con datos históricos para realizar la recomendación.

---

## 🔧 Parámetros de Entrada

### Headers

| Header | Valor Requerido | Descripción |
|--------|----------------|-------------|
| `Content-Type` | `application/json` | Tipo de contenido de la petición |

### Body (JSON)

El body debe ser un objeto JSON con los datos del estudiante. Los campos se dividen en **obligatorios** y **opcionales**.

#### ✅ Campos Obligatorios

Estos campos son **requeridos** para realizar la predicción:

| Campo | Tipo | Rango/Valores | Descripción | Ejemplo |
|-------|------|---------------|-------------|---------|
| `porcentaje_diagnostico_inicial` | `float` | 0 - 100 | Porcentaje obtenido en el diagnóstico inicial del estudiante | `65.5` |
| `nivel_motivacion` | `int` | 1 - 9 | Nivel de motivación del estudiante en escala del 1 al 9 | `7` |
| `ritmo_aprendizaje` | `string` | `"LENTO"`, `"NORMAL"`, `"RAPIDO"` | Ritmo de aprendizaje del estudiante | `"NORMAL"` |
| `estilo_dominante` | `string` | `"VISUAL"`, `"AUDITIVO"`, `"KINESTESICO"`, `"MIXTO"` | Estilo de aprendizaje dominante | `"VISUAL"` |

#### 📊 Campos Opcionales

Estos campos son **opcionales** pero se recomienda incluirlos para obtener predicciones más precisas:

| Campo | Tipo | Rango | Descripción | Ejemplo |
|-------|------|-------|-------------|---------|
| `velocidad_progreso` | `float` | ≥ 0 | Velocidad de progreso del estudiante | `4.5` |
| `ratio_intentos_exitosos` | `float` | 0.0 - 1.0 | Ratio de intentos exitosos (0.0 = 0%, 1.0 = 100%) | `0.75` |
| `mejora_tendencia` | `float` | Cualquiera | Tendencia de mejora (positivo = mejora, negativo = empeora) | `0.15` |
| `estilo_visual` | `float` | 0 - 100 | Porcentaje de preferencia por estilo visual | `50.0` |
| `estilo_auditivo` | `float` | 0 - 100 | Porcentaje de preferencia por estilo auditivo | `29.0` |
| `estilo_kinestesico` | `float` | 0 - 100 | Porcentaje de preferencia por estilo kinestésico | `21.0` |
| `puntuacion_concepto_basico_promedio` | `float` | 0 - 100 | Puntuación promedio en conceptos básicos | `78.3` |
| `puntuacion_concepto_intermedio_promedio` | `float` | 0 - 100 | Puntuación promedio en conceptos intermedios | `68.9` |
| `puntuacion_concepto_avanzado_promedio` | `float` | 0 - 100 | Puntuación promedio en conceptos avanzados | `65.9` |
| `tasa_aciertos_basicos` | `float` | 0.0 - 1.0 | Tasa de aciertos en nivel básico | `0.78` |
| `tasa_aciertos_intermedios` | `float` | 0.0 - 1.0 | Tasa de aciertos en nivel intermedio | `0.69` |
| `tasa_aciertos_avanzados` | `float` | 0.0 - 1.0 | Tasa de aciertos en nivel avanzado | `0.66` |
| `lecciones_completadas` | `int` | ≥ 0 | Número de lecciones completadas | `18` |
| `lecciones_totales` | `int` | ≥ 1 | Número total de lecciones disponibles | `20` |
| `tiempo_promedio_por_sesion_min` | `float` | ≥ 0 | Tiempo promedio por sesión en minutos | `27.2` |
| `confianza_promedio` | `float` | 0.0 - 1.0 | Confianza promedio del estudiante | `0.61` |

---

## 📤 Ejemplos de Request

### Ejemplo 1: Request Mínimo (Solo Campos Obligatorios)

```json
{
  "porcentaje_diagnostico_inicial": 55.0,
  "nivel_motivacion": 5,
  "ritmo_aprendizaje": "NORMAL",
  "estilo_dominante": "AUDITIVO"
}
```

### Ejemplo 2: Request Completo (Con Todos los Campos)

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

### Ejemplo 3: Estudiante con Ritmo Lento

```json
{
  "porcentaje_diagnostico_inicial": 45.0,
  "nivel_motivacion": 4,
  "ritmo_aprendizaje": "LENTO",
  "estilo_dominante": "AUDITIVO",
  "velocidad_progreso": 2.1,
  "ratio_intentos_exitosos": 0.55,
  "confianza_promedio": 0.45
}
```

### Ejemplo 4: Estudiante con Ritmo Rápido

```json
{
  "porcentaje_diagnostico_inicial": 80.0,
  "nivel_motivacion": 8,
  "ritmo_aprendizaje": "RAPIDO",
  "estilo_dominante": "KINESTESICO",
  "velocidad_progreso": 6.8,
  "ratio_intentos_exitosos": 0.88,
  "mejora_tendencia": 0.25,
  "confianza_promedio": 0.82
}
```

---

## 📥 Respuestas

### ✅ Respuesta Exitosa (200 OK)

Cuando la predicción se realiza correctamente, la API devuelve un objeto JSON con la siguiente estructura:

```json
{
  "success": true,
  "data": {
    "ruta_recomendada_id": 32,
    "ruta_recomendada_nombre": "Ruta Canónica 32",
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

#### Campos de la Respuesta Exitosa

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `success` | `boolean` | Indica si la operación fue exitosa. Siempre será `true` en respuestas exitosas |
| `data` | `object` | Objeto con los datos de la predicción |
| `data.ruta_recomendada_id` | `int` | ID de la ruta recomendada (rango típico: 1-80, puede variar según el modelo) |
| `data.ruta_recomendada_nombre` | `string` \| `null` | Nombre descriptivo de la ruta (si está disponible) |
| `data.confidence` | `float` | Nivel de confianza de la predicción (0.0 - 1.0). Valores más altos indican mayor certeza |
| `data.probabilidades` | `object` \| `null` | Objeto con las top 3 rutas más probables y sus probabilidades. Las claves son los IDs de ruta (como strings) y los valores son las probabilidades (0.0 - 1.0) |
| `data.mensaje` | `string` \| `null` | Mensaje descriptivo sobre la recomendación |
| `error` | `null` | Siempre será `null` en respuestas exitosas |

#### Interpretación de la Confianza

- **0.9 - 1.0**: Muy alta confianza. La recomendación es muy precisa.
- **0.7 - 0.9**: Alta confianza. La recomendación es confiable.
- **0.5 - 0.7**: Confianza moderada. La recomendación es razonable pero podría haber alternativas.
- **< 0.5**: Baja confianza. Considerar revisar los datos de entrada o consultar alternativas.

---

### ❌ Respuestas de Error

#### 400 Bad Request - Datos Inválidos

Ocurre cuando los datos enviados no cumplen con las validaciones (valores fuera de rango, tipos incorrectos, etc.).

**Ejemplo de Error:**

```json
{
  "detail": [
    {
      "loc": ["body", "porcentaje_diagnostico_inicial"],
      "msg": "ensure this value is less than or equal to 100",
      "type": "value_error.number.not_le",
      "ctx": {"limit_value": 100}
    }
  ]
}
```

**Causas Comunes:**
- Valores fuera del rango permitido (ej: `porcentaje_diagnostico_inicial > 100`)
- Tipos de datos incorrectos (ej: enviar string en lugar de número)
- Valores de enum inválidos (ej: `ritmo_aprendizaje: "MEDIO"` en lugar de `"NORMAL"`)
- Campos obligatorios faltantes

#### 503 Service Unavailable - Modelo No Disponible

Ocurre cuando el modelo no está cargado o no se encuentra disponible.

**Ejemplo de Error:**

```json
{
  "detail": "Modelo no disponible. Verifica que los archivos del modelo estén en la carpeta 'modelos/'"
}
```

**Solución:**
- Verificar que los archivos del modelo (`modelo_recomendacion_*.pkl`, `scaler_*.pkl`, `metadata_*.json`) estén en la carpeta `modelos/`
- Verificar que la API esté corriendo correctamente
- Consultar el endpoint `/health` para verificar el estado

#### 500 Internal Server Error - Error en la Predicción

Ocurre cuando hay un error interno durante el procesamiento de la predicción.

**Ejemplo de Error:**

```json
{
  "detail": "Error al realizar la predicción: [mensaje de error específico]"
}
```

**Causas Posibles:**
- Error al procesar las features
- Error al aplicar el scaler
- Error en el modelo de Machine Learning
- Problemas con el formato de los datos

---

## 🔍 Ejemplos de Uso

### Con cURL

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

### Con Python (requests)

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "porcentaje_diagnostico_inicial": 65.5,
    "nivel_motivacion": 7,
    "ritmo_aprendizaje": "NORMAL",
    "estilo_dominante": "VISUAL",
    "velocidad_progreso": 4.5,
    "ratio_intentos_exitosos": 0.75
}

response = requests.post(url, json=data)
resultado = response.json()

if resultado["success"]:
    ruta_id = resultado["data"]["ruta_recomendada_id"]
    confidence = resultado["data"]["confidence"]
    print(f"Ruta recomendada: {ruta_id} (Confianza: {confidence:.2%})")
else:
    print(f"Error: {resultado['error']}")
```

### Con JavaScript (fetch)

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
.then(data => {
  if (data.success) {
    console.log('Ruta recomendada:', data.data.ruta_recomendada_id);
    console.log('Confianza:', data.data.confidence);
  } else {
    console.error('Error:', data.error);
  }
})
.catch(error => console.error('Error:', error));
```

### Con Node.js (axios)

```javascript
const axios = require('axios');

const data = {
  porcentaje_diagnostico_inicial: 65.5,
  nivel_motivacion: 7,
  ritmo_aprendizaje: "NORMAL",
  estilo_dominante: "VISUAL"
};

axios.post('http://localhost:8000/predict', data)
  .then(response => {
    const resultado = response.data;
    if (resultado.success) {
      console.log(`Ruta recomendada: ${resultado.data.ruta_recomendada_id}`);
      console.log(`Confianza: ${(resultado.data.confidence * 100).toFixed(2)}%`);
    }
  })
  .catch(error => {
    console.error('Error:', error.response?.data || error.message);
  });
```

---

## ⚠️ Notas Importantes

1. **Valores por Defecto**: Los campos opcionales que no se envíen se rellenarán automáticamente con valores por defecto (generalmente 0.0 o 0).

2. **Precisión de la Predicción**: Incluir más campos opcionales generalmente mejora la precisión de la predicción, ya que el modelo tiene más información para tomar la decisión.

3. **Validación Automática**: La API valida automáticamente todos los datos de entrada usando Pydantic. Los valores fuera de rango o tipos incorrectos generarán errores 400.

4. **Case Sensitivity**: Los valores de `ritmo_aprendizaje` y `estilo_dominante` son case-insensitive, pero se recomienda usar mayúsculas como se muestra en los ejemplos.

5. **IDs de Ruta**: Los IDs de ruta recomendados pueden variar según el modelo entrenado. Consulta el endpoint `/model/info` para conocer el rango de IDs disponibles.

6. **Probabilidades**: El campo `probabilidades` muestra las top 3 rutas más probables. Esto es útil para ofrecer alternativas al estudiante si la ruta principal no es adecuada.

---

## 🔗 Endpoints Relacionados

- **GET /health** - Verificar el estado de la API y el modelo
- **GET /model/info** - Obtener información sobre el modelo entrenado
- **POST /predict/batch** - Realizar predicciones para múltiples estudiantes

---

## 📚 Documentación Adicional

Para más información sobre la API completa, consulta:
- `GUIA_API_MODELO.md` - Guía completa de la API
- `README.md` - Documentación general del proyecto
- `http://localhost:8000/docs` - Documentación interactiva (Swagger UI)

