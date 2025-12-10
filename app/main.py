"""
API principal de Recomendación de Rutas de Aprendizaje
"""
from flask import Flask, request, jsonify
from app.models import (
    DatosEstudiante, 
    ResponseModel, 
    PrediccionResponse,
    BatchRequest,
    BatchResponse
)
from app.predictor import PredictorRutas
from app.utils import obtener_nombre_ruta
from pydantic import ValidationError
import os

# Inicializar Flask
app = Flask(__name__)

# Exportar como 'application' para Passenger
application = app

# Cargar predictor al iniciar la aplicación
predictor = None
try:
    modelos_dir = os.getenv("MODELOS_DIR", "modelos")
    predictor = PredictorRutas(modelos_dir=modelos_dir)
except Exception as e:
    print(f"Advertencia: No se pudo cargar el modelo al iniciar: {str(e)}")
    predictor = None


@app.route("/", methods=["GET"])
def root():
    """
    Endpoint raíz que devuelve información sobre la API
    """
    return jsonify({
        "message": "API de Recomendación de Rutas de Aprendizaje",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "/": "Información de la API",
            "/ping": "Endpoint de prueba",
            "/health": "Estado de salud de la API",
            "/predict": "POST - Predecir ruta para un estudiante",
            "/predict/batch": "POST - Predecir rutas para múltiples estudiantes",
            "/model/info": "GET - Información del modelo"
        }
    })


@app.route("/ping", methods=["GET"])
def ping():
    """
    Endpoint de prueba para verificar que la API está funcionando
    """
    return jsonify({"message": "pong"})


@app.route("/health", methods=["GET"])
def health_check():
    """
    Verifica que la API y el modelo estén funcionando correctamente
    """
    if predictor is None or not predictor.cargado:
        return jsonify({
            "status": "unhealthy",
            "modelo_cargado": False,
            "error": "Modelo no disponible"
        }), 503
    
    return jsonify({
        "status": "healthy",
        "modelo_cargado": predictor.cargado,
        "features_esperadas": predictor.metadata.get("num_features", 0) if predictor.metadata else 0
    })


@app.route("/model/info", methods=["GET"])
def model_info():
    """
    Obtiene información detallada sobre el modelo entrenado
    """
    if predictor is None or not predictor.cargado:
        return jsonify({
            "error": "Modelo no disponible. Verifica que los archivos del modelo estén en la carpeta 'modelos/'"
        }), 503
    
    info = predictor.obtener_info()
    return jsonify(info)


@app.route("/predict", methods=["POST"])
def predecir_ruta():
    """
    Endpoint principal para obtener la ruta de aprendizaje recomendada para un estudiante
    
    Returns:
        Respuesta con la ruta recomendada y detalles de la predicción
    """
    if predictor is None or not predictor.cargado:
        return jsonify({
            "success": False,
            "error": "Modelo no disponible. Verifica que los archivos del modelo estén en la carpeta 'modelos/'"
        }), 503
    
    try:
        # Validar datos de entrada con Pydantic
        datos_json = request.get_json()
        if not datos_json:
            return jsonify({
                "success": False,
                "error": "No se proporcionaron datos JSON"
            }), 400
        
        estudiante = DatosEstudiante(**datos_json)
        
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
        
        return jsonify(ResponseModel(
            success=True,
            data=prediccion_response,
            error=None
        ).dict())
        
    except ValidationError as e:
        return jsonify({
            "success": False,
            "error": f"Error de validación: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al realizar la predicción: {str(e)}"
        }), 500


@app.route("/predict/batch", methods=["POST"])
def predecir_rutas_batch():
    """
    Permite obtener recomendaciones de rutas para varios estudiantes en una sola petición
    
    Returns:
        Respuesta con predicciones para todos los estudiantes
    """
    if predictor is None or not predictor.cargado:
        return jsonify({
            "success": False,
            "error": "Modelo no disponible. Verifica que los archivos del modelo estén en la carpeta 'modelos/'"
        }), 503
    
    try:
        # Validar datos de entrada con Pydantic
        datos_json = request.get_json()
        if not datos_json:
            return jsonify({
                "success": False,
                "error": "No se proporcionaron datos JSON"
            }), 400
        
        batch_request = BatchRequest(**datos_json)
        
        # Convertir lista de modelos Pydantic a diccionarios
        lista_datos = [estudiante.dict() for estudiante in batch_request.estudiantes]
        
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
        
        return jsonify(BatchResponse(
            success=True,
            total=len(predicciones),
            predicciones=predicciones
        ).dict())
        
    except ValidationError as e:
        return jsonify({
            "success": False,
            "error": f"Error de validación: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al realizar las predicciones: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
