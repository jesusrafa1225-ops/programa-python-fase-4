"""Simulación automática de más de 10 operaciones (válidas e inválidas).

Usa su propio GestorSistema para no mezclar datos con los que el usuario
registre manualmente desde el menú.
"""
from .entities import Cliente
from .exceptions import SistemaFJError
from .logger_config import logger
from .manager import GestorSistema
from .reservation import Reserva
from .services import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def _intentar(numero, descripcion, operacion):
    """try/except/else/finally: un error nunca detiene la simulación."""
    print(f"\n[{numero:02d}] {descripcion}")
    try:
        resultado = operacion()
    except SistemaFJError as e:
        logger.error("SIMULACIÓN %02d (%s) rechazada: %s", numero, descripcion, e)
        if e.__cause__:
            logger.error("   causa original: %r", e.__cause__)
        print(f"     ✗ Error controlado: {e}")
        return None
    except Exception as e:  # error imprevisto: se registra y se continúa
        logger.exception("SIMULACIÓN %02d: error inesperado", numero)
        print(f"     ✗ Error inesperado: {e!r}")
        return None
    else:
        logger.info("SIMULACIÓN %02d (%s) exitosa", numero, descripcion)
        print(f"     ✓ {resultado}")
        return resultado
    finally:
        logger.info("SIMULACIÓN %02d finalizada", numero)


def ejecutar_simulacion():
    g = GestorSistema()
    logger.info("=== Inicio de la simulación automática ===")
    print("\n" + "=" * 60 + "\nSIMULACIÓN AUTOMÁTICA (datos independientes del menú)\n" + "=" * 60)

    # ---- Clientes ----
    ana = _intentar(1, "Cliente válido", lambda: _cli(g, "C001", "ana maría gómez", "ana@correo.com", "300 123 4567"))
    _intentar(2, "Cliente con correo inválido", lambda: _cli(g, "C002", "Pedro Ruiz", "pedro-correo.com", "3109876543"))
    _intentar(3, "Cliente duplicado (misma identificación)", lambda: _cli(g, "C001", "Otra Persona", "otra@correo.com", "3001112233"))
    _intentar(4, "Cliente con teléfono inválido", lambda: _cli(g, "C003", "Luis Pérez", "luis@correo.com", "abc"))
    luis = _intentar(5, "Cliente válido", lambda: _cli(g, "C004", "Luis Pérez", "luis@correo.com", "3205551234"))

    # ---- Servicios ----
    sala = _intentar(6, "Sala válida", lambda: _srv(g, ReservaSala("S01", "Sala Innovación", 50000, 12)))
    equipo = _intentar(7, "Equipo válido", lambda: _srv(g, AlquilerEquipo("E01", "Portátil Pro", 20000, 5)))
    ase = _intentar(8, "Asesoría válida", lambda: _srv(g, AsesoriaEspecializada("A01", "Asesoría Datos", 120000, "Analítica")))
    _intentar(9, "Servicio con tarifa negativa", lambda: _srv(g, ReservaSala("S02", "Sala Rota", -5, 10)))
    _intentar(10, "Sala con capacidad cero", lambda: _srv(g, ReservaSala("S03", "Sala Vacía", 40000, 0)))

    # ---- Reservas exitosas ----
    r1 = _intentar(11, "Reserva válida (sala, 3 h, 10 % descuento)",
                   lambda: _res(g, Reserva("R001", ana, sala, 3, 10)))
    _intentar(12, "Confirmar R001", lambda: (r1.confirmar(), r1)[1])
    _intentar(13, "Procesar R001 (descuento + IVA)", lambda: f"Total ${r1.procesar():,.2f}")

    r2 = _intentar(14, "Reserva válida (equipo, 2 días)", lambda: _res(g, Reserva("R002", luis, equipo, 2)))

    # ---- Reservas y operaciones fallidas ----
    _intentar(15, "Reserva con duración negativa", lambda: _res(g, Reserva("R003", ana, sala, -2)))
    _intentar(16, "Procesar R002 sin confirmarla", lambda: f"Total ${r2.procesar():,.2f}")
    _intentar(17, "Cancelar R001 ya procesada", lambda: (r1.cancelar(), r1)[1])
    ase.disponible = False
    _intentar(18, "Reserva sobre servicio no disponible", lambda: _res(g, Reserva("R004", ana, ase, 2)))
    ase.disponible = True
    _intentar(19, "Reserva con cliente inexistente en el sistema",
              lambda: _res(g, Reserva("R005", Cliente("C999", "Fantasma Uno", "f@x.com", "3000000000"), sala, 1)))

    # ---- Cálculos y sobrecarga (parámetros opcionales) ----
    _intentar(20, "Costo: solo duración y por defecto con IVA", lambda: f"${sala.calcular_costo(2):,.2f}")
    _intentar(21, "Costo: con descuento 20 % e IVA 0 %", lambda: f"${sala.calcular_costo(2, descuento=20, impuesto=0):,.2f}")
    _intentar(22, "Costo con descuento inconsistente (150 %)", lambda: sala.calcular_costo(2, descuento=150))
    _intentar(23, "Costo con descuento no numérico (encadenamiento)", lambda: sala.calcular_costo(2, descuento="mucho"))

    # ---- Cierre ----
    _intentar(24, "Cancelar R002 pendiente", lambda: (r2.cancelar(), r2)[1])
    print("\n" + "-" * 60)
    print(g.resumen())
    for lista in (g.clientes, g.servicios, g.reservas):
        for item in lista:
            print("  •", item)
    logger.info("=== Fin de la simulación: la aplicación continuó estable ===")
    print("\nLa simulación terminó sin interrumpir el programa. Revise software_fj.log")


# Ayudantes: registran y devuelven el objeto creado
def _cli(g, *datos):
    c = Cliente(*datos)
    g.registrar_cliente(c)
    return c


def _srv(g, s):
    g.registrar_servicio(s)
    return s


def _res(g, r):
    g.crear_reserva(r)
    return r
