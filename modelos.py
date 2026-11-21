"""
Módulo de modelos de dominio (POO) para el Sistema de Gestión de Software FJ.
Implementa abstracción, herencia, polimorfismo, encapsulación y sobrecarga de métodos.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ReservaIncorrectaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class EntidadSistema(ABC):
    """
    Clase abstracta base que representa cualquier entidad general del sistema Software FJ.
    """

    def __init__(self, id_entidad: str):
        # Valida que el identificador no sea nulo ni esté vacío
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio y debe ser texto.")
        self._id = id_entidad.strip()
        self._fecha_registro = datetime.now()

    @property
    def id(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self._id

    @property
    def fecha_registro(self) -> datetime:
        """Retorna la fecha y hora en que se registró la entidad."""
        return self._fecha_registro

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las subclases a presentar su información clave."""
        pass


class Cliente(EntidadSistema):
    """
    Representa un cliente de Software FJ con encapsulación estricta y validaciones de datos.
    """

    def __init__(self, id_cliente: str, nombre: str, documento: str, correo: str):
        super().__init__(id_cliente)
        # Se asignan mediante setters para garantizar que pasen por todas las validaciones
        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres válidos.")
        self.__nombre = valor.strip()

    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip().isdigit() or len(valor.strip()) < 6:
            raise DatoInvalidoError(f"El documento '{valor}' es inválido. Debe contener al menos 6 dígitos numéricos.")
        self.__documento = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not isinstance(valor, str) or not re.match(patron_correo, valor.strip()):
            raise DatoInvalidoError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id}] | Nombre: {self.nombre} | Doc: {self.documento} | Correo: {self.correo}"


class Servicio(EntidadSistema, ABC):
    """
    Clase abstracta que modela un servicio ofrecido por Software FJ.
    Define la interfaz polimórfica para describir, validar y calcular costos.
    """

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base del servicio debe ser un número positivo mayor a 0.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Valida las reglas específicas de cada tipo de servicio antes de operar."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción detallada y polimórfica del servicio."""
        pass

    @abstractmethod
    def _calcular_subtotal(self, duracion: int) -> float:
        """Calcula el valor neto del servicio según su lógica especializada."""
        pass

    def calcular_costo(self, duracion: int, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Método sobrecargado mediante parámetros opcionales para calcular el costo total.
        Permite calcular:
        1. Costo simple: calcular_costo(duracion)
        2. Costo con impuestos: calcular_costo(duracion, impuesto=0.19)
        3. Costo con impuestos y descuento: calcular_costo(duracion, impuesto=0.19, descuento=0.10)
        """
        self.validar_parametros(duracion)

        if impuesto < 0 or impuesto > 1:
            raise CalculoInconsistenteError(f"El porcentaje de impuesto ({impuesto}) debe estar entre 0.0 y 1.0.")
        if descuento < 0 or descuento >= 1:
            raise CalculoInconsistenteError(f"El porcentaje de descuento ({descuento}) debe estar entre 0.0 y 0.99.")

        subtotal = self._calcular_subtotal(duracion)
        valor_con_descuento = subtotal * (1 - descuento)
        total = valor_con_descuento * (1 + impuesto)

        if total <= 0:
            raise CalculoInconsistenteError("El cálculo final del servicio arrojó un valor menor o igual a cero.")

        return round(total, 2)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.describir()} | Tarifa base: ${self.tarifa_base:,.2f} | Estado: {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para el alquiler de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 1 or duracion > 12:
            raise ReservaIncorrectaError("La reserva de una sala debe ser entre 1 y 12 horas.")

    def _calcular_subtotal(self, duracion: int) -> float:
        # Si la sala supera 20 personas, aplica un recargo operativo del 15%
        recargo = 1.15 if self._capacidad > 20 else 1.0
        return self.tarifa_base * duracion * recargo

    def describir(self) -> str:
        return f"Sala '{self.nombre}' (ID: {self.id}, Capacidad: {self._capacidad} personas)"


class AlquilerEquipo(Servicio):
    """Servicio especializado para el préstamo/alquiler de equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, cantidad_unidades: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not isinstance(cantidad_unidades, int) or cantidad_unidades <= 0:
            raise DatoInvalidoError("La cantidad de unidades del equipo debe ser mayor a 0.")
        self._cantidad_unidades = cantidad_unidades

    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 1 or duracion > 30:
            raise ReservaIncorrectaError("El alquiler de equipos debe ser entre 1 y 30 días.")

    def _calcular_subtotal(self, duracion: int) -> float:
        # Incluye una póliza fija de seguro tecnológico de $15.000 por transacción
        seguro_equipo = 15000.0
        return (self.tarifa_base * duracion * self._cantidad_unidades) + seguro_equipo

    def describir(self) -> str:
        return f"Alquiler Equipo '{self.nombre}' (ID: {self.id}, Unidades: {self._cantidad_unidades})"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría y asesoría técnica por expertos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not especialidad or not isinstance(especialidad, str) or not especialidad.strip():
            raise ParametroFaltanteError("Debe especificar el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 2:
            raise ReservaIncorrectaError("Toda asesoría especializada requiere un mínimo de 2 horas.")

    def _calcular_subtotal(self, duracion: int) -> float:
        return self.tarifa_base * duracion

    def describir(self) -> str:
        return f"Asesoría en {self._especialidad}: '{self.nombre}' (ID: {self.id})"


class Reserva(EntidadSistema):
    """
    Integra un Cliente, un Servicio y una duración, gestionando el ciclo de vida
    de la reserva (PENDIENTE -> CONFIRMADA -> CANCELADA).
    """

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Servicio.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no se encuentra disponible actualmente.")

        # Valida la duración usando las reglas polimórficas del servicio específico
        servicio.validar_parametros(duracion)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> int:
        return self._duracion

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def procesar_y_confirmar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """
        Calcula el costo total usando la sobrecarga del servicio, marca el servicio como ocupado
        y cambia el estado de la reserva a CONFIRMADA.
        """
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.id} porque su estado actual es '{self._estado}'."
            )
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' fue ocupado antes de confirmar la reserva {self.id}."
            )

        self._costo_total = self._servicio.calcular_costo(
            duracion=self._duracion,
            impuesto=impuesto,
            descuento=descuento
        )
        self._servicio.disponible = False
        self._estado = "CONFIRMADA"
        return self._costo_total

    def cancelar(self) -> None:
        """Cancela una reserva activa y libera nuevamente la disponibilidad del servicio."""
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"La reserva {self.id} ya se encuentra cancelada.")

        self._estado = "CANCELADA"
        self._servicio.disponible = True

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | Total: ${self._costo_total:,.2f}"
        )
