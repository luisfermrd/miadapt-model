"""
API principal de Recomendación de Rutas de Aprendizaje
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from app.models import (
    DatosEstudiante, 
    ResponseModel, 
    PrediccionResponse,
    BatchRequest,
    BatchResponse
)
from app.predictor import PredictorRutas
from app.utils import obtener_nombre_ruta
import os

# Inicializar FastAPI
app = FastAPI(
    title="API de Recomendación de Rutas de Aprendizaje",
    description="API para recomendar rutas de aprendizaje personalizadas basadas en características del estudiante",
    version="1.0.0"
)

# Inicializar predictor (se carga al iniciar la aplicación)
predictor = None

@app.on_event("startup")
async def startup_event():
    """Carga el modelo al iniciar la aplicación"""
    global predictor
    try:
        modelos_dir = os.getenv("MODELOS_DIR", "modelos")
        predictor = PredictorRutas(modelos_dir=modelos_dir)
    except Exception as e:
        print(f"Advertencia: No se pudo cargar el modelo al iniciar: {str(e)}")
        predictor = None


@app.get("/", tags=["General"])
async def root():
    """
    Endpoint raíz que devuelve información sobre la API
    """
    return {
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


@app.get("/health", tags=["General"])
async def health_check():
    """
    Verifica que la API y el modelo estén funcionando correctamente
    """
    if predictor is None or not predictor.cargado:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo no disponible"
        )
    
    return {
        "status": "healthy",
        "modelo_cargado": predictor.cargado,
        "features_esperadas": predictor.metadata.get("num_features", 0) if predictor.metadata else 0
    }


@app.get("/model/info", tags=["Modelo"])
async def model_info():
    """
    Obtiene información detallada sobre el modelo entrenado
    """
    if predictor is None or not predictor.cargado:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo no disponible. Verifica que los archivos del modelo estén en la carpeta 'modelos/'"
        )
    
    info = predictor.obtener_info()
    return info


@app.post("/predict", response_model=ResponseModel, tags=["Predicción"])
async def predecir_ruta(estudiante: DatosEstudiante):
    """
    Endpoint principal para obtener la ruta de aprendizaje recomendada para un estudiante
    
    Args:
        estudiante: Datos del estudiante para la predicción
        
    Returns:
        Respuesta con la ruta recomendada y detalles de la predicción
    """
    if predictor is None or not predictor.cargado:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo no disponible. Verifica que los archivos del modelo estén en la carpeta 'modelos/'"
        )
    
    try:
        # Convertir modelo Pydantic a diccionario
        datos_estudiante = estudiante.dict()
        
        # Realizar predicción
        ruta_id, confidence, probabilidades = predictor.predecir(datos_estudiante)
        
        # Obtener nombre de la ruta
        ruta_nombre = obtener_nombre_ruta(ruta_id)
        
        # Crear mensaje descriptivo
        mensaje = (
            f"Ruta recomendada basada en diagnóstico {datos_estudiante['porcentaje_diagnostico_inicial']}%, "
            f"ritmo {datos_estudiante['ritmo_aprendizaje']}, motivación {datos_estudiante['nivel_motivacion']}"
        )
        
        # Crear respuesta
        prediccion_response = PrediccionResponse(
            ruta_recomendada_id=ruta_id,
            ruta_recomendada_nombre=ruta_nombre,
            confidence=confidence,
            probabilidades=probabilidades,
            mensaje=mensaje
        )
        
        return ResponseModel(
            success=True,
            data=prediccion_response,
            error=None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar la predicción: {str(e)}"
        )


@app.post("/predict/batch", response_model=BatchResponse, tags=["Predicción"])
async def predecir_rutas_batch(request: BatchRequest):
    """
    Permite obtener recomendaciones de rutas para varios estudiantes en una sola petición
    
    Args:
        request: Objeto con lista de estudiantes
        
    Returns:
        Respuesta con predicciones para todos los estudiantes
    """
    if predictor is None or not predictor.cargado:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo no disponible. Verifica que los archivos del modelo estén en la carpeta 'modelos/'"
        )
    
    try:
        # Convertir lista de modelos Pydantic a diccionarios
        lista_datos = [estudiante.dict() for estudiante in request.estudiantes]
        
        # Realizar predicciones
        resultados = predictor.predecir_batch(lista_datos)
        
        # Formatear respuestas
        predicciones = []
        for i, resultado in enumerate(resultados):
            if resultado is None:
                # Si hubo error en una predicción, crear respuesta de error
                predicciones.append(
                    PrediccionResponse(
                        ruta_recomendada_id=-1,
                        ruta_recomendada_nombre="Error en predicción",
                        confidence=0.0,
                        probabilidades=None,
                        mensaje=f"Error al procesar estudiante {i+1}"
                    )
                )
            else:
                ruta_id, confidence, probabilidades = resultado
                ruta_nombre = obtener_nombre_ruta(ruta_id)
                
                predicciones.append(
                    PrediccionResponse(
                        ruta_recomendada_id=ruta_id,
                        ruta_recomendada_nombre=ruta_nombre,
                        confidence=confidence,
                        probabilidades=probabilidades
                    )
                )
        
        return BatchResponse(
            success=True,
            total=len(predicciones),
            predicciones=predicciones
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar las predicciones: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

