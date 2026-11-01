import os
import json
import hashlib
import zipfile
from datetime import datetime

RUTA_DATOS = "jugadores.dat"
RUTA_INDICE = "indice.json"
RUTA_HASH = "jugadores.sha256"
CARPETA_RESPALDOS = "respaldos"

CAMPOS = ["id", "nombre", "telefono", "correo", "ciudad", "club", "posicion", "estado"]
LARGOS = [6, 30, 15, 35, 20, 25, 15, 1]

TAM_REGISTRO = sum(LARGOS) + 1
CANTIDAD_DATOS = len(CAMPOS) - 1
POS_ESTADO = len(CAMPOS) - 1


def validar_largos(jugador):
    for i in range(len(CAMPOS)):
        datos = str(jugador[i]).encode("utf-8")
        if len(datos) > LARGOS[i]:
            return "El campo " + CAMPOS[i] + " permite maximo " + str(LARGOS[i]) + " caracteres."
    return ""


def validar_formato(jugador):
    telefono = jugador[2]
    digitos = 0
    for letra in telefono:
        if letra.isdigit():
            digitos = digitos + 1
        elif letra not in " +-()":
            return "El telefono solo puede tener numeros, espacios, + - ( )."
    if digitos < 7:
        return "El telefono debe tener al menos 7 numeros."

    correo = jugador[3]
    if " " in correo or correo.count("@") != 1:
        return "El correo no es valido. Ejemplo: nombre@dominio.com"
    usuario, dominio = correo.split("@")
    if usuario == "" or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        return "El correo no es valido. Ejemplo: nombre@dominio.com"

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


def archivo_valido():
    try:
        with open(RUTA_DATOS, "rb") as archivo:
            while True:
                registro = archivo.read(TAM_REGISTRO)

                if len(registro) < TAM_REGISTRO:
                    break

                jugador = leer_campos(registro)

                if registro[-1:] != b"\n":
                    return False
                if not jugador[0].isdecimal():
                    return False
                if jugador[POS_ESTADO] != "A" and jugador[POS_ESTADO] != "E":
                    return False
    except OSError:
        return False

    return True


def apartar_archivos():
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        for ruta in [RUTA_DATOS, RUTA_INDICE, RUTA_HASH]:
            if os.path.exists(ruta):
                nombre, extension = os.path.splitext(ruta)
                os.replace(ruta, nombre + "_anterior_" + fecha + extension)
    except PermissionError:
        return "No hay permisos para renombrar los archivos de datos. Cierre otros programas que los usen."
    except OSError:
        return "No se pudieron renombrar los archivos de datos."

    return preparar_archivos()


def cargar_indice():
    try:
        with open(RUTA_INDICE, "r", encoding="utf-8") as archivo:
            indice = json.load(archivo)
    except (OSError, ValueError):
        return None

    if type(indice) != dict:
        return None

    return indice


def guardar_indice(indice):
    with open(RUTA_INDICE, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4)


def agregar_jugador(datos):
    jugador = []
    for i in range(CANTIDAD_DATOS):
        texto = str(datos[i]).strip()
        if texto == "":
            return "El campo " + CAMPOS[i] + " no puede estar vacio.", -1, -1, -1
        if "\n" in texto or "\r" in texto:
            return "El campo " + CAMPOS[i] + " no puede tener saltos de linea.", -1, -1, -1
        jugador.append(texto)

    if not jugador[0].isdecimal() or int(jugador[0]) == 0:
        return "El id debe ser un numero entero mayor que cero.", -1, -1, -1

    jugador[0] = str(int(jugador[0]))

    error = validar_formato(jugador)
    if error != "":
        return error, -1, -1, -1

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
        guardar_hash()

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
    if jugador[0] != clave or jugador[POS_ESTADO] != "A":
        return "El indice no coincide con el archivo de datos.", [], -1, -1, -1

    return "", jugador, numero, inicio, fin


def modificar_jugador(id_texto, nuevos):
    error, jugador, numero, inicio, fin = buscar_jugador(id_texto)
    if error != "":
        return error, -1, -1

    datos = [jugador[0]]
    for i in range(CANTIDAD_DATOS - 1):
        texto = str(nuevos[i]).strip()
        if texto == "":
            return "El campo " + CAMPOS[i + 1] + " no puede estar vacio.", -1, -1
        if "\n" in texto or "\r" in texto:
            return "El campo " + CAMPOS[i + 1] + " no puede tener saltos de linea.", -1, -1
        datos.append(texto)

    error = validar_formato(datos)
    if error != "":
        return error, -1, -1

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
        guardar_hash()
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

    jugador[POS_ESTADO] = "E"

    try:
        with open(RUTA_DATOS, "r+b") as archivo:
            archivo.seek(numero * TAM_REGISTRO)
            archivo.write(armar_registro(jugador))

        del indice[jugador[0]]
        guardar_indice(indice)
        guardar_hash()

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
                if jugador[POS_ESTADO] == "A":
                    jugadores.append([numero] + jugador)
    except OSError:
        return None

    return jugadores


def calcular_hash(ruta):
    sha256 = hashlib.sha256()

    with open(ruta, "rb") as archivo:
        while True:
            bloque = archivo.read(4096)

            if not bloque:
                break

            sha256.update(bloque)

    return sha256.hexdigest()


def guardar_hash():
    with open(RUTA_HASH, "w", encoding="utf-8") as archivo:
        archivo.write(calcular_hash(RUTA_DATOS))


def verificar_hash():
    if not os.path.exists(RUTA_HASH):
        return "sin_hash", "", ""

    try:
        with open(RUTA_HASH, "r", encoding="utf-8") as archivo:
            guardado = archivo.read().strip()
        actual = calcular_hash(RUTA_DATOS)
    except (OSError, ValueError):
        return "error", "", ""

    if guardado == actual:
        return "ok", guardado, actual

    return "alterado", guardado, actual


def crear_respaldo():
    archivos_respaldo = [RUTA_DATOS, RUTA_INDICE]

    for ruta in archivos_respaldo:
        if not os.path.exists(ruta):
            return "No se encontro el archivo " + ruta + ". No se pudo crear el respaldo.", "", 0, 0

    try:
        os.makedirs(CARPETA_RESPALDOS, exist_ok=True)
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_zip = os.path.join(CARPETA_RESPALDOS, "respaldo_" + fecha + ".zip")

        original = 0

        with zipfile.ZipFile(ruta_zip, "w", compression=zipfile.ZIP_DEFLATED) as zip_archivo:
            for ruta in archivos_respaldo:
                zip_archivo.write(ruta, ruta)
                original = original + os.path.getsize(ruta)

        comprimido = os.path.getsize(ruta_zip)

    except PermissionError:
        return "No hay permisos para crear el respaldo.", "", 0, 0
    except OSError:
        return "No se pudo crear el respaldo ZIP.", "", 0, 0

    return "", ruta_zip, original, comprimido


def informacion_archivo():
    try:
        datos = os.stat(RUTA_DATOS)
    except OSError:
        return "No se pudo consultar el archivo " + RUTA_DATOS + ".", 0, "", False, False

    modificado = datetime.fromtimestamp(datos.st_mtime).strftime("%d/%m/%Y %H:%M:%S")
    puede_leer = os.access(RUTA_DATOS, os.R_OK)
    puede_escribir = os.access(RUTA_DATOS, os.W_OK)

    return "", datos.st_size, modificado, puede_leer, puede_escribir


def construir_indice():
    indice = {}

    with open(RUTA_DATOS, "rb") as archivo:
        for numero in range(contar_registros()):
            registro = archivo.read(TAM_REGISTRO)
            jugador = leer_campos(registro)
            if jugador[POS_ESTADO] == "A" and jugador[0].isdecimal():
                indice[jugador[0]] = numero

    return indice


def reconstruir_indice():
    try:
        indice = construir_indice()
        guardar_indice(indice)
    except PermissionError:
        return "No hay permisos para escribir el archivo indice.json.", 0
    except OSError:
        return "No se pudo reconstruir el indice.", 0

    return "", len(indice)


def indice_correcto():
    indice = cargar_indice()

    if indice is None:
        return False

    try:
        return indice == construir_indice()
    except OSError:
        return False
