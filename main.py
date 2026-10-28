import tkinter as tk
from tkinter import messagebox
import archivos

ventana = tk.Tk()
ventana.title("Registro de Jugadores de Futbol")
ventana.geometry("480x300")
ventana.resizable(False, False)


def proximamente():
    messagebox.showinfo(
        "En desarrollo",
        "Esta opcion todavia no esta disponible."
    )


def mostrar_estructura():
    texto = "Campos del registro:\n\n"
    for i in range(len(archivos.CAMPOS)):
        texto = texto + archivos.CAMPOS[i] + ": " + str(archivos.LARGOS[i]) + " bytes\n"
    texto = texto + "salto de linea: 1 byte\n\n"
    texto = texto + "Tamano total: " + str(archivos.TAM_REGISTRO) + " bytes"
    messagebox.showinfo("Estructura del registro", texto)


def acerca_de():
    messagebox.showinfo(
        "Acerca de",
        "Registro de Jugadores de Futbol\n"
        "Proyecto de manejo de archivos con acceso aleatorio.\n"
        "Version 1.0"
    )


def actualizar_estado():
    try:
        cantidad = archivos.contar_registros()
        lbl_registros.config(text="Registros guardados: " + str(cantidad))

        if archivos.archivo_completo():
            lbl_aviso.config(text="")
        else:
            lbl_aviso.config(text="Aviso: el archivo tiene un registro incompleto.")

    except OSError:
        lbl_registros.config(text="Registros guardados: no disponible")
        lbl_aviso.config(text="Aviso: no se pudo leer el archivo de datos.")


barra = tk.Menu(ventana)

menu_jugadores = tk.Menu(barra, tearoff=0)
menu_jugadores.add_command(label="Agregar jugador", command=proximamente)
menu_jugadores.add_command(label="Buscar por ID", command=proximamente)
menu_jugadores.add_command(label="Modificar jugador", command=proximamente)
menu_jugadores.add_command(label="Eliminar jugador", command=proximamente)
menu_jugadores.add_command(label="Ver todos", command=proximamente)
menu_jugadores.add_separator()
menu_jugadores.add_command(label="Salir", command=ventana.destroy)
barra.add_cascade(label="Jugadores", menu=menu_jugadores)

menu_exportar = tk.Menu(barra, tearoff=0)
menu_exportar.add_command(label="Exportar a JSON", command=proximamente)
menu_exportar.add_command(label="Generar reporte PDF", command=proximamente)
barra.add_cascade(label="Exportar", menu=menu_exportar)

menu_herramientas = tk.Menu(barra, tearoff=0)
menu_herramientas.add_command(label="Verificar integridad", command=proximamente)
menu_herramientas.add_command(label="Crear respaldo ZIP", command=proximamente)
menu_herramientas.add_command(label="Informacion del archivo", command=proximamente)
barra.add_cascade(label="Herramientas", menu=menu_herramientas)

menu_ayuda = tk.Menu(barra, tearoff=0)
menu_ayuda.add_command(label="Estructura del registro", command=mostrar_estructura)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)
barra.add_cascade(label="Ayuda", menu=menu_ayuda)

ventana.config(menu=barra)

lbl_titulo = tk.Label(
    ventana,
    text="REGISTRO DE JUGADORES DE FUTBOL",
    font=("Arial", 14, "bold")
)
lbl_titulo.pack(pady=20)

lbl_archivo = tk.Label(ventana, text="Archivo de datos: " + archivos.RUTA_DATOS)
lbl_archivo.pack()

lbl_tamano = tk.Label(
    ventana,
    text="Tamano de cada registro: " + str(archivos.TAM_REGISTRO) + " bytes"
)
lbl_tamano.pack(pady=5)

lbl_registros = tk.Label(ventana, text="")
lbl_registros.pack()

lbl_aviso = tk.Label(ventana, text="", fg="red")
lbl_aviso.pack(pady=10)

error = archivos.preparar_archivos()

if error != "":
    messagebox.showerror("Error", error)

actualizar_estado()

ventana.mainloop()