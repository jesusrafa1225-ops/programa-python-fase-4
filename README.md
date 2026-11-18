# Software FJ – Sistema interactivo

## Ejecución
1. Descomprima el proyecto.
2. Abra la carpeta `Software_FJ_Interactivo` en Visual Studio Code.
3. Abra la terminal integrada (Terminal > New Terminal).
4. Ejecute `python main.py` (en Windows también puede usar `py main.py`).

## Uso
El menú permite registrar clientes, registrar tres tipos de servicios, crear reservas, confirmar/cancelar/procesar reservas y consultar registros. Seleccione `0` para salir.

Los datos se conservan en listas mientras el programa está abierto. No se usa base de datos. Los eventos y errores se registran en `software_fj.log`.

## Arquitectura
`entities.py`: Entidad abstracta y Cliente.  
`services.py`: Servicio abstracto y tres servicios derivados.  
`reservation.py`: Reserva, estados y operaciones.  
`manager.py`: listas y administración.  
`exceptions.py`: excepciones personalizadas.  
`logger_config.py`: registro de eventos y errores.  
`main.py`: menú interactivo.

El método `calcular_costo(duracion, descuento=0, impuesto=0.19)` permite variantes mediante parámetros opcionales. En Python, la sobrecarga tradicional se simula con valores predeterminados o despacho por argumentos.

## Simulación automática
La opción 6 del menú ejecuta 24 operaciones (clientes, servicios, reservas y cálculos válidos e inválidos) y demuestra que el sistema continúa estable ante errores. Código en `software_fj/simulacion.py`.
