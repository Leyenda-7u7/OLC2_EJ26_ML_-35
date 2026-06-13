"""
Motor principal CreditGuard.
Coordina carga, limpieza, entrenamiento, evaluación y predicción.
"""

from app.ml.constants import COLUMNAS_NUMERICAS

from app.ml.preprocessing import (
    cargar_csv,
    limpiar_datos,
    normalizar_datos,
    normalizar_solicitante,
    dividir_datos_estratificado,
    datos_a_matrices,
)

from app.ml.model import RandomForestCreditGuard
from app.ml.metrics import calcular_metricas
from app.ml.validation import validar_hiperparametros, validar_solicitante


class CreditGuardEngine:
    """
    Orquesta el flujo completo:
    carga → limpieza → normalización → entrenamiento → evaluación → predicción.
    """

    def __init__(self):
        self.modelo = RandomForestCreditGuard()

        self.datos_raw = None
        self.datos_limpios = None
        self.reporte_limpieza = None

        self.ruta_csv_original = None
        self.ruta_datos_limpios = None

        self.datos_normalizados = None
        self.params_norm = None

        self.entrenamiento = None
        self.prueba = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.metricas = None
        self.listo_para_predecir = False

    def cargar_y_limpiar(self, ruta_csv=None, contenido_csv=None):
        """
        Carga un CSV, limpia los datos y guarda internamente los datos limpios.
        """
        self.datos_raw = cargar_csv(
            ruta_archivo=ruta_csv,
            contenido_csv=contenido_csv,
        )

        datos_limpios, reporte = limpiar_datos(self.datos_raw)

        if len(datos_limpios) == 0:
            raise ValueError("Después de la limpieza no quedaron registros válidos.")

        self.datos_limpios = datos_limpios
        self.reporte_limpieza = reporte

        self.datos_normalizados = None
        self.params_norm = None
        self.entrenamiento = None
        self.prueba = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.metricas = None
        self.listo_para_predecir = False

        return {
            "mensaje": "Datos cargados y limpiados correctamente.",
            "reporte": self.reporte_limpieza,
        }

    def entrenar(self, n_arboles=100, max_depth=10, max_leaves=50):
        """
        Normaliza, divide, entrena y evalúa el modelo usando los datos limpios.
        """
        if self.datos_limpios is None:
            raise RuntimeError("Primero debes cargar y limpiar un CSV.")

        validar_hiperparametros(n_arboles, max_depth, max_leaves)

        if len(self.datos_limpios) < 10:
            raise ValueError("Se necesitan al menos 10 registros limpios para entrenar.")

        self.datos_normalizados, self.params_norm = normalizar_datos(
            self.datos_limpios
        )

        self.entrenamiento, self.prueba = dividir_datos_estratificado(
            self.datos_normalizados,
            proporcion_entrenamiento=0.8,
            semilla=42,
        )

        if len(self.entrenamiento) == 0 or len(self.prueba) == 0:
            raise ValueError("No se pudo dividir el dataset en entrenamiento y prueba.")

        self.X_train, self.y_train = datos_a_matrices(self.entrenamiento)
        self.X_test, self.y_test = datos_a_matrices(self.prueba)

        self.modelo.reentrenar(
            self.X_train,
            self.y_train,
            n_arboles=n_arboles,
            max_depth=max_depth,
            max_leaves=max_leaves,
        )

        y_pred = self.modelo.predecir(self.X_test)

        self.metricas = calcular_metricas(self.y_test, y_pred)
        self.listo_para_predecir = True

        return {
            "mensaje": "Modelo entrenado correctamente.",
            "metricas": self.metricas,
            "resumen_datos": {
                "total_limpio": len(self.datos_limpios),
                "entrenamiento": len(self.X_train),
                "prueba": len(self.X_test),
                "clase_0_train": self.y_train.count(0),
                "clase_1_train": self.y_train.count(1),
                "clase_0_test": self.y_test.count(0),
                "clase_1_test": self.y_test.count(1),
            },
        }

    def reentrenar_con_hiperparametros(self, n_arboles, max_depth, max_leaves):
        """
        Reentrena con nuevos hiperparámetros y vuelve a evaluar en prueba.
        """
        if self.X_train is None or self.y_train is None:
            raise RuntimeError("Primero debes entrenar el modelo con un CSV.")

        validar_hiperparametros(n_arboles, max_depth, max_leaves)

        self.modelo.reentrenar(
            self.X_train,
            self.y_train,
            n_arboles=n_arboles,
            max_depth=max_depth,
            max_leaves=max_leaves,
        )

        y_pred = self.modelo.predecir(self.X_test)

        self.metricas = calcular_metricas(self.y_test, y_pred)
        self.listo_para_predecir = True

        return {
            "mensaje": "Modelo reentrenado correctamente.",
            "metricas": self.metricas,
        }

    def predecir_solicitante(self, datos_solicitante: dict):
        """
        Predice el riesgo para un solicitante individual.
        """
        if not self.listo_para_predecir:
            raise RuntimeError("El modelo no está entrenado aún.")

        solicitante_limpio = validar_solicitante(datos_solicitante)

        solicitante_norm = normalizar_solicitante(
            solicitante_limpio,
            self.params_norm,
        )

        muestra = [solicitante_norm[col] for col in COLUMNAS_NUMERICAS]

        clase, confianza = self.modelo.predecir_uno(muestra)

        return {
            "riesgo": bool(clase == 1),
            "confianza": round(confianza * 100, 1),
            "clase": clase,
            "mensaje": (
                "RIESGO DE INCUMPLIMIENTO DETECTADO"
                if clase == 1
                else "SIN RIESGO DE INCUMPLIMIENTO"
            ),
        }
    
    def registrar_rutas_archivos(self, ruta_csv_original=None, ruta_datos_limpios=None):
        """
        Guarda las rutas de archivos usados durante el flujo.
        """
        if ruta_csv_original is not None:
            self.ruta_csv_original = ruta_csv_original

        if ruta_datos_limpios is not None:
            self.ruta_datos_limpios = ruta_datos_limpios


    def obtener_estado(self):
        """
        Retorna el estado actual del motor.
        """
        return {
            "datos_cargados": self.datos_raw is not None,
            "datos_limpios": self.datos_limpios is not None,
            "modelo_entrenado": self.listo_para_predecir,
            "total_limpio": len(self.datos_limpios) if self.datos_limpios else 0,
            "metricas": self.metricas,
            "reporte_limpieza": self.reporte_limpieza,
            "archivos": {
                "csv_original": self.ruta_csv_original,
                "datos_limpios": self.ruta_datos_limpios,
            },
        }