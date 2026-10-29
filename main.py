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


ventana_agregar = None
cajas_agregar = []
lbl_resultado = None


def guardar_jugador():
    datos = []
    for caja in cajas_agregar:
        datos.append(caja.get())

    error, numero, inicio, fin = archivos.agregar_jugador(datos)

    if error != "":
        lbl_resultado.config(text=error, fg="red")
    else:
        lbl_resultado.config(
            text="Jugador guardado en el registro " + str(numero) + ".\n"
            "Posicion con tell(): " + str(inicio) + " a " + str(fin) + " bytes.",
            fg="green"
        )
        for caja in cajas_agregar:
            caja.delete(0, tk.END)
        cajas_agregar[0].focus()
        actualizar_estado()


def abrir_agregar():
    global ventana_agregar, cajas_agregar, lbl_resultado

    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar jugador")
    ventana_agregar.geometry("380x330")
    ventana_agregar.resizable(False, False)

    etiquetas = ["ID:", "Nombre:", "Pais:", "Club:", "Posicion:"]
    cajas_agregar = []

    for i in range(5):
        etiqueta = tk.Label(ventana_agregar, text=etiquetas[i])
        etiqueta.grid(row=i, column=0, padx=15, pady=8, sticky="e")
        caja = tk.Entry(ventana_agregar, width=30)
        caja.grid(row=i, column=1, pady=8)
        cajas_agregar.append(caja)

    boton_guardar = tk.Button(ventana_agregar, text="Guardar", width=12, command=guardar_jugador)
    boton_guardar.grid(row=5, column=0, pady=15)

    boton_cerrar = tk.Button(ventana_agregar, text="Cerrar", width=12, command=ventana_agregar.destroy)
    boton_cerrar.grid(row=5, column=1, pady=15)

    lbl_resultado = tk.Label(ventana_agregar, text="", wraplength=340)
    lbl_resultado.grid(row=6, column=0, columnspan=2, padx=15)

    cajas_agregar[0].focus()
    ventana_agregar.transient(ventana)
    ventana_agregar.wait_visibility()
    ventana_agregar.grab_set()

menu_jugadores = tk.Menu(barra, tearoff=0)
menu_jugadores.add_command(label="Agregar jugador", command=abrir_agregar)
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