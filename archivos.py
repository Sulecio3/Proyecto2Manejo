import os
import json

RUTA_DATOS = "jugadores.dat"
RUTA_INDICE = "indice.json"
RUTA_HASH = "jugadores.sha256"

CAMPOS = ["id", "nombre", "pais", "club", "posicion", "estado"]
LARGOS = [6, 30, 15, 25, 15, 1]

TAM_REGISTRO = sum(LARGOS) + 1


def validar_largos(jugador):
    for i in range(len(CAMPOS)):
        datos = str(jugador[i]).encode("utf-8")
        if len(datos) > LARGOS[i]:
            return "El campo " + CAMPOS[i] + " permite maximo " + str(LARGOS[i]) + " caracteres."
    return ""


def armar_registro(jugador):
    registro = b""
    for i in range(len(CAMPOS)):
        datos = str(jugador[i]).encode("utf-8")
        registro = registro + datos.ljust(LARGOS[i])
    registro = registro + b"\n"
    return registro


def leer_campos(registro):
    jugador = []
    inicio = 0
    for largo in LARGOS:
        trozo = registro[inicio:inicio + largo]
        jugador.append(trozo.decode("utf-8", errors="replace").strip())
        inicio = inicio + largo
    return jugador


def preparar_archivos():
    try:
        if not os.path.exists(RUTA_DATOS):
            with open(RUTA_DATOS, "ab") as archivo:
                pass

        if not os.path.exists(RUTA_INDICE):
            with open(RUTA_INDICE, "w", encoding="utf-8") as archivo:
                json.dump({}, archivo)

    except PermissionError:
        return "No hay permisos para crear los archivos en esta carpeta."
    except OSError:
        return "No se pudieron crear los archivos de datos."

    return ""


def contar_registros():
    return os.path.getsize(RUTA_DATOS) // TAM_REGISTRO


def archivo_completo():
    return os.path.getsize(RUTA_DATOS) % TAM_REGISTRO == 0


def cargar_indice():
    try:
        with open(RUTA_INDICE, "r", encoding="utf-8") as archivo:
            indice = json.load(archivo)
    except (OSError, json.JSONDecodeError):
        return None

    if type(indice) != dict:
        return None

    return indice


def guardar_indice(indice):
    with open(RUTA_INDICE, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4)


def agregar_jugador(datos):
    jugador = []
    for i in range(5):
        texto = str(datos[i]).strip()
        if texto == "":
            return "El campo " + CAMPOS[i] + " no puede estar vacio.", -1, -1, -1
        if "\n" in texto or "\r" in texto:
            return "El campo " + CAMPOS[i] + " no puede tener saltos de linea.", -1, -1, -1
        jugador.append(texto)

    if not jugador[0].isdecimal() or int(jugador[0]) == 0:
        return "El id debe ser un numero entero mayor que cero.", -1, -1, -1

    jugador[0] = str(int(jugador[0]))
    jugador.append("A")

    error = validar_largos(jugador)
    if error != "":
        return error, -1, -1, -1

    indice = cargar_indice()
    if indice is None:
        return "No se pudo leer el archivo indice.json.", -1, -1, -1

    if jugador[0] in indice:
        return "Ya existe un jugador con el id " + jugador[0] + ".", -1, -1, -1

    registro = armar_registro(jugador)

    try:
        numero = contar_registros()

        with open(RUTA_DATOS, "r+b") as archivo:
            archivo.seek(numero * TAM_REGISTRO)
            inicio = archivo.tell()
            archivo.write(registro)
            fin = archivo.tell()

        indice[jugador[0]] = numero
        guardar_indice(indice)

    except PermissionError:
        return "No hay permisos para escribir en los archivos de datos.", -1, -1, -1
    except OSError:
        return "No se pudo guardar el jugador en el archivo.", -1, -1, -1

    return "", numero, inicio, fin


def convertir_id(texto):
    texto = str(texto).strip()
    if not texto.isdecimal() or int(texto) == 0:
        return ""
    return str(int(texto))


def leer_registro(numero):
    with open(RUTA_DATOS, "rb") as archivo:
        archivo.seek(numero * TAM_REGISTRO)
        inicio = archivo.tell()
        registro = archivo.read(TAM_REGISTRO)
        fin = archivo.tell()
    return registro, inicio, fin


def buscar_jugador(id_texto):
    clave = convertir_id(id_texto)
    if clave == "":
        return "El id debe ser un numero entero mayor que cero.", [], -1, -1, -1

    indice = cargar_indice()
    if indice is None:
        return "No se pudo leer el archivo indice.json.", [], -1, -1, -1

    if clave not in indice:
        return "No existe un jugador con el id " + clave + ".", [], -1, -1, -1

    numero = indice[clave]
    if type(numero) != int or numero < 0:
        return "El indice tiene un dato invalido para el id " + clave + ".", [], -1, -1, -1

    try:
        registro, inicio, fin = leer_registro(numero)
    except PermissionError:
        return "No hay permisos para leer el archivo de datos.", [], -1, -1, -1
    except OSError:
        return "No se pudo leer el archivo de datos.", [], -1, -1, -1

    if len(registro) != TAM_REGISTRO:
        return "El registro del id " + clave + " esta incompleto.", [], -1, -1, -1

    jugador = leer_campos(registro)
    if jugador[0] != clave or jugador[5] != "A":
        return "El indice no coincide con el archivo de datos.", [], -1, -1, -1

    return "", jugador, numero, inicio, fin


def modificar_jugador(id_texto, nuevos):
    error, jugador, numero, inicio, fin = buscar_jugador(id_texto)
    if error != "":
        return error, -1, -1

    datos = [jugador[0]]
    for i in range(4):
        texto = str(nuevos[i]).strip()
        if texto == "":
            return "El campo " + CAMPOS[i + 1] + " no puede estar vacio.", -1, -1
        if "\n" in texto or "\r" in texto:
            return "El campo " + CAMPOS[i + 1] + " no puede tener saltos de linea.", -1, -1
        datos.append(texto)
    datos.append("A")

    error = validar_largos(datos)
    if error != "":
        return error, -1, -1

    try:
        with open(RUTA_DATOS, "r+b") as archivo:
            archivo.seek(numero * TAM_REGISTRO)
            inicio = archivo.tell()
            archivo.write(armar_registro(datos))
            fin = archivo.tell()
    except PermissionError:
        return "No hay permisos para escribir en el archivo de datos.", -1, -1
    except OSError:
        return "No se pudo modificar el jugador en el archivo.", -1, -1

    return "", inicio, fin


def eliminar_jugador(id_texto):
    error, jugador, numero, inicio, fin = buscar_jugador(id_texto)
    if error != "":
        return error

    indice = cargar_indice()
    if indice is None:
        return "No se pudo leer el archivo indice.json."

    jugador[5] = "E"

    try:
        with open(RUTA_DATOS, "r+b") as archivo:
            archivo.seek(numero * TAM_REGISTRO)
            archivo.write(armar_registro(jugador))

        del indice[jugador[0]]
        guardar_indice(indice)

    except PermissionError:
        return "No hay permisos para escribir en los archivos de datos."
    except OSError:
        return "No se pudo eliminar el jugador."

    return ""


def listar_jugadores():
    jugadores = []

    try:
        with open(RUTA_DATOS, "rb") as archivo:
            for numero in range(contar_registros()):
                registro = archivo.read(TAM_REGISTRO)
                jugador = leer_campos(registro)
                if jugador[5] == "A":
                    jugadores.append([numero] + jugador)
    except OSError:
        return None

    return jugadores