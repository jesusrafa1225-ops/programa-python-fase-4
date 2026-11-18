from .entities import Cliente
from .services import Servicio
from .reservation import Reserva
from .exceptions import ValidacionError, ClienteDuplicadoError, EntidadNoEncontradaError
from .logger_config import logger

class GestorSistema:
    def __init__(self): self._clientes, self._servicios, self._reservas = [], [], []
    @property
    def clientes(self): return tuple(self._clientes)
    @property
    def servicios(self): return tuple(self._servicios)
    @property
    def reservas(self): return tuple(self._reservas)
    def registrar_cliente(self, c):
        if not isinstance(c, Cliente): raise ValidacionError("Se requiere un Cliente.")
        if any(x.identificador == c.identificador for x in self._clientes): raise ClienteDuplicadoError("Cliente duplicado.")
        self._clientes.append(c); logger.info("Cliente registrado %s", c.identificador)
    def registrar_servicio(self, s):
        if not isinstance(s, Servicio): raise ValidacionError("Se requiere un Servicio.")
        if any(x.identificador == s.identificador for x in self._servicios): raise ValidacionError("Servicio duplicado.")
        self._servicios.append(s); logger.info("Servicio registrado %s", s.identificador)
    def crear_reserva(self, r):
        if not isinstance(r, Reserva): raise ValidacionError("Se requiere una Reserva.")
        if r.cliente not in self._clientes or r.servicio not in self._servicios: raise EntidadNoEncontradaError("Cliente o servicio no registrado.")
        if any(x.identificador == r.identificador for x in self._reservas): raise ValidacionError("Reserva duplicada.")
        self._reservas.append(r); logger.info("Reserva creada %s", r.identificador)
    def resumen(self): return f"Clientes: {len(self._clientes)} | Servicios: {len(self._servicios)} | Reservas: {len(self._reservas)}"
