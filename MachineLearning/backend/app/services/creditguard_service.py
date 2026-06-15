"""
Servicio singleton del motor CreditGuard.
FastAPI usará esta instancia compartida durante la ejecución del servidor.
"""

from app.ml.engine import CreditGuardEngine


creditguard_engine = CreditGuardEngine()