import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import math
import archivos
import exportar

verde_oscuro = "#0d3b20"
verde_cancha = "#1e7d3c"
verde_claro = "#27944a"
blanco = "#f7f7f2"
amarillo = "#ffd23f"
negro = "#101c15"
rojo = "#ff6b5e"
verde_led = "#6dff8f"

ventana = tk.Tk()
ventana.title("Registro de Jugadores de Futbol")
ventana.geometry("1000x700")
ventana.resizable(False, False)
ventana.config(bg=verde_oscuro)

estilo_tabla = ttk.Style()
estilo_tabla.theme_use("clam")
estilo_tabla.configure("Treeview", background=blanco, fieldbackground=blanco, foreground=negro, rowheight=26, font=("Arial", 10))
estilo_tabla.configure("Treeview.Heading", background=verde_cancha, foreground=blanco, font=("Arial", 10, "bold"))
estilo_tabla.map("Treeview", background=[("selected", amarillo)], foreground=[("selected", negro)])
estilo_tabla.configure("Vertical.TScrollbar", background=verde_cancha, troughcolor=negro)

ventana_agregar = None
cajas_agregar = []
lbl_resultado = None

ventana_modificar = None
caja_id_mod = None
cajas_mod = []
lbl_resultado_mod = None
id_cargado = ""


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
    for fila in tabla.get_children():
        tabla.delete(fila)

    filtro = caja_filtro.get().strip().lower()
    jugadores = archivos.listar_jugadores()

    if jugadores is None:
        val_activos.config(text="--")
        val_registros.config(text="--")
        val_tamano.config(text="--")
        val_integridad.config(text="ERROR", fg=rojo)
        lbl_conteo.config(text="")
        lbl_aviso.config(text="No se pudo leer el archivo de datos.")
        return

    mostrados = 0

    for jugador in jugadores:
        texto = jugador[1] + " " + jugador[2] + " " + jugador[3] + " " + jugador[4] + " " + jugador[5]

        if filtro in texto.lower():
            if mostrados % 2 == 0:
                fila_tag = "par"
            else:
                fila_tag = "impar"

            tabla.insert("", tk.END, values=(jugador[0], jugador[1], jugador[2], jugador[3], jugador[4], jugador[5]), tags=(fila_tag,))
            mostrados = mostrados + 1

    lbl_conteo.config(text="Mostrando " + str(mostrados) + " de " + str(len(jugadores)))
    val_activos.config(text=str(len(jugadores)))

    try:
        val_registros.config(text=str(archivos.contar_registros()))
    except OSError:
        val_registros.config(text="--")

    error, tamano, modificado, puede_leer, puede_escribir = archivos.informacion_archivo()
    if error == "":
        val_tamano.config(text=str(tamano))
    else:
        val_tamano.config(text="--")

    estado_hash = archivos.verificar_hash()[0]
    if estado_hash == "ok":
        val_integridad.config(text="OK", fg=verde_led)
    elif estado_hash == "alterado":
        val_integridad.config(text="ALERTA", fg=rojo)
    elif estado_hash == "sin_hash":
        val_integridad.config(text="SIN HASH", fg=amarillo)
    else:
        val_integridad.config(text="ERROR", fg=rojo)

    aviso = ""
    try:
        if not archivos.archivo_completo():
            aviso = "Aviso: hay un registro incompleto al final del archivo."
    except OSError:
        aviso = "Aviso: no se pudo revisar el archivo de datos."
    lbl_aviso.config(text=aviso)


def al_filtrar(evento):
    actualizar_estado()


def mostrar_todos():
    caja_filtro.delete(0, tk.END)
    actualizar_estado()


def guardar_jugador():
    datos = []
    for caja in cajas_agregar:
        datos.append(caja.get())

    error, numero, inicio, fin = archivos.agregar_jugador(datos)

    if error != "":
        lbl_resultado.config(text=error, fg=rojo)
    else:
        lbl_resultado.config(
            text="Jugador guardado en el registro " + str(numero) + ".\n"
            "Posicion con tell(): " + str(inicio) + " a " + str(fin) + " bytes.",
            fg=verde_led
        )
        for caja in cajas_agregar:
            caja.delete(0, tk.END)
        cajas_agregar[0].focus()
        actualizar_estado()


def abrir_agregar():
    global ventana_agregar, cajas_agregar, lbl_resultado

    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar jugador")
    ventana_agregar.geometry("420x400")
    ventana_agregar.resizable(False, False)
    ventana_agregar.config(bg=verde_oscuro)

    lbl_cabecera = tk.Label(ventana_agregar, text="NUEVO JUGADOR", bg=negro, fg=amarillo, font=("Arial", 14, "bold"), pady=12)
    lbl_cabecera.pack(fill="x")

    formulario = tk.Frame(ventana_agregar, bg=verde_oscuro)
    formulario.pack(pady=15)

    etiquetas = ["ID", "Nombre", "Pais", "Club", "Posicion"]
    cajas_agregar = []

    for i in range(5):
        etiqueta = tk.Label(formulario, text=etiquetas[i], bg=verde_oscuro, fg=blanco, font=("Arial", 10, "bold"))
        etiqueta.grid(row=i, column=0, padx=10, pady=8, sticky="e")
        caja = tk.Entry(formulario, width=30, font=("Arial", 10), bg=blanco, fg=negro, relief="flat")
        caja.grid(row=i, column=1, pady=8, ipady=3)
        cajas_agregar.append(caja)

    boton_guardar = tk.Button(formulario, text="Guardar", width=12, bg=amarillo, fg=negro, relief="flat", font=("Arial", 10, "bold"), command=guardar_jugador)
    boton_guardar.grid(row=5, column=0, pady=15, padx=10)

    boton_cerrar = tk.Button(formulario, text="Cerrar", width=12, bg=verde_cancha, fg=blanco, relief="flat", font=("Arial", 10, "bold"), command=ventana_agregar.destroy)
    boton_cerrar.grid(row=5, column=1, pady=15)

    lbl_resultado = tk.Label(ventana_agregar, text="", bg=verde_oscuro, fg=blanco, font=("Arial", 10), wraplength=360)
    lbl_resultado.pack()

    cajas_agregar[0].focus()
    ventana_agregar.transient(ventana)
    ventana_agregar.wait_visibility()
    ventana_agregar.grab_set()


def cargar_para_modificar():
    global id_cargado

    error, jugador, numero, inicio, fin = archivos.buscar_jugador(caja_id_mod.get())

    for caja in cajas_mod:
        caja.delete(0, tk.END)

    if error != "":
        id_cargado = ""
        lbl_resultado_mod.config(text=error, fg=rojo)
    else:
        id_cargado = jugador[0]
        for i in range(4):
            cajas_mod[i].insert(0, jugador[i + 1])
        lbl_resultado_mod.config(text="Jugador cargado. Cambie los datos y guarde.", fg=amarillo)


def guardar_cambios():
    if id_cargado == "":
        lbl_resultado_mod.config(text="Primero cargue un jugador con el boton Cargar datos.", fg=rojo)
        return

    nuevos = []
    for caja in cajas_mod:
        nuevos.append(caja.get())

    error, inicio, fin = archivos.modificar_jugador(id_cargado, nuevos)

    if error != "":
        lbl_resultado_mod.config(text=error, fg=rojo)
    else:
        lbl_resultado_mod.config(
            text="Jugador modificado en su lugar.\n"
            "Posicion con tell(): " + str(inicio) + " a " + str(fin) + " bytes.",
            fg=verde_led
        )
        actualizar_estado()


def abrir_modificar(id_inicial=""):
    global ventana_modificar, caja_id_mod, cajas_mod, lbl_resultado_mod, id_cargado

    id_cargado = ""

    ventana_modificar = tk.Toplevel(ventana)
    ventana_modificar.title("Modificar jugador")
    ventana_modificar.geometry("470x430")
    ventana_modificar.resizable(False, False)
    ventana_modificar.config(bg=verde_oscuro)

    lbl_cabecera = tk.Label(ventana_modificar, text="MODIFICAR JUGADOR", bg=negro, fg=amarillo, font=("Arial", 14, "bold"), pady=12)
    lbl_cabecera.pack(fill="x")

    formulario = tk.Frame(ventana_modificar, bg=verde_oscuro)
    formulario.pack(pady=15)

    etiqueta_id = tk.Label(formulario, text="ID", bg=verde_oscuro, fg=blanco, font=("Arial", 10, "bold"))
    etiqueta_id.grid(row=0, column=0, padx=10, pady=8, sticky="e")

    caja_id_mod = tk.Entry(formulario, width=12, font=("Arial", 10), bg=blanco, fg=negro, relief="flat")
    caja_id_mod.grid(row=0, column=1, pady=8, ipady=3, sticky="w")

    boton_cargar = tk.Button(formulario, text="Cargar datos", bg=verde_cancha, fg=blanco, relief="flat", font=("Arial", 10, "bold"), command=cargar_para_modificar)
    boton_cargar.grid(row=0, column=2, padx=10)

    etiquetas = ["Nombre", "Pais", "Club", "Posicion"]
    cajas_mod = []

    for i in range(4):
        etiqueta = tk.Label(formulario, text=etiquetas[i], bg=verde_oscuro, fg=blanco, font=("Arial", 10, "bold"))
        etiqueta.grid(row=i + 1, column=0, padx=10, pady=8, sticky="e")
        caja = tk.Entry(formulario, width=30, font=("Arial", 10), bg=blanco, fg=negro, relief="flat")
        caja.grid(row=i + 1, column=1, columnspan=2, pady=8, ipady=3, sticky="w")
        cajas_mod.append(caja)

    boton_guardar = tk.Button(formulario, text="Guardar cambios", width=15, bg=amarillo, fg=negro, relief="flat", font=("Arial", 10, "bold"), command=guardar_cambios)
    boton_guardar.grid(row=5, column=1, pady=15, sticky="w")

    boton_cerrar = tk.Button(formulario, text="Cerrar", width=10, bg=verde_cancha, fg=blanco, relief="flat", font=("Arial", 10, "bold"), command=ventana_modificar.destroy)
    boton_cerrar.grid(row=5, column=2, pady=15)

    lbl_resultado_mod = tk.Label(ventana_modificar, text="", bg=verde_oscuro, fg=blanco, font=("Arial", 10), wraplength=400)
    lbl_resultado_mod.pack()

    if id_inicial != "":
        caja_id_mod.insert(0, id_inicial)
        cargar_para_modificar()
    else:
        caja_id_mod.focus()

    ventana_modificar.transient(ventana)
    ventana_modificar.wait_visibility()
    ventana_modificar.grab_set()


def editar_seleccion(evento):
    seleccion = tabla.selection()

    if len(seleccion) == 0:
        return

    valores = tabla.item(seleccion[0], "values")
    abrir_modificar(str(valores[1]))


def buscar_por_id():
    texto = simpledialog.askstring("Buscar por ID", "Ingrese el id del jugador:", parent=ventana)

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


def eliminar_por_id():
    texto = simpledialog.askstring("Eliminar jugador", "Ingrese el id del jugador:", parent=ventana)

    if texto is None:
        return

    error, jugador, numero, inicio, fin = archivos.buscar_jugador(texto)

    if error != "":
        messagebox.showerror("Error", error)
        return

    respuesta = messagebox.askyesno("Confirmar", "Desea eliminar a " + jugador[1] + " (id " + jugador[0] + ")?")

    if respuesta:
        error = archivos.eliminar_jugador(jugador[0])

        if error != "":
            messagebox.showerror("Error", error)
        else:
            messagebox.showinfo("Eliminado", "El jugador fue eliminado.")
            actualizar_estado()


def exportar_a_json():
    error, total = exportar.exportar_json()

    if error != "":
        messagebox.showerror("Error", error)
    else:
        messagebox.showinfo("Exportacion", "Se exportaron " + str(total) + " jugadores a:\n" + exportar.RUTA_JSON)


def generar_reporte_pdf():
    error, total = exportar.generar_pdf()

    if error != "":
        messagebox.showerror("Error", error)
    else:
        messagebox.showinfo("Reporte PDF", "Se genero el reporte con " + str(total) + " jugadores en:\n" + exportar.RUTA_PDF)


def revisar_hash_inicial():
    estado, guardado, actual = archivos.verificar_hash()

    if estado == "sin_hash":
        try:
            archivos.guardar_hash()
        except OSError:
            messagebox.showerror("Error", "No se pudo crear el archivo jugadores.sha256.")

    elif estado == "alterado":
        messagebox.showwarning(
            "Archivo alterado",
            "El archivo jugadores.dat fue modificado fuera de la aplicacion.\n"
            "Use Herramientas > Verificar integridad para revisarlo."
        )

    elif estado == "error":
        messagebox.showerror("Error", "No se pudo verificar la integridad del archivo.")


def verificar_integridad():
    estado, guardado, actual = archivos.verificar_hash()

    if estado == "ok":
        messagebox.showinfo("Integridad", "El archivo esta integro.\n\nSHA-256 actual:\n" + actual)

    elif estado == "sin_hash":
        try:
            archivos.guardar_hash()
            messagebox.showinfo("Integridad", "No habia un hash guardado. Se creo con el contenido actual del archivo.")
        except OSError:
            messagebox.showerror("Error", "No se pudo crear el archivo jugadores.sha256.")

    elif estado == "alterado":
        respuesta = messagebox.askyesno(
            "Archivo alterado",
            "El archivo jugadores.dat fue modificado fuera de la aplicacion.\n\n"
            "SHA-256 guardado:\n" + guardado + "\n\n"
            "SHA-256 actual:\n" + actual + "\n\n"
            "Desea aceptar el archivo actual y actualizar el hash?"
        )

        if respuesta:
            try:
                archivos.guardar_hash()
                messagebox.showinfo("Integridad", "El hash fue actualizado.")
            except OSError:
                messagebox.showerror("Error", "No se pudo actualizar el hash.")

    else:
        messagebox.showerror("Error", "No se pudo verificar la integridad del archivo.")

    actualizar_estado()


def hacer_respaldo():
    error, ruta_zip, original, comprimido = archivos.crear_respaldo()

    if error != "":
        messagebox.showerror("Error", error)
        return

    if original == 0:
        reduccion = 0
    else:
        reduccion = ((original - comprimido) / original) * 100

    texto = "Respaldo creado en:\n" + ruta_zip + "\n\n"
    texto = texto + "Tamano original: " + str(original) + " bytes\n"
    texto = texto + "Tamano del ZIP: " + str(comprimido) + " bytes\n"
    texto = texto + f"Reduccion: {reduccion:.2f}%"
    messagebox.showinfo("Respaldo ZIP", texto)


def mostrar_informacion():
    error, tamano, modificado, puede_leer, puede_escribir = archivos.informacion_archivo()

    if error != "":
        messagebox.showerror("Error", error)
        return

    if puede_leer:
        permiso_lectura = "Si"
    else:
        permiso_lectura = "No"

    if puede_escribir:
        permiso_escritura = "Si"
    else:
        permiso_escritura = "No"

    texto = "Archivo: " + archivos.RUTA_DATOS + "\n"
    texto = texto + "Tamano: " + str(tamano) + " bytes\n"
    texto = texto + "Registros completos: " + str(tamano // archivos.TAM_REGISTRO) + "\n"
    texto = texto + "Ultima modificacion: " + modificado + "\n"
    texto = texto + "Permiso de lectura: " + permiso_lectura + "\n"
    texto = texto + "Permiso de escritura: " + permiso_escritura
    messagebox.showinfo("Informacion del archivo", texto)


def revisar_indice_inicial():
    if archivos.indice_correcto():
        return

    respuesta = messagebox.askyesno(
        "Indice",
        "El archivo indice.json no existe, esta danado o no coincide con jugadores.dat.\n\n"
        "Desea reconstruirlo ahora?"
    )

    if respuesta:
        reconstruir_indice()


def reconstruir_indice():
    error, total = archivos.reconstruir_indice()

    if error != "":
        messagebox.showerror("Error", error)
    else:
        messagebox.showinfo("Indice reconstruido", "Se indexaron " + str(total) + " jugadores activos.")
        actualizar_estado()


def dibujar_balon(x, y):
    banner.create_oval(x - 12, y - 12, x + 12, y + 12, fill=blanco, outline=negro)

    puntos = []
    for i in range(5):
        angulo = math.radians(-90 + i * 72)
        puntos.append(x + 5 * math.cos(angulo))
        puntos.append(y + 5 * math.sin(angulo))
        banner.create_line(x + 5 * math.cos(angulo), y + 5 * math.sin(angulo), x + 12 * math.cos(angulo), y + 12 * math.sin(angulo), fill=negro)

    banner.create_polygon(puntos, fill=negro)


def crear_casilla(titulo):
    marco = tk.Frame(marcador, bg=negro, padx=16, pady=6, highlightthickness=1, highlightbackground=amarillo)
    marco.pack(side="left", padx=8, pady=10)

    lbl_titulo_casilla = tk.Label(marco, text=titulo, bg=negro, fg=blanco, font=("Arial", 8, "bold"))
    lbl_titulo_casilla.pack()

    valor = tk.Label(marco, text="0", bg=negro, fg=amarillo, font=("Consolas", 24, "bold"))
    valor.pack()

    return valor


barra = tk.Menu(ventana)

menu_jugadores = tk.Menu(barra, tearoff=0)
menu_jugadores.add_command(label="Agregar jugador", command=abrir_agregar)
menu_jugadores.add_command(label="Buscar por ID", command=buscar_por_id)
menu_jugadores.add_command(label="Modificar jugador", command=abrir_modificar)
menu_jugadores.add_command(label="Eliminar jugador", command=eliminar_por_id)
menu_jugadores.add_command(label="Ver todos", command=mostrar_todos)
menu_jugadores.add_separator()
menu_jugadores.add_command(label="Salir", command=ventana.destroy)
barra.add_cascade(label="Jugadores", menu=menu_jugadores)

menu_exportar = tk.Menu(barra, tearoff=0)
menu_exportar.add_command(label="Exportar a JSON", command=exportar_a_json)
menu_exportar.add_command(label="Generar reporte PDF", command=generar_reporte_pdf)
barra.add_cascade(label="Exportar", menu=menu_exportar)

menu_herramientas = tk.Menu(barra, tearoff=0)
menu_herramientas.add_command(label="Verificar integridad", command=verificar_integridad)
menu_herramientas.add_command(label="Crear respaldo ZIP", command=hacer_respaldo)
menu_herramientas.add_command(label="Informacion del archivo", command=mostrar_informacion)
menu_herramientas.add_command(label="Reconstruir indice", command=reconstruir_indice)
barra.add_cascade(label="Herramientas", menu=menu_herramientas)

menu_ayuda = tk.Menu(barra, tearoff=0)
menu_ayuda.add_command(label="Estructura del registro", command=mostrar_estructura)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)
barra.add_cascade(label="Ayuda", menu=menu_ayuda)

ventana.config(menu=barra)

banner = tk.Canvas(ventana, width=1000, height=100, highlightthickness=0)
banner.pack(side="top")

for i in range(0, 1000, 50):
    if (i // 50) % 2 == 0:
        color = verde_cancha
    else:
        color = verde_claro
    banner.create_rectangle(i, 0, i + 50, 100, fill=color, outline=color)

banner.create_rectangle(10, 10, 990, 90, outline=blanco, width=2)
banner.create_line(500, 10, 500, 90, fill=blanco, width=2)
banner.create_oval(463, 13, 537, 87, outline=blanco, width=2)
banner.create_oval(497, 47, 503, 53, fill=blanco, outline=blanco)
banner.create_rectangle(10, 22, 110, 78, outline=blanco, width=2)
banner.create_rectangle(10, 38, 40, 62, outline=blanco, width=2)
banner.create_rectangle(890, 22, 990, 78, outline=blanco, width=2)
banner.create_rectangle(960, 38, 990, 62, outline=blanco, width=2)
dibujar_balon(75, 50)
dibujar_balon(925, 50)

marcador = tk.Frame(ventana, bg=verde_oscuro)
marcador.pack(side="bottom", fill="x")

val_activos = crear_casilla("ACTIVOS")
val_registros = crear_casilla("REGISTROS")
val_bytes = crear_casilla("BYTES POR REG")
val_tamano = crear_casilla("TAMANO EN BYTES")
val_integridad = crear_casilla("INTEGRIDAD")
val_bytes.config(text=str(archivos.TAM_REGISTRO))

lbl_aviso = tk.Label(marcador, text="", bg=verde_oscuro, fg=rojo, font=("Arial", 10, "bold"), wraplength=230, justify="left")
lbl_aviso.pack(side="left", padx=15)

zona = tk.Frame(ventana, bg=verde_oscuro)
zona.pack(side="top", fill="both", expand=True, padx=30, pady=12)

encabezado = tk.Frame(zona, bg=verde_oscuro)
encabezado.pack(fill="x", pady=(0, 10))

titulos = tk.Frame(encabezado, bg=verde_oscuro)
titulos.pack(side="left")

lbl_titulo = tk.Label(titulos, text="Jugadores registrados", bg=verde_oscuro, fg=amarillo, font=("Arial", 16, "bold"))
lbl_titulo.pack(anchor="w")

lbl_conteo = tk.Label(titulos, text="", bg=verde_oscuro, fg=blanco, font=("Arial", 9))
lbl_conteo.pack(anchor="w")

caja_filtro = tk.Entry(encabezado, width=26, font=("Arial", 10), bg=blanco, fg=negro, relief="flat")
caja_filtro.pack(side="right", ipady=3)
caja_filtro.bind("<KeyRelease>", al_filtrar)

lbl_filtro = tk.Label(encabezado, text="Filtrar", bg=verde_oscuro, fg=blanco, font=("Arial", 10, "bold"))
lbl_filtro.pack(side="right", padx=8)

contenedor_tabla = tk.Frame(zona, bg=verde_oscuro)
contenedor_tabla.pack(fill="both", expand=True)

columnas = ("reg", "id", "nombre", "pais", "club", "posicion")
encabezados = ["Reg", "ID", "Nombre", "Pais", "Club", "Posicion"]
anchos = [60, 80, 250, 150, 200, 150]

tabla = ttk.Treeview(contenedor_tabla, columns=columnas, show="headings")

for i in range(len(columnas)):
    if i < 2:
        tabla.heading(columnas[i], text=encabezados[i], anchor="center")
        tabla.column(columnas[i], width=anchos[i], anchor="center")
    else:
        tabla.heading(columnas[i], text=encabezados[i], anchor="w")
        tabla.column(columnas[i], width=anchos[i], anchor="w")

tabla.tag_configure("par", background="#ffffff")
tabla.tag_configure("impar", background="#e3f1e6")
tabla.bind("<Double-1>", editar_seleccion)

desplazamiento = ttk.Scrollbar(contenedor_tabla, orient="vertical", command=tabla.yview)
tabla.config(yscrollcommand=desplazamiento.set)
desplazamiento.pack(side="right", fill="y")
tabla.pack(side="left", fill="both", expand=True)

error = archivos.preparar_archivos()
actualizar_estado()
ventana.update()

if error != "":
    messagebox.showerror("Error", error)
else:
    revisar_indice_inicial()
    revisar_hash_inicial()

actualizar_estado()

ventana.mainloop()