from software_fj.manager import GestorSistema
from software_fj.entities import Cliente
from software_fj.services import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from software_fj.reservation import Reserva
from software_fj.exceptions import SistemaFJError
from software_fj.logger_config import logger
from software_fj.simulacion import ejecutar_simulacion


def pedir(texto):
    v = input(texto).strip()
    if not v:
        raise ValueError("El campo no puede estar vacío.")
    return v


def pedir_numero(texto, tipo=float):
    """Lee un número; si no es válido, lanza un error claro encadenado."""
    try:
        return tipo(input(texto).strip().replace(",", "."))
    except ValueError as exc:
        nombre = "entero" if tipo is int else "numérico"
        raise ValueError(f"Debe ingresar un valor {nombre} válido.") from exc


def elegir(elementos, titulo):
    if not elementos:
        print("No hay registros. Registre primero los datos necesarios.")
        return None
    print("\n" + titulo)
    for i, x in enumerate(elementos, 1):
        print(f"{i}. {x}")
    n = pedir_numero("Seleccione número: ", int)
    if n < 1 or n > len(elementos):
        raise ValueError("Selección fuera de rango.")
    return elementos[n - 1]


def menu():
    sistema = GestorSistema()
    while True:
        print("\n" + "=" * 52)
        print(" SOFTWARE FJ | GESTIÓN INTEGRAL")
        print("=" * 52)
        print("1. Registrar cliente")
        print("2. Registrar servicio")
        print("3. Crear reserva")
        print("4. Confirmar, cancelar o procesar reserva")
        print("5. Consultar todos los registros")
        print("6. Ejecutar simulación automática (24 operaciones)")
        print("0. Salir")
        try:
            op = input("Opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada finalizada. Hasta pronto.")
            logger.info("Programa finalizado por el usuario (Ctrl+C / EOF)")
            break
        if op == "0":
            print("Hasta pronto.")
            break
        try:
            if op == "1":
                c = Cliente(pedir("Identificación: "), pedir("Nombre: "), pedir("Correo: "), pedir("Teléfono: "))
                sistema.registrar_cliente(c)
                print("Cliente registrado.")
            elif op == "2":
                print("1 Sala | 2 Equipo | 3 Asesoría")
                t = input("Tipo: ").strip()
                cod = pedir("Código: ")
                nom = pedir("Nombre: ")
                tarifa = pedir_numero("Tarifa base: ")
                if t == "1":
                    s = ReservaSala(cod, nom, tarifa, pedir_numero("Capacidad: ", int))
                elif t == "2":
                    s = AlquilerEquipo(cod, nom, tarifa, pedir_numero("Unidades: ", int))
                elif t == "3":
                    s = AsesoriaEspecializada(cod, nom, tarifa, pedir("Especialidad: "))
                else:
                    raise ValueError("Tipo de servicio inválido.")
                sistema.registrar_servicio(s)
                print("Servicio registrado.")
            elif op == "3":
                c = elegir(sistema.clientes, "CLIENTES")
                s = elegir(sistema.servicios, "SERVICIOS") if c is not None else None
                if c is not None and s is not None:
                    r = Reserva(pedir("Código de reserva: "), c, s,
                                pedir_numero("Duración (horas/días): "),
                                pedir_numero("Descuento % (0 si no aplica): "))
                    sistema.crear_reserva(r)
                    print("Reserva creada como Pendiente.")
            elif op == "4":
                r = elegir(sistema.reservas, "RESERVAS")
                if r:
                    print("1 Confirmar | 2 Cancelar | 3 Procesar")
                    a = input("Acción: ").strip()
                    if a == "1":
                        r.confirmar()
                        print("Reserva confirmada.")
                    elif a == "2":
                        r.cancelar()
                        print("Reserva cancelada.")
                    elif a == "3":
                        print(f"Total: ${r.procesar():,.2f}")
                    else:
                        raise ValueError("Acción inválida.")
            elif op == "5":
                print("\nCLIENTES")
                for x in sistema.clientes:
                    print(x)
                print("\nSERVICIOS")
                for x in sistema.servicios:
                    print(x.describir())
                print("\nRESERVAS")
                for x in sistema.reservas:
                    print(x)
                print(sistema.resumen())
            elif op == "6":
                ejecutar_simulacion()
            else:
                print("Opción no válida.")
        except (SistemaFJError, ValueError, TypeError) as e:
            logger.exception("Operación rechazada: %s", e)
            print(f"ERROR CONTROLADO: {e}\nEl sistema sigue activo; intente nuevamente.")
        except (EOFError, KeyboardInterrupt):
            logger.warning("Operación cancelada por el usuario")
            print("\nOperación cancelada. Volviendo al menú.")
        except Exception as e:
            logger.exception("Error inesperado")
            print(f"Error inesperado: {e}. El sistema continúa activo.")


if __name__ == "__main__":
    menu()
