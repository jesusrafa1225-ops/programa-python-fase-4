from abc import ABC, abstractmethod
from .entities import Entidad
from .exceptions import ValidacionError

class Servicio(Entidad, ABC):
    def __init__(self, identificador, nombre, tarifa, disponible=True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip() or not isinstance(tarifa, (int, float)) or isinstance(tarifa, bool) or tarifa <= 0:
            raise ValidacionError("Nombre y tarifa positiva son obligatorios.")
        self.nombre, self.tarifa, self.disponible = nombre.strip(), float(tarifa), disponible

    @abstractmethod
    def validar_duracion(self, duracion): pass
    @abstractmethod
    def costo_base(self, duracion): pass
    @abstractmethod
    def describir(self): pass

    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        try:
            self.validar_duracion(duracion)
            if not 0 <= descuento <= 100 or not 0 <= impuesto <= 1:
                raise ValidacionError("Descuento o impuesto fuera de rango.")
            return round(self.costo_base(duracion) * (1-descuento/100) * (1+impuesto), 2)
        except ValidacionError:
            raise
        except Exception as exc:
            raise ValidacionError("No fue posible calcular el costo.") from exc

    def descripcion(self): return self.describir()

class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0: raise ValidacionError("Capacidad inválida.")
        self.capacidad = capacidad
    def validar_duracion(self, d):
        if isinstance(d, bool) or not isinstance(d, (int,float)) or d <= 0: raise ValidacionError("Las horas deben ser positivas.")
    def costo_base(self, d): return self.tarifa*d
    def describir(self): return f"Sala {self.nombre}, capacidad {self.capacidad}, tarifa/hora ${self.tarifa:,.0f}"

class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa, unidades, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        if not isinstance(unidades, int) or unidades <= 0: raise ValidacionError("Unidades inválidas.")
        self.unidades = unidades
    def validar_duracion(self, d):
        if isinstance(d, bool) or not isinstance(d, (int, float)) or d <= 0 or not float(d).is_integer():
            raise ValidacionError("Los días deben ser un número entero positivo.")
    def costo_base(self, d): return self.tarifa*d
    def describir(self): return f"Equipo {self.nombre}, unidades {self.unidades}, tarifa/día ${self.tarifa:,.0f}"

class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador, nombre, tarifa, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa, disponible)
        if not especialidad.strip(): raise ValidacionError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()
    def validar_duracion(self, d):
        if isinstance(d, bool) or not isinstance(d, (int,float)) or d <= 0: raise ValidacionError("Las horas deben ser positivas.")
    def costo_base(self, d): return self.tarifa*d
    def describir(self): return f"Asesoría {self.nombre}, especialidad {self.especialidad}, tarifa/hora ${self.tarifa:,.0f}"
