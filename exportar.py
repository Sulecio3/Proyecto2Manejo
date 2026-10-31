import os
import json
from datetime import datetime
from reportlab.pdfgen import canvas
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


def generar_pdf():
    error, total = exportar_json()

    if error != "":
        return error, 0

    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        pdf = canvas.Canvas(RUTA_PDF)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 780, "REPORTE DE JUGADORES DE FUTBOL")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 758, "Fecha de generacion: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        pdf.drawString(50, 744, "Total de jugadores: " + str(datos["total"]))

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, 712, "ID")
        pdf.drawString(95, 712, "Nombre")
        pdf.drawString(250, 712, "Pais")
        pdf.drawString(340, 712, "Club")
        pdf.drawString(470, 712, "Posicion")

        pdf.setFont("Helvetica", 10)
        y = 692

        for jugador in datos["jugadores"]:
            if y < 60:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 780

            pdf.drawString(50, y, str(jugador["id"]))
            pdf.drawString(95, y, jugador["nombre"])
            pdf.drawString(250, y, jugador["pais"])
            pdf.drawString(340, y, jugador["club"])
            pdf.drawString(470, y, jugador["posicion"])
            y = y - 18

        pdf.save()

    except PermissionError:
        return "No se pudo escribir el PDF. Si lo tiene abierto, cierrelo e intente de nuevo.", 0
    except OSError:
        return "No se pudo guardar el reporte PDF.", 0
    except (ValueError, KeyError):
        return "El archivo JSON exportado no tiene el formato esperado.", 0

    return "", total