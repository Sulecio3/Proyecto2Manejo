import os
import json
from datetime import datetime
import archivos

CARPETA = "exportaciones"
RUTA_JSON = os.path.join(CARPETA, "jugadores.json")
RUTA_PDF = os.path.join(CARPETA, "reporte_jugadores.pdf")


def exportar_json():
    jugadores = archivos.listar_jugadores()

    if jugadores is None:
        return "No se pudo leer el archivo de datos.", 0

    lista = []
    for jugador in jugadores:
        if jugador[1].isdecimal():
            identificador = int(jugador[1])
        else:
            identificador = jugador[1]

        lista.append({
            "registro": jugador[0],
            "id": identificador,
            "nombre": jugador[2],
            "pais": jugador[3],
            "club": jugador[4],
            "posicion": jugador[5]
        })

    datos = {
        "fecha_exportacion": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total": len(lista),
        "jugadores": lista
    }

    try:
        os.makedirs(CARPETA, exist_ok=True)
        with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except PermissionError:
        return "No hay permisos para escribir en la carpeta exportaciones.", 0
    except OSError:
        return "No se pudo guardar el archivo JSON.", 0

    return "", len(lista)