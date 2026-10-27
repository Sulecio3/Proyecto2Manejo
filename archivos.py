import os
import json

RUTA_DATOS = "jugadores.dat"
RUTA_INDICE = "indice.json"
RUTA_HASH = "jugadores.sha256"

CAMPOS = ["id", "nombre", "pais", "club", "posicion", "estado"]
LARGOS = [6, 30, 15, 25, 15, 1]

TAM_REGISTRO = sum(LARGOS) + 1