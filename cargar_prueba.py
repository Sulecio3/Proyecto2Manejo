import archivos

error = archivos.preparar_archivos()

if error != "":
    print(error)
elif not archivos.archivo_valido():
    print("El archivo jugadores.dat tiene otra estructura (version anterior).")
    print("Abra main.py y acepte renombrarlo, o borre jugadores.dat, indice.json y jugadores.sha256.")
else:
    jugadores = [
        ["410", "Ronaldinho Gaúcho", "5510-4410", "ronaldinho@ejemplo.com", "Porto Alegre", "Barcelona", "Mediocampista"],
        ["122", "Zinedine Zidane", "5520-1220", "zidane@ejemplo.com", "Marsella", "Real Madrid", "Mediocampista"],
        ["305", "Andrés Iniesta", "5530-3050", "iniesta@ejemplo.com", "Fuentealbilla", "Barcelona", "Mediocampista"],
        ["518", "Thierry Henry", "5540-5180", "henry@ejemplo.com", "Les Ulis", "Arsenal", "Delantero"],
        ["207", "Paolo Maldini", "5550-2070", "maldini@ejemplo.com", "Milán", "AC Milan", "Defensa"],
        ["631", "Carlos Ruiz", "5560-6310", "carlos.ruiz@ejemplo.com", "Ciudad de Guatemala", "Municipal", "Delantero"],
        ["144", "Marco Pappa", "5570-1440", "marco.pappa@ejemplo.com", "Ciudad de Guatemala", "Comunicaciones", "Mediocampista"],
        ["389", "Rafael Márquez", "5580-3890", "rafael.marquez@ejemplo.com", "Zamora", "Barcelona", "Defensa"],
        ["276", "Keylor Navas", "5590-2760", "keylor.navas@ejemplo.com", "Pérez Zeledón", "Real Madrid", "Portero"],
        ["452", "Hugo Sánchez", "5511-4520", "hugo.sanchez@ejemplo.com", "Ciudad de México", "Real Madrid", "Delantero"],
        ["163", "Diego Forlán", "5521-1630", "forlan@ejemplo.com", "Montevideo", "Atlético de Madrid", "Delantero"],
        ["597", "Luis Suárez", "5531-5970", "luis.suarez@ejemplo.com", "Salto", "Barcelona", "Delantero"],
        ["238", "Kaká", "5541-2380", "kaka@ejemplo.com", "Brasilia", "AC Milan", "Mediocampista"],
        ["341", "Gianluigi Buffon", "5551-3410", "buffon@ejemplo.com", "Carrara", "Juventus", "Portero"],
        ["475", "Roberto Carlos", "5561-4750", "roberto.carlos@ejemplo.com", "Garça", "Real Madrid", "Defensa"]
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
