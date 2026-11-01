import archivos

print("ESTRUCTURA DEL REGISTRO")
print()

inicio = 0
for i in range(len(archivos.CAMPOS)):
    campo = archivos.CAMPOS[i]
    largo = archivos.LARGOS[i]
    print(f"{campo:<10} inicio: {inicio:<4} largo: {largo}")
    inicio = inicio + largo

print(f"{'salto':<10} inicio: {inicio:<4} largo: 1")
print()
print("Tamano total del registro:", archivos.TAM_REGISTRO, "bytes")
print()

jugador = ["1", "Rafael Márquez", "5551-2048", "rafael.marquez@ejemplo.com", "Zamora", "Barcelona", "Defensa", "A"]

error = archivos.validar_largos(jugador)

if error == "":
    registro = archivos.armar_registro(jugador)

    print("Registro de ejemplo:")
    print(registro.decode("utf-8"), end="")
    print("Bytes del registro:", len(registro))

    if len(registro) == archivos.TAM_REGISTRO:
        print("El tamano coincide con el definido.")
    else:
        print("ERROR: el tamano no coincide.")

    print("Campos recuperados:", archivos.leer_campos(registro))
else:
    print(error)
