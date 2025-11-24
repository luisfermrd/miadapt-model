"""
Clase para cargar y usar el modelo de recomendación de rutas
"""
import os
import json
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Tuple
from datetime import datetime


class PredictorRutas:
    """Clase para manejar el modelo de recomendación de rutas"""
    
    def __init__(self, modelos_dir: str = "modelos"):
        """
        Inicializa el predictor cargando el modelo, scaler y metadata
        
        Args:
            modelos_dir: Directorio donde están los archivos del modelo
        """
        self.modelos_dir = Path(modelos_dir)
        self.modelo = None
        self.scaler = None
        self.metadata = None
        self.features = None
        self.cargado = False
        
        self._cargar_modelo()
    
    def _cargar_modelo(self):
        """Carga el modelo, scaler y metadata desde los archivos"""
        try:
            # Buscar archivos del modelo
            archivos_modelo = list(self.modelos_dir.glob("modelo_recomendacion_*.pkl"))
            archivos_scaler = list(self.modelos_dir.glob("scaler_*.pkl"))
            archivos_metadata = list(self.modelos_dir.glob("metadata_*.json"))
            
            if not archivos_modelo or not archivos_scaler or not archivos_metadata:
                raise FileNotFoundError(
                    f"No se encontraron los archivos del modelo en {self.modelos_dir}"
                )
            
            # Usar el más reciente si hay múltiples
            archivo_modelo = max(archivos_modelo, key=os.path.getctime)
            archivo_scaler = max(archivos_scaler, key=os.path.getctime)
            archivo_metadata = max(archivos_metadata, key=os.path.getctime)
            
            # Cargar modelo
            with open(archivo_modelo, 'rb') as f:
                self.modelo = pickle.load(f)
            
            # Cargar scaler
            with open(archivo_scaler, 'rb') as f:
                self.scaler = pickle.load(f)
            
            # Cargar metadata
            with open(archivo_metadata, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            
            self.features = self.metadata.get('features', [])
            self.cargado = True
            
        except Exception as e:
            self.cargado = False
            raise Exception(f"Error al cargar el modelo: {str(e)}")
    
    def _preparar_features(self, datos: dict) -> np.ndarray:
        """
        Prepara las features para la predicción según el formato esperado
        
        Args:
            datos: Diccionario con los datos del estudiante
            
        Returns:
            Array numpy con las features preparadas
        """
        from app.utils import calcular_features_derivadas
        
        # Calcular features derivadas
        features_dict = calcular_features_derivadas(datos)
        
        # Crear DataFrame con las features en el orden correcto
        features_df = pd.DataFrame([features_dict])
        
        # Asegurar que todas las features estén presentes
        for feature in self.features:
            if feature not in features_df.columns:
                features_df[feature] = 0.0
        
        # Reordenar columnas según el orden esperado
        features_df = features_df[self.features]
        
        return features_df.values
    
    def predecir(self, datos: dict) -> Tuple[int, float, Dict[str, float]]:
        """
        Realiza una predicción para un estudiante
        
        Args:
            datos: Diccionario con los datos del estudiante
            
        Returns:
            Tupla con (ruta_id, confidence, probabilidades)
        """
        if not self.cargado:
            raise Exception("Modelo no cargado")
        
        try:
            # Preparar features
            features_array = self._preparar_features(datos)
            
            # Aplicar scaler
            features_scaled = self.scaler.transform(features_array)
            
            # Realizar predicción
            prediccion = self.modelo.predict(features_scaled)[0]
            probabilidades = self.modelo.predict_proba(features_scaled)[0]
            
            # Obtener confidence (probabilidad máxima)
            confidence = float(np.max(probabilidades))
            
            # Obtener top 3 probabilidades
            top_indices = np.argsort(probabilidades)[-3:][::-1]
            clases = self.modelo.classes_
            
            prob_dict = {}
            for idx in top_indices:
                prob_dict[str(int(clases[idx]))] = float(probabilidades[idx])
            
            return int(prediccion), confidence, prob_dict
            
        except Exception as e:
            raise Exception(f"Error al realizar la predicción: {str(e)}")
    
    def predecir_batch(self, lista_datos: list) -> list:
        """
        Realiza predicciones para múltiples estudiantes
        
        Args:
            lista_datos: Lista de diccionarios con datos de estudiantes
            
        Returns:
            Lista de tuplas (ruta_id, confidence, probabilidades)
        """
        resultados = []
        for datos in lista_datos:
            try:
                resultado = self.predecir(datos)
                resultados.append(resultado)
            except Exception as e:
                # En caso de error, agregar None para manejar después
                resultados.append(None)
        return resultados
    
    def obtener_info(self) -> dict:
        """
        Obtiene información sobre el modelo cargado
        
        Returns:
            Diccionario con información del modelo
        """
        if not self.cargado:
            return {"error": "Modelo no cargado"}
        
        return {
            "modelo": self.metadata.get("modelo", "Desconocido"),
            "fecha_entrenamiento": self.metadata.get("fecha_entrenamiento", "Desconocida"),
            "metricas": self.metadata.get("metricas", {}),
            "num_features": self.metadata.get("num_features", 0),
            "num_clases": self.metadata.get("num_clases", 0)
        }

