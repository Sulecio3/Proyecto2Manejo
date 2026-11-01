import os
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
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
            "telefono": jugador[3],
            "correo": jugador[4],
            "ciudad": jugador[5],
            "club": jugador[6],
            "posicion": jugador[7]
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

        pdf = canvas.Canvas(RUTA_PDF, pagesize=landscape(A4))
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, 550, "REPORTE DE JUGADORES DE FUTBOL")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(40, 528, "Fecha de generacion: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        pdf.drawString(40, 514, "Total de jugadores: " + str(datos["total"]))

        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(40, 482, "ID")
        pdf.drawString(80, 482, "Nombre")
        pdf.drawString(230, 482, "Telefono")
        pdf.drawString(320, 482, "Correo")
        pdf.drawString(490, 482, "Ciudad")
        pdf.drawString(590, 482, "Club")
        pdf.drawString(720, 482, "Posicion")

        pdf.setFont("Helvetica", 9)
        y = 462

        for jugador in datos["jugadores"]:
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 9)
                y = 550

            pdf.drawString(40, y, str(jugador["id"]))
            pdf.drawString(80, y, jugador["nombre"])
            pdf.drawString(230, y, jugador["telefono"])
            pdf.drawString(320, y, jugador["correo"])
            pdf.drawString(490, y, jugador["ciudad"])
            pdf.drawString(590, y, jugador["club"])
            pdf.drawString(720, y, jugador["posicion"])
            y = y - 18

        pdf.save()

    except PermissionError:
        return "No se pudo escribir el PDF. Si lo tiene abierto, cierrelo e intente de nuevo.", 0
    except OSError:
        return "No se pudo guardar el reporte PDF.", 0
    except (ValueError, KeyError):
        return "El archivo JSON exportado no tiene el formato esperado.", 0

    return "", total
