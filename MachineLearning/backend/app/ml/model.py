"""
Random Forest implementado desde cero para CreditGuard.
No utiliza scikit-learn ni librerías externas de Machine Learning.
"""

import math
import random
from collections import Counter


def _gini(y):
    """
    Calcula el índice Gini de una lista de etiquetas.
    """
    n = len(y)

    if n == 0:
        return 0.0

    conteo = Counter(y)

    return 1.0 - sum((c / n) ** 2 for c in conteo.values())


def _mejor_division(X, y, indices_features):
    """
    Encuentra la mejor división usando ganancia Gini.
    """
    mejor_ganancia = -1
    mejor_feature = None
    mejor_umbral = None

    gini_padre = _gini(y)
    n = len(y)

    for feat_idx in indices_features:
        valores = sorted(set(row[feat_idx] for row in X))

        for i in range(len(valores) - 1):
            umbral = (valores[i] + valores[i + 1]) / 2

            izq_y = [y[j] for j in range(n) if X[j][feat_idx] <= umbral]
            der_y = [y[j] for j in range(n) if X[j][feat_idx] > umbral]

            if len(izq_y) == 0 or len(der_y) == 0:
                continue

            ganancia = gini_padre - (
                (len(izq_y) / n) * _gini(izq_y)
                + (len(der_y) / n) * _gini(der_y)
            )

            if ganancia > mejor_ganancia:
                mejor_ganancia = ganancia
                mejor_feature = feat_idx
                mejor_umbral = umbral

    return mejor_feature, mejor_umbral, mejor_ganancia


def _construir_arbol(
    X,
    y,
    profundidad_actual,
    max_depth,
    max_leaves,
    indices_features,
    hojas_actuales,
):
    """
    Construye recursivamente un árbol de decisión.
    """
    n = len(y)
    conteo = Counter(y)

    if n == 0:
        return {
            "hoja": True,
            "clase": 0,
            "conteo": {},
        }

    if (
        len(set(y)) == 1
        or profundidad_actual >= max_depth
        or hojas_actuales[0] >= max_leaves
    ):
        return {
            "hoja": True,
            "clase": conteo.most_common(1)[0][0],
            "conteo": dict(conteo),
        }

    feat_idx = indices_features or list(range(len(X[0])))

    n_features_split = max(1, int(math.sqrt(len(feat_idx))))

    features_candidatas = random.sample(
        feat_idx,
        min(n_features_split, len(feat_idx)),
    )

    mejor_feature, mejor_umbral, mejor_ganancia = _mejor_division(
        X,
        y,
        features_candidatas,
    )

    if mejor_feature is None or mejor_ganancia <= 0:
        return {
            "hoja": True,
            "clase": conteo.most_common(1)[0][0],
            "conteo": dict(conteo),
        }

    mascara_izq = [X[i][mejor_feature] <= mejor_umbral for i in range(n)]

    X_izq = [X[i] for i in range(n) if mascara_izq[i]]
    y_izq = [y[i] for i in range(n) if mascara_izq[i]]

    X_der = [X[i] for i in range(n) if not mascara_izq[i]]
    y_der = [y[i] for i in range(n) if not mascara_izq[i]]

    hojas_actuales[0] += 1

    return {
        "hoja": False,
        "feature": mejor_feature,
        "umbral": mejor_umbral,
        "izquierdo": _construir_arbol(
            X_izq,
            y_izq,
            profundidad_actual + 1,
            max_depth,
            max_leaves,
            feat_idx,
            hojas_actuales,
        ),
        "derecho": _construir_arbol(
            X_der,
            y_der,
            profundidad_actual + 1,
            max_depth,
            max_leaves,
            feat_idx,
            hojas_actuales,
        ),
    }


def _predecir_muestra(nodo, muestra):
    """
    Recorre el árbol para clasificar una muestra.
    """
    if nodo["hoja"]:
        return nodo["clase"]

    if muestra[nodo["feature"]] <= nodo["umbral"]:
        return _predecir_muestra(nodo["izquierdo"], muestra)

    return _predecir_muestra(nodo["derecho"], muestra)


class RandomForestCreditGuard:
    """
    Random Forest para clasificación binaria de riesgo crediticio.
    """

    def __init__(self, n_arboles=100, max_depth=10, max_leaves=50, semilla=42):
        self.n_arboles = n_arboles
        self.max_depth = max_depth
        self.max_leaves = max_leaves
        self.semilla = semilla

        self.arboles = []
        self.entrenado = False

    def entrenar(self, X, y):
        """
        Entrena el bosque con bootstrap aggregating.
        """
        if len(X) == 0 or len(y) == 0:
            raise ValueError("No hay datos suficientes para entrenar el modelo.")

        random.seed(self.semilla)

        self.arboles = []

        n = len(X)
        n_features = len(X[0])
        indices_features = list(range(n_features))

        for _ in range(self.n_arboles):
            indices_bootstrap = [random.randint(0, n - 1) for _ in range(n)]

            X_boot = [X[j] for j in indices_bootstrap]
            y_boot = [y[j] for j in indices_bootstrap]

            hojas_actuales = [0]

            arbol = _construir_arbol(
                X_boot,
                y_boot,
                profundidad_actual=0,
                max_depth=self.max_depth,
                max_leaves=self.max_leaves,
                indices_features=indices_features,
                hojas_actuales=hojas_actuales,
            )

            self.arboles.append(arbol)

        self.entrenado = True

    def predecir(self, X):
        """
        Predice la clase para cada muestra.
        """
        if not self.entrenado:
            raise RuntimeError("El modelo no ha sido entrenado aún.")

        predicciones = []

        for muestra in X:
            votos = [_predecir_muestra(arbol, muestra) for arbol in self.arboles]
            predicciones.append(Counter(votos).most_common(1)[0][0])

        return predicciones

    def predecir_uno(self, muestra):
        """
        Predice la clase para un único solicitante y retorna confianza.
        """
        if not self.entrenado:
            raise RuntimeError("El modelo no ha sido entrenado aún.")

        votos = [_predecir_muestra(arbol, muestra) for arbol in self.arboles]

        clase_ganadora = Counter(votos).most_common(1)[0][0]
        confianza = votos.count(clase_ganadora) / len(votos)

        return clase_ganadora, confianza

    def reentrenar(self, X, y, n_arboles=None, max_depth=None, max_leaves=None):
        """
        Actualiza hiperparámetros y reentrena.
        """
        if n_arboles is not None:
            self.n_arboles = n_arboles

        if max_depth is not None:
            self.max_depth = max_depth

        if max_leaves is not None:
            self.max_leaves = max_leaves

        self.entrenar(X, y)