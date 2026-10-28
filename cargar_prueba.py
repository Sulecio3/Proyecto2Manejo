import archivos

error = archivos.preparar_archivos()

if error != "":
    print(error)
else:
    jugadores = [
        ["410", "Ronaldinho Gaúcho", "Brasil", "Barcelona", "Mediocampista"],
        ["122", "Zinedine Zidane", "Francia", "Real Madrid", "Mediocampista"],
        ["305", "Andrés Iniesta", "España", "Barcelona", "Mediocampista"],
        ["518", "Thierry Henry", "Francia", "Arsenal", "Delantero"],
        ["207", "Paolo Maldini", "Italia", "AC Milan", "Defensa"],
        ["631", "Carlos Ruiz", "Guatemala", "Municipal", "Delantero"],
        ["144", "Marco Pappa", "Guatemala", "Comunicaciones", "Mediocampista"],
        ["389", "Rafael Márquez", "México", "Barcelona", "Defensa"],
        ["276", "Keylor Navas", "Costa Rica", "Real Madrid", "Portero"],
        ["452", "Hugo Sánchez", "México", "Real Madrid", "Delantero"],
        ["163", "Diego Forlán", "Uruguay", "Atlético de Madrid", "Delantero"],
        ["597", "Luis Suárez", "Uruguay", "Barcelona", "Delantero"],
        ["238", "Kaká", "Brasil", "AC Milan", "Mediocampista"],
        ["341", "Gianluigi Buffon", "Italia", "Juventus", "Portero"],
        ["475", "Roberto Carlos", "Brasil", "Real Madrid", "Defensa"]
    ]

    print("CARGA DE JUGADORES DE PRUEBA")
    print()

    for jugador in jugadores:
        error, numero, inicio, fin = archivos.agregar_jugador(jugador)

        if error == "":
            print(f"Registro {numero:<3} id {jugador[0]:<5} {jugador[1]:<20} tell(): {inicio} a {fin}")
        else:
            print("No se guardo", jugador[1], "->", error)

    print()
    print("Registros en el archivo:", archivos.contar_registros())
    print("Tamano del archivo:", archivos.contar_registros() * archivos.TAM_REGISTRO, "bytes")