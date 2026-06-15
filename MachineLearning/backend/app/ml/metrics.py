"""
Métricas de evaluación para CreditGuard.
"""


def calcular_metricas(y_real, y_predicho):
    """
    Calcula exactitud, precisión, recall y F1-score.

    Clase positiva = 1, con riesgo de incumplimiento.
    """
    n = len(y_real)

    if n == 0:
        return {
            "exactitud": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        }

    vp = sum(1 for r, p in zip(y_real, y_predicho) if r == 1 and p == 1)
    vn = sum(1 for r, p in zip(y_real, y_predicho) if r == 0 and p == 0)
    fp = sum(1 for r, p in zip(y_real, y_predicho) if r == 0 and p == 1)
    fn = sum(1 for r, p in zip(y_real, y_predicho) if r == 1 and p == 0)

    exactitud = (vp + vn) / n

    precision = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0.0

    if precision + recall > 0:
        f1 = (2 * precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    return {
        "exactitud": round(exactitud, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "matriz": {
            "VP": vp,
            "VN": vn,
            "FP": fp,
            "FN": fn,
        },
    }