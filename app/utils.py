"""
Utilidades auxiliares para el procesamiento de datos
"""
from typing import Dict


def calcular_features_derivadas(datos: Dict) -> Dict:
    """
    Calcula las features derivadas necesarias para el modelo
    basándose en los datos de entrada del estudiante
    
    Args:
        datos: Diccionario con los datos del estudiante
        
    Returns:
        Diccionario con todas las features necesarias para el modelo
    """
    # Inicializar diccionario de features
    features = {}
    
    # Features básicas directas
    features['porcentaje_diagnostico_inicial'] = datos.get('porcentaje_diagnostico_inicial', 0.0)
    features['nivel_motivacion'] = datos.get('nivel_motivacion', 0)
    features['velocidad_progreso'] = datos.get('velocidad_progreso', 0.0)
    features['ratio_intentos_exitosos'] = datos.get('ratio_intentos_exitosos', 0.0)
    features['mejora_tendencia'] = datos.get('mejora_tendencia', 0.0)
    features['tiempo_promedio_por_sesion_min'] = datos.get('tiempo_promedio_por_sesion_min', 0.0)
    features['confianza_promedio'] = datos.get('confianza_promedio', 0.0)
    
    # Normalizar estilos de aprendizaje (si suman más de 100, normalizar)
    estilo_visual = datos.get('estilo_visual', 0.0)
    estilo_auditivo = datos.get('estilo_auditivo', 0.0)
    estilo_kinestesico = datos.get('estilo_kinestesico', 0.0)
    
    suma_estilos = estilo_visual + estilo_auditivo + estilo_kinestesico
    if suma_estilos > 0:
        features['estilo_visual_norm'] = estilo_visual / suma_estilos
        features['estilo_auditivo_norm'] = estilo_auditivo / suma_estilos
        features['estilo_kinestesico_norm'] = estilo_kinestesico / suma_estilos
    else:
        # Si no se proporcionan, usar valores por defecto basados en estilo_dominante
        estilo_dominante = datos.get('estilo_dominante', 'MIXTO').upper()
        if estilo_dominante == 'VISUAL':
            features['estilo_visual_norm'] = 1.0
            features['estilo_auditivo_norm'] = 0.0
            features['estilo_kinestesico_norm'] = 0.0
        elif estilo_dominante == 'AUDITIVO':
            features['estilo_visual_norm'] = 0.0
            features['estilo_auditivo_norm'] = 1.0
            features['estilo_kinestesico_norm'] = 0.0
        elif estilo_dominante == 'KINESTESICO':
            features['estilo_visual_norm'] = 0.0
            features['estilo_auditivo_norm'] = 0.0
            features['estilo_kinestesico_norm'] = 1.0
        else:  # MIXTO
            features['estilo_visual_norm'] = 0.33
            features['estilo_auditivo_norm'] = 0.33
            features['estilo_kinestesico_norm'] = 0.34
    
    # Calcular desempeño promedio
    punt_basico = datos.get('puntuacion_concepto_basico_promedio', 0.0)
    punt_intermedio = datos.get('puntuacion_concepto_intermedio_promedio', 0.0)
    punt_avanzado = datos.get('puntuacion_concepto_avanzado_promedio', 0.0)
    
    num_puntuaciones = sum([1 for x in [punt_basico, punt_intermedio, punt_avanzado] if x > 0])
    if num_puntuaciones > 0:
        features['desempeno_promedio'] = (punt_basico + punt_intermedio + punt_avanzado) / num_puntuaciones
    else:
        features['desempeno_promedio'] = datos.get('porcentaje_diagnostico_inicial', 0.0)
    
    # Calcular tasa de éxito general
    tasa_basicos = datos.get('tasa_aciertos_basicos', 0.0)
    tasa_intermedios = datos.get('tasa_aciertos_intermedios', 0.0)
    tasa_avanzados = datos.get('tasa_aciertos_avanzados', 0.0)
    
    num_tasas = sum([1 for x in [tasa_basicos, tasa_intermedios, tasa_avanzados] if x > 0])
    if num_tasas > 0:
        features['tasa_exito_general'] = (tasa_basicos + tasa_intermedios + tasa_avanzados) / num_tasas
    else:
        features['tasa_exito_general'] = datos.get('ratio_intentos_exitosos', 0.0)
    
    # Calcular experiencia (basada en lecciones completadas)
    lecciones_completadas = datos.get('lecciones_completadas', 0)
    lecciones_totales = datos.get('lecciones_totales', 1)
    features['experiencia'] = lecciones_completadas / max(lecciones_totales, 1)
    
    # One-hot encoding para ritmo_aprendizaje
    ritmo = datos.get('ritmo_aprendizaje', 'NORMAL').upper()
    features['ritmo_aprendizaje_LENTO'] = 1.0 if ritmo == 'LENTO' else 0.0
    features['ritmo_aprendizaje_NORMAL'] = 1.0 if ritmo == 'NORMAL' else 0.0
    features['ritmo_aprendizaje_RAPIDO'] = 1.0 if ritmo == 'RAPIDO' else 0.0
    
    # One-hot encoding para nivel_diagnostico_cat
    porcentaje_diag = datos.get('porcentaje_diagnostico_inicial', 0.0)
    if porcentaje_diag < 40:
        nivel_diag = 'BAJO'
    elif porcentaje_diag < 70:
        nivel_diag = 'MEDIO'
    else:
        nivel_diag = 'ALTO'
    
    features['nivel_diagnostico_cat_ALTO'] = 1.0 if nivel_diag == 'ALTO' else 0.0
    features['nivel_diagnostico_cat_BAJO'] = 1.0 if nivel_diag == 'BAJO' else 0.0
    features['nivel_diagnostico_cat_MEDIO'] = 1.0 if nivel_diag == 'MEDIO' else 0.0
    
    # One-hot encoding para nivel_motivacion_cat
    nivel_mot = datos.get('nivel_motivacion', 5)
    if nivel_mot <= 6:
        nivel_mot_cat = 'MEDIA'
    else:
        nivel_mot_cat = 'ALTA'
    
    features['nivel_motivacion_cat_ALTA'] = 1.0 if nivel_mot_cat == 'ALTA' else 0.0
    features['nivel_motivacion_cat_MEDIA'] = 1.0 if nivel_mot_cat == 'MEDIA' else 0.0
    
    # One-hot encoding para estilo_dominante
    estilo_dom = datos.get('estilo_dominante', 'MIXTO').upper()
    features['estilo_dominante_AUDITIVO'] = 1.0 if estilo_dom == 'AUDITIVO' else 0.0
    features['estilo_dominante_KINESTESICO'] = 1.0 if estilo_dom == 'KINESTESICO' else 0.0
    features['estilo_dominante_MIXTO'] = 1.0 if estilo_dom == 'MIXTO' else 0.0
    features['estilo_dominante_VISUAL'] = 1.0 if estilo_dom == 'VISUAL' else 0.0
    
    return features


def obtener_nombre_ruta(ruta_id: int) -> str:
    """
    Obtiene el nombre de una ruta basándose en su ID
    (Puede ser expandido con un catálogo de rutas)
    
    Args:
        ruta_id: ID de la ruta
        
    Returns:
        Nombre de la ruta
    """
    # Por ahora retornamos un nombre genérico
    # Esto puede ser expandido con un catálogo real de rutas
    return f"Ruta Canónica {ruta_id}"

