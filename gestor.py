"""
Módulo controlador del Sistema de Gestión de Software FJ.
Gestiona las listas internas en memoria y aplica manejo avanzado de excepciones
(try/except, try/except/else, try/except/finally y encadenamiento de excepciones).
"""

from typing import List, Optional
from excepciones import (
    ErrorSistemaFJ,
    DatoInvalidoError,
    OperacionNoPermitidaError,
    ReservaIncorrectaError,
)
from modelos import Cliente, Servicio, Reserva
from logger import configurar_logger


class GestorSoftwareFJ:
    """
    Clase coordinadora que administra clientes, servicios y reservas en memoria,
    garantizando continuidad operativa ante errores y trazabilidad en logs.
    """

    def __init__(self, archivo_log: str = "sistema_fj.log"):
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []
        self._logger = configurar_logger(archivo_log)
        self._logger.info("=== INICIO DE SESIÓN DEL SISTEMA SOFTWARE FJ ===")

    @property
    def clientes(self) -> List[Cliente]:
        return self._clientes

    @property
    def servicios(self) -> List[Servicio]:
        return self._servicios

    @property
    def reservas(self) -> List[Reserva]:
        return self._reservas

    def registrar_cliente(self, id_cliente: str, nombre: str, documento: str, correo: str) -> Optional[Cliente]:
        """Registra un cliente usando try/except/else y verifica duplicados."""
        try:
            # Verifica si ya existe un cliente con el mismo ID o documento
            if any(c.id == id_cliente or c.documento == documento for c in self._clientes):
                raise OperacionNoPermitidaError(
                    f"Ya existe un cliente registrado con ID '{id_cliente}' o documento '{documento}'."
                )
            nuevo_cliente = Cliente(id_cliente, nombre, documento, correo)
        except ErrorSistemaFJ as error:
            self._logger.error(f"Fallo al registrar cliente ({id_cliente}): {error}")
            return None
        else:
            self._clientes.append(nuevo_cliente)
            self._logger.info(f"Cliente registrado con éxito -> {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Agrega un servicio especializado al catálogo en memoria."""
        try:
            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("El objeto proporcionado no corresponde a un Servicio válido.")
            if any(s.id == servicio.id for s in self._servicios):
                raise OperacionNoPermitidaError(f"El servicio con ID '{servicio.id}' ya existe en el catálogo.")
        except ErrorSistemaFJ as error:
            self._logger.error(f"Fallo al registrar servicio: {error}")
            return False
        else:
            self._servicios.append(servicio)
            self._logger.info(f"Servicio agregado al catálogo -> {servicio.obtener_resumen()}")
            return True

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        """Busca un cliente por ID o lanza una excepción personalizada si no existe."""
        for cliente in self._clientes:
            if cliente.id == id_cliente:
                return cliente
        raise DatoInvalidoError(f"No se encontró ningún cliente con ID '{id_cliente}'.")

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        """Busca un servicio por ID o lanza una excepción personalizada si no existe."""
        for servicio in self._servicios:
            if servicio.id == id_servicio:
                return servicio
        raise DatoInvalidoError(f"No se encontró ningún servicio con ID '{id_servicio}'.")

    def crear_y_confirmar_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
    ) -> Optional[Reserva]:
        """
        Crea y confirma una reserva aplicando try/except/finally y encadenamiento de excepciones.
        """
        reserva_creada: Optional[Reserva] = None
        estado_auditoria = "FALLIDA"

        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)

            if any(r.id == id_reserva for r in self._reservas):
                raise OperacionNoPermitidaError(f"El código de reserva '{id_reserva}' ya fue utilizado.")

            # Encadenamiento de excepciones: si falla la creación o el cálculo, se encapsula en ReservaIncorrectaError
            try:
                reserva_creada = Reserva(id_reserva, cliente, servicio, duracion)
                reserva_creada.procesar_y_confirmar(impuesto=impuesto, descuento=descuento)
            except ErrorSistemaFJ as error_origen:
                raise ReservaIncorrectaError(
                    f"No fue posible procesar la reserva '{id_reserva}' para el servicio '{id_servicio}'."
                ) from error_origen

            self._reservas.append(reserva_creada)
            estado_auditoria = "EXITOSA"
            self._logger.info(f"Reserva confirmada -> {reserva_creada.obtener_resumen()}")
            return reserva_creada

        except ErrorSistemaFJ as error:
            causa = f" | Causa original: {error.__cause__}" if error.__cause__ else ""
            self._logger.error(f"Error en operación de reserva '{id_reserva}': {error}{causa}")
            return None
        finally:
            self._logger.debug(f"Auditoría finalizada para intento de reserva '{id_reserva}' -> Estado: {estado_auditoria}")

    def cancelar_reserva(self, id_reserva: str) -> bool:
        """Cancela una reserva existente y restaura la disponibilidad del servicio."""
        try:
            reserva_objetivo = next((r for r in self._reservas if r.id == id_reserva), None)
            if reserva_objetivo is None:
                raise ReservaIncorrectaError(f"La reserva '{id_reserva}' no existe en el sistema.")

            reserva_objetivo.cancelar()
        except ErrorSistemaFJ as error:
            self._logger.error(f"Fallo al cancelar reserva '{id_reserva}': {error}")
            return False
        else:
            self._logger.info(f"Reserva cancelada correctamente -> {reserva_objetivo.obtener_resumen()}")
            return True
