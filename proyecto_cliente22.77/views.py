from models import Estudiante
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/Estudiante.json")

CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")#agregado
# TUPLAS de configuración: fijas, nadie las modifica en tiempo de ejecución
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")## cambio 


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """CONJUNTO con los emails ya usados. Sirve para detectar duplicados al instante."""
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }

def carnets_registrados(excepto_id=None):
    return {
        registro["carnet"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }

def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota a un estudiante. La nota debe estar entre 0 y 20."""
    estudiante = obtener_por_id(id_estudiante)
    if estudiante is None:
      return False, f"No existe un estudiante con id {id_estudiante}"
    if not (0 <= nota <= 20):
      return False, "La nota debe estar entre 0 y 20"    
    # PASO 3: usar el método del modelo para agregar la nota EN MEMORIA
    estudiante.agregar_nota(materia, nota)

    # PASO 4: buscar la posición de ese estudiante en la lista del JSON
    registros = gestor.leer()
    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            registros[indice] = estudiante.a_diccionario()
            break

    # PASO 5: guardar la lista completa, ya con el registro actualizado
    gestor.guardar(registros)

    # PASO 6: devolver éxito
    return True, f"Nota agregada a {estudiante.obtener_nombre_completo()} en {materia}"
 
def materias_ofertadas():
    """Devuelve un CONJUNTO con todas las materias inscritas por todos los estudiantes."""
    todas = set()
    for estudiante in obtener_todos():
        todas = todas | estudiante.materias
    return todas

def estudiantes_en_comun(id_a, id_b):
    """Devuelve el CONJUNTO de materias que comparten dos estudiantes."""
    estudiante_a = obtener_por_id(id_a)
    if estudiante_a is None:
        return False, f"No existe un estudiante con id {id_a}"
    estudiante_b = obtener_por_id(id_b)
    if estudiante_b is None:
        return False, f"No existe un estudiante con id {id_b}"

    comunes = estudiante_a.materias_en_comun(estudiante_b)
    return True, comunes
    
def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_cliente(datos):
    """datos: diccionario con las claves de CAMPOS_CLIENTE. Devuelve (exito, mensaje)."""
    try:
        # 1) Normalizo: un diccionario con todos los campos, sin espacios sobrantes
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        # 2) Reviso obligatorios recorriendo la TUPLA
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 3) Formato del email
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        # 4) Duplicado: búsqueda instantánea dentro del CONJUNTO
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"
        
         #agregada Busquda instantanea
        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        # 5) Creo el objeto del Modelo. ** convierte el diccionario en argumentos
        cliente = Estudiante(siguiente_id(), **valores)

        # 6) Agrego a la LISTA y guardo
        registros = gestor.leer()
        registros.append(cliente.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Cliente {cliente.obtener_nombre_completo()} creado con id {cliente.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """LISTA de objetos Cliente."""
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_cliente):
    for cliente in obtener_todos():
        if cliente.id == id_cliente:
            return cliente
    return None


# ===================== S · SEARCH =====================

def buscar_clientes(termino):
    """Búsqueda lineal: revisa registro por registro los campos de CAMPOS_BUSCABLES."""
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:                 # recorro la TUPLA de campos
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break                                   # ya coincidió: paso al siguiente cliente
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_cliente(id_cliente, cambios):
    """cambios: diccionario solo con los campos que se quieren modificar."""
    try:
        # DIFERENCIA DE CONJUNTOS: ¿mandaron algún campo que no existe?
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            
            if cambios["email"].lower() in emails_registrados(excepto_id=id_cliente):
                return False, "Ese email ya lo usa otro cliente"
            
        if "carnet" in cambios:
            if cambios["carnet"].lower() in carnets_registrados(excepto_id=id_cliente):
                return False, "Ese carnet ya lo usa otro estudiante"    

        registros = gestor.leer()
        posicion = None
        for indice, registro in enumerate(registros):   # enumerate me da índice y valor
            if registro["id"] == id_cliente:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un cliente con id {id_cliente}"

        registros[posicion].update(cambios)             # actualizo el diccionario en su lugar
        gestor.guardar(registros)
        return True, f"Cliente {id_cliente} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_cliente(id_cliente):
    registros = gestor.leer()
    # Construyo una LISTA NUEVA sin ese registro: nunca borro mientras recorro
    quedan = [registro for registro in registros if registro["id"] != id_cliente]

    if len(quedan) == len(registros):
        return False, f"No existe un cliente con id {id_cliente}"

    gestor.guardar(quedan)
    return True, f"Cliente {id_cliente} eliminado"


# ===================== EXTRA: estadísticas con conjuntos =====================

def estadisticas():
    """Devuelve un DICCIONARIO de resumen. Práctica pura de conjuntos."""
    registros = gestor.leer()
    dominios = {r["email"].split("@")[1].lower() for r in registros if "@" in r["email"]}
    sin_notas = [r["nombre"] for r in registros if not r.get("notas")]

    return {
        "total": len(registros),
        "materias_ofertadas": sorted(materias_ofertadas()),
        "dominios": sorted(dominios),
        "sin_notas": sin_notas,
    }