from abc import ABC, abstractmethod
import re
from .exceptions import ValidacionError

class Entidad(ABC):
    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValidacionError("El identificador es obligatorio.")
        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def descripcion(self): pass

    def __str__(self):
        return self.descripcion()

class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.nombre, self.correo, self.telefono = nombre, correo, telefono

    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, v):
        if not isinstance(v, str) or len(v.strip()) < 3:
            raise ValidacionError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = v.strip().title()

    @property
    def correo(self): return self._correo
    @correo.setter
    def correo(self, v):
        if not isinstance(v, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", v.strip()):
            raise ValidacionError("Correo electrónico inválido.")
        self._correo = v.lower().strip()

    @property
    def telefono(self): return self._telefono
    @telefono.setter
    def telefono(self, v):
        limpio = re.sub(r"[\s+()-]", "", str(v))
        if not limpio.isdigit() or not 7 <= len(limpio) <= 15:
            raise ValidacionError("Teléfono inválido: use entre 7 y 15 dígitos.")
        self._telefono = limpio

    def descripcion(self): return f"{self.nombre} - {self.correo}"
    def __str__(self): return f"{self.identificador} | {self.nombre} | {self.correo}"
