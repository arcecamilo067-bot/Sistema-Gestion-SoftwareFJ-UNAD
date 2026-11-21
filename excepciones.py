"""
Módulo de excepciones personalizadas para el Sistema de Gestión de Software FJ.
Define una jerarquía clara de errores controlada desde una excepción base del dominio.
"""


class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR-000"):
        # Se almacena el mensaje descriptivo y un código interno para trazabilidad en logs
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(f"[{codigo_error}] {mensaje}")


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple con el formato, tipo o rango esperado."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-DATO-001")


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un atributo o argumento obligatorio para ejecutar una acción."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-PARAM-002")


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar ejecutar una acción inválida según las reglas del negocio."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-OPER-003")


class ReservaIncorrectaError(ErrorSistemaFJ):
    """Se lanza cuando los datos, duración o estado de una reserva son inconsistentes."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-RES-004")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando un servicio está inactivo, ocupado o sin inventario suficiente."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-SERV-005")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando el cálculo de tarifas, impuestos o descuentos arroja valores incoherentes."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-CALC-006")
