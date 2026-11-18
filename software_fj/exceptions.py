class SistemaFJError(Exception): pass
class ValidacionError(SistemaFJError): pass
class ClienteDuplicadoError(SistemaFJError): pass
class ServicioNoDisponibleError(SistemaFJError): pass
class ReservaError(SistemaFJError): pass
class EntidadNoEncontradaError(SistemaFJError): pass
