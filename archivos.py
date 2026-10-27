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