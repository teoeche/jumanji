from views import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_cliente, obtener_todos, obtener_por_id, buscar_clientes,
    actualizar_cliente, eliminar_cliente, estadisticas,agregar_nota,estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CARNET':<15}{'PROMEDIO':<10}")
    print("-" * 85)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}"
              f"{estudiante.email:<28}{estudiante.carnet:<15}{estudiante.obtener_promedio():<10}")
    print("-" * 85)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")




# ---------- C · CREAR ----------
def opcion_crear():
    imprimir_titulo("CREAR NUEVO CLIENTE")
    # Recorro la TUPLA de campos: si mañana agrego un campo al Modelo,
    # este formulario se actualiza solo.
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_cliente(datos)          # desempaqueto la TUPLA que devuelve
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- R · LEER TODOS ----------
def opcion_ver_todos():
    imprimir_titulo("LISTA DE CLIENTES")
    clientes = obtener_todos()
    if not clientes:
        imprimir_info("Todavía no hay clientes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(clientes)
    pausa()


# ---------- S · BUSCAR ----------
def opcion_buscar():
    imprimir_titulo("BUSCAR CLIENTE")
    termino = input("Nombre, email, teléfono o ciudad: ")
    encontrados = buscar_clientes(termino)

    if not encontrados:
        imprimir_info(f"Ningún cliente coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


# ---------- R · LEER UNO ----------
def opcion_ver_por_id():
    imprimir_titulo("VER CLIENTE POR ID")
    try:
        id_cliente = int(input("Id del cliente: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    cliente = obtener_por_id(id_cliente)
    if not cliente:
        imprimir_error(f"No existe un cliente con id {id_cliente}")
    else:
        # Recorro el DICCIONARIO del cliente: clave y valor a la vez
        for clave, valor in cliente.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")
    pausa()


# ---------- U · ACTUALIZAR ----------
def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_cliente = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    cliente = obtener_por_id(id_cliente)
    if not cliente:
        imprimir_error(f"No existe un estudiante con id {id_cliente}")
        return pausa()

    imprimir_info(f"Editando a {cliente.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    # Armo un DICCIONARIO solo con lo que el usuario escribió
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(cliente, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_cliente(id_cliente, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- D · ELIMINAR ----------
def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_cliente = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    cliente = obtener_por_id(id_cliente)
    if not cliente:
        imprimir_error(f"No existe un cliente con id {id_cliente}")
        return pausa()

    imprimir_info(f"Se eliminará: {cliente}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_cliente(id_cliente)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


# ---------- EXTRA · ESTADÍSTICAS ----------
def opcion_estadisticas():
    imprimir_titulo("ESTADÍSTICAS")
    datos = estadisticas()
    print(f"  Estudiantes registrados : {datos['total']}")
    print(f"  Materias ofertadas      : {len(datos['materias_ofertadas'])} -> {', '.join(datos['materias_ofertadas'])}")
    print(f"  Dominios de email       : {', '.join(datos['dominios'])}")
    print(f"  Sin notas               : {len(datos['sin_notas'])}")
    pausa()
# ---------- EXTRA · VER PROMEDIO ----------
def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO DE ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        imprimir_info(f"Promedio de {estudiante.obtener_nombre_completo()}: {estudiante.obtener_promedio()}")
    pausa()

def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA A ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    materia = input("Materia: ").strip()

    try:
        nota = float(input("Nota (0 a 20): "))
    except ValueError:
        imprimir_error("La nota debe ser un número")
        return pausa()

    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()  

def opcion_materias_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los ids deben ser números enteros")
        return pausa()

    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    elif not resultado:
        imprimir_info("Estos estudiantes no comparten ninguna materia")
    else:
        imprimir_info(f"Materias en común: {', '.join(sorted(resultado))}")
    pausa()       
    
def salir():
    imprimir_info("¡Hasta luego! 👋")
    return "salir"


# DICCIONARIO de opciones: tecla -> (texto del menú, función)
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Estadísticas", opcion_estadisticas),
    "8": ("Ver promedio", opcion_ver_promedio),#agregado
    "9": ("Agregar nota", opcion_agregar_nota), 
    "10": ("Materias en común", opcion_materias_comun),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTE")
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()

        if tecla not in OPCIONES:          # búsqueda instantánea por clave
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")