import archivos


def buscar_secuencial(clave):
    revisados = 0
    encontrado = False

    with open(archivos.RUTA_DATOS, "rb") as archivo:
        while True:
            registro = archivo.read(archivos.TAM_REGISTRO)

            if len(registro) < archivos.TAM_REGISTRO:
                break

            revisados = revisados + 1
            jugador = archivos.leer_campos(registro)

            if jugador[0] == clave and jugador[5] == "A":
                encontrado = True
                break

    return encontrado, revisados


codigos = ["410", "122", "475", "631", "999"]

print("COMPARACION DE BUSQUEDAS")
print()
print(f"{'ID':<6}{'Con indice':<30}{'Secuencial'}")

for clave in codigos:
    error, jugador, numero, inicio, fin = archivos.buscar_jugador(clave)

    if error == "":
        con_indice = "1 lectura, seek(" + str(inicio) + ")"
    else:
        con_indice = "0 lecturas, no existe"

    encontrado, revisados = buscar_secuencial(clave)

    print(f"{clave:<6}{con_indice:<30}{revisados} registros revisados")