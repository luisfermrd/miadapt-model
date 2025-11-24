"""
Modelos Pydantic para validación de datos de entrada y salida
"""
from typing import Optional, Dict, List
from pydantic import BaseModel, Field, validator


class DatosEstudiante(BaseModel):
    """Modelo para los datos de entrada de un estudiante"""
    
    # Campos obligatorios
    porcentaje_diagnostico_inicial: float = Field(
        ..., 
        ge=0, 
        le=100, 
        description="Porcentaje de diagnóstico inicial del estudiante (0-100)"
    )
    nivel_motivacion: int = Field(
        ..., 
        ge=1, 
        le=9, 
        description="Nivel de motivación del estudiante (escala 1-9)"
    )
    ritmo_aprendizaje: str = Field(
        ..., 
        description="Ritmo de aprendizaje del estudiante"
    )
    estilo_dominante: str = Field(
        ..., 
        description="Estilo de aprendizaje dominante"
    )
    
    # Campos opcionales
    velocidad_progreso: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        description="Velocidad de progreso del estudiante"
    )
    ratio_intentos_exitosos: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=1, 
        description="Ratio de intentos exitosos (0.0 a 1.0)"
    )
    mejora_tendencia: Optional[float] = Field(
        default=0.0, 
        description="Tendencia de mejora (positivo = mejora, negativo = empeora)"
    )
    estilo_visual: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=100, 
        description="Porcentaje de preferencia por estilo visual"
    )
    estilo_auditivo: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=100, 
        description="Porcentaje de preferencia por estilo auditivo"
    )
    estilo_kinestesico: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=100, 
        description="Porcentaje de preferencia por estilo kinestésico"
    )
    puntuacion_concepto_basico_promedio: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=100, 
        description="Puntuación promedio en conceptos básicos"
    )
    puntuacion_concepto_intermedio_promedio: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=100, 
        description="Puntuación promedio en conceptos intermedios"
    )
    puntuacion_concepto_avanzado_promedio: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=100, 
        description="Puntuación promedio en conceptos avanzados"
    )
    tasa_aciertos_basicos: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=1, 
        description="Tasa de aciertos en nivel básico"
    )
    tasa_aciertos_intermedios: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=1, 
        description="Tasa de aciertos en nivel intermedio"
    )
    tasa_aciertos_avanzados: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=1, 
        description="Tasa de aciertos en nivel avanzado"
    )
    lecciones_completadas: Optional[int] = Field(
        default=0, 
        ge=0, 
        description="Número de lecciones completadas"
    )
    lecciones_totales: Optional[int] = Field(
        default=1, 
        ge=1, 
        description="Número total de lecciones disponibles"
    )
    tiempo_promedio_por_sesion_min: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        description="Tiempo promedio por sesión en minutos"
    )
    confianza_promedio: Optional[float] = Field(
        default=0.0, 
        ge=0, 
        le=1, 
        description="Confianza promedio del estudiante"
    )
    
    @validator('ritmo_aprendizaje')
    def validate_ritmo_aprendizaje(cls, v):
        valores_validos = ['LENTO', 'NORMAL', 'RAPIDO']
        if v.upper() not in valores_validos:
            raise ValueError(f'ritmo_aprendizaje debe ser uno de: {valores_validos}')
        return v.upper()
    
    @validator('estilo_dominante')
    def validate_estilo_dominante(cls, v):
        valores_validos = ['VISUAL', 'AUDITIVO', 'KINESTESICO', 'MIXTO']
        if v.upper() not in valores_validos:
            raise ValueError(f'estilo_dominante debe ser uno de: {valores_validos}')
        return v.upper()
    
    class Config:
        schema_extra = {
            "example": {
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
        }


class PrediccionResponse(BaseModel):
    """Modelo para la respuesta de una predicción"""
    ruta_recomendada_id: int
    ruta_recomendada_nombre: Optional[str] = None
    confidence: float
    probabilidades: Optional[Dict[str, float]] = None
    mensaje: Optional[str] = None


class ResponseModel(BaseModel):
    """Modelo estándar de respuesta de la API"""
    success: bool
    data: Optional[PrediccionResponse] = None
    error: Optional[str] = None


class BatchRequest(BaseModel):
    """Modelo para solicitudes batch"""
    estudiantes: List[DatosEstudiante]


class BatchResponse(BaseModel):
    """Modelo para respuestas batch"""
    success: bool
    total: int
    predicciones: List[PrediccionResponse]

