import tkinter as tk
from tkinter import messagebox, simpledialog
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


def actualizar_estado():
    try:
        cantidad = archivos.contar_registros()
        indice = archivos.cargar_indice()

        texto = "Registros en el archivo: " + str(cantidad)
        if indice is not None:
            texto = texto + " (activos: " + str(len(indice)) + ")"
        lbl_registros.config(text=texto)

        if archivos.archivo_completo():
            lbl_aviso.config(text="")
        else:
            lbl_aviso.config(text="Aviso: el archivo tiene un registro incompleto.")

    except OSError:
        lbl_registros.config(text="Registros en el archivo: no disponible")
        lbl_aviso.config(text="Aviso: no se pudo leer el archivo de datos.")

def buscar_por_id():
    texto = simpledialog.askstring(
        "Buscar por ID",
        "Ingrese el id del jugador:",
        parent=ventana
    )

    if texto is None:
        return

    error, jugador, numero, inicio, fin = archivos.buscar_jugador(texto)

    if error != "":
        messagebox.showerror("Error", error)
    else:
        messagebox.showinfo(
            "Jugador encontrado",
            "ID: " + jugador[0] + "\n"
            "Nombre: " + jugador[1] + "\n"
            "Pais: " + jugador[2] + "\n"
            "Club: " + jugador[3] + "\n"
            "Posicion: " + jugador[4] + "\n\n"
            "Registro numero: " + str(numero) + "\n"
            "Posicion con seek() y tell(): " + str(inicio) + " a " + str(fin)
        )


ventana_modificar = None
caja_id_mod = None
cajas_mod = []
lbl_resultado_mod = None
id_cargado = ""


def cargar_para_modificar():
    global id_cargado

    error, jugador, numero, inicio, fin = archivos.buscar_jugador(caja_id_mod.get())

    for caja in cajas_mod:
        caja.delete(0, tk.END)

    if error != "":
        id_cargado = ""
        lbl_resultado_mod.config(text=error, fg="red")
    else:
        id_cargado = jugador[0]
        for i in range(4):
            cajas_mod[i].insert(0, jugador[i + 1])
        lbl_resultado_mod.config(
            text="Jugador cargado. Cambie los datos y guarde.",
            fg="black"
        )


def guardar_cambios():
    if id_cargado == "":
        lbl_resultado_mod.config(
            text="Primero cargue un jugador con el boton Cargar datos.",
            fg="red"
        )
        return

    nuevos = []
    for caja in cajas_mod:
        nuevos.append(caja.get())

    error, inicio, fin = archivos.modificar_jugador(id_cargado, nuevos)

    if error != "":
        lbl_resultado_mod.config(text=error, fg="red")
    else:
        lbl_resultado_mod.config(
            text="Jugador modificado en su lugar.\n"
            "Posicion con tell(): " + str(inicio) + " a " + str(fin) + " bytes.",
            fg="green"
        )


def abrir_modificar():
    global ventana_modificar, caja_id_mod, cajas_mod, lbl_resultado_mod, id_cargado

    id_cargado = ""

    ventana_modificar = tk.Toplevel(ventana)
    ventana_modificar.title("Modificar jugador")
    ventana_modificar.geometry("420x380")
    ventana_modificar.resizable(False, False)

    etiqueta_id = tk.Label(ventana_modificar, text="ID:")
    etiqueta_id.grid(row=0, column=0, padx=15, pady=8, sticky="e")

    caja_id_mod = tk.Entry(ventana_modificar, width=12)
    caja_id_mod.grid(row=0, column=1, pady=8, sticky="w")

    boton_cargar = tk.Button(ventana_modificar, text="Cargar datos", command=cargar_para_modificar)
    boton_cargar.grid(row=0, column=2, padx=10)

    etiquetas = ["Nombre:", "Pais:", "Club:", "Posicion:"]
    cajas_mod = []

    for i in range(4):
        etiqueta = tk.Label(ventana_modificar, text=etiquetas[i])
        etiqueta.grid(row=i + 1, column=0, padx=15, pady=8, sticky="e")
        caja = tk.Entry(ventana_modificar, width=30)
        caja.grid(row=i + 1, column=1, columnspan=2, pady=8, sticky="w")
        cajas_mod.append(caja)

    boton_guardar = tk.Button(ventana_modificar, text="Guardar cambios", width=14, command=guardar_cambios)
    boton_guardar.grid(row=5, column=1, pady=15)

    boton_cerrar = tk.Button(ventana_modificar, text="Cerrar", width=10, command=ventana_modificar.destroy)
    boton_cerrar.grid(row=5, column=2, pady=15)

    lbl_resultado_mod = tk.Label(ventana_modificar, text="", wraplength=380)
    lbl_resultado_mod.grid(row=6, column=0, columnspan=3, padx=15)

    caja_id_mod.focus()
    ventana_modificar.transient(ventana)
    ventana_modificar.wait_visibility()
    ventana_modificar.grab_set()


def eliminar_por_id():
    texto = simpledialog.askstring(
        "Eliminar jugador",
        "Ingrese el id del jugador:",
        parent=ventana
    )

    if texto is None:
        return

    error, jugador, numero, inicio, fin = archivos.buscar_jugador(texto)

    if error != "":
        messagebox.showerror("Error", error)
        return

    respuesta = messagebox.askyesno(
        "Confirmar",
        "Desea eliminar a " + jugador[1] + " (id " + jugador[0] + ")?"
    )

    if respuesta:
        error = archivos.eliminar_jugador(jugador[0])

        if error != "":
            messagebox.showerror("Error", error)
        else:
            messagebox.showinfo("Eliminado", "El jugador fue eliminado.")
            actualizar_estado()


def ver_todos():
    jugadores = archivos.listar_jugadores()

    if jugadores is None:
        messagebox.showerror("Error", "No se pudo leer el archivo de datos.")
        return

    if len(jugadores) == 0:
        messagebox.showinfo("Jugadores", "Todavia no hay jugadores registrados.")
        return

    ventana_lista = tk.Toplevel(ventana)
    ventana_lista.title("Jugadores registrados")
    ventana_lista.geometry("800x380")

    lista = tk.Listbox(ventana_lista, font=("Courier New", 10), width=95, height=16)
    desplazamiento = tk.Scrollbar(ventana_lista, command=lista.yview)
    lista.config(yscrollcommand=desplazamiento.set)
    desplazamiento.pack(side="right", fill="y")
    lista.pack(side="left", fill="both", expand=True)

    titulo = f"{'Reg':<4}{'ID':<7}{'Nombre':<28}{'Pais':<15}{'Club':<26}{'Posicion':<15}"
    lista.insert(tk.END, titulo)

    for jugador in jugadores:
        linea = (
            f"{jugador[0]:<4}{jugador[1]:<7}{jugador[2]:<28}"
            f"{jugador[3]:<15}{jugador[4]:<26}{jugador[5]:<15}"
        )
        lista.insert(tk.END, linea)    


barra = tk.Menu(ventana)
menu_jugadores = tk.Menu(barra, tearoff=0)
menu_jugadores.add_command(label="Agregar jugador", command=abrir_agregar)
menu_jugadores.add_command(label="Buscar por ID", command=buscar_por_id)
menu_jugadores.add_command(label="Modificar jugador", command=abrir_modificar)
menu_jugadores.add_command(label="Eliminar jugador", command=eliminar_por_id)
menu_jugadores.add_command(label="Ver todos", command=ver_todos)
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