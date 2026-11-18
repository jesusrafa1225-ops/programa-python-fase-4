from enum import Enum
from .entities import Entidad, Cliente
from .services import Servicio
from .exceptions import ValidacionError, ReservaError, ServicioNoDisponibleError
from .logger_config import logger

class EstadoReserva(Enum):
    PENDIENTE="Pendiente"
    CONFIRMADA="Confirmada"
    CANCELADA="Cancelada"
    PROCESADA="Procesada"

class Reserva(Entidad):
    def __init__(self, identificador, cliente, servicio, duracion, descuento=0):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ValidacionError("Cliente o servicio no válido.")
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
            raise ValidacionError("El descuento debe estar entre 0 y 100.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible para reservar.")
        servicio.validar_duracion(duracion)
        self.cliente, self.servicio, self.duracion = cliente, servicio, duracion
        self.descuento, self.estado, self.total = descuento, EstadoReserva.PENDIENTE, None

    def confirmar(self):
        if self.estado != EstadoReserva.PENDIENTE: raise ReservaError("Solo se confirman reservas pendientes.")
        if not self.servicio.disponible: raise ServicioNoDisponibleError("El servicio no está disponible.")
        self.estado = EstadoReserva.CONFIRMADA
        logger.info("Reserva %s confirmada", self.identificador)

    def cancelar(self):
        if self.estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise ReservaError("No se puede cancelar en el estado actual.")
        self.estado = EstadoReserva.CANCELADA
        logger.info("Reserva %s cancelada", self.identificador)

    def procesar(self):
        if self.estado != EstadoReserva.CONFIRMADA: raise ReservaError("La reserva debe estar confirmada.")
        try:
            self.total = self.servicio.calcular_costo(self.duracion, self.descuento)
        except Exception as exc:
            logger.exception("Error al procesar reserva %s", self.identificador)
            raise ReservaError("Falló el procesamiento.") from exc
        else:
            self.estado = EstadoReserva.PROCESADA
            logger.info("Reserva %s procesada: %s", self.identificador, self.total)
            return self.total
        finally:
            logger.info("Finalizó intento de procesamiento %s", self.identificador)

    def descripcion(self):
        return f"{self.identificador} | {self.cliente.nombre} | {self.servicio.nombre} | {self.estado.value} | Total: {self.total}"
    def __str__(self): return self.descripcion()
