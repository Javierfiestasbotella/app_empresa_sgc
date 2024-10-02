import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from PIL import Image, ImageTk
import pandas as pd
import os

# Importar las librerías necesarias
import subprocess
import datetime


# Ruta del directorio donde se guardarán las copias de seguridad
directorio_backup = r"C:\Users\sgcov\Desktop\Codigos python\app_empresa_sgc\copia_seguridad"

# Función para realizar la copia de seguridad
def realizar_backup():
    try:
        # Verificar si el directorio de backup existe, si no, crearlo
        if not os.path.exists(directorio_backup):
            os.makedirs(directorio_backup)
        
        # Obtener la fecha y hora actual para el nombre del archivo de backup
        fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Definir el nombre del archivo de backup con la fecha y hora
        backup_file = os.path.join(directorio_backup, f"backup_clientes_db_{fecha_hora}.backup")
        
        # Ruta completa de pg_dump utilizando la versión 16
        pg_dump_path = r"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe"
        
        # Comando para realizar la copia de seguridad utilizando pg_dump
        command = f'"{pg_dump_path}" -U postgres -h localhost -p 5432 -F c -b -v -f "{backup_file}" clientes_db'
        
        # Ejecutar el comando de copia de seguridad
        subprocess.run(command, shell=True, check=True)
        
        messagebox.showinfo("Copia de Seguridad", f"Copia de seguridad creada con éxito en: {backup_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error de Copia de Seguridad", f"No se pudo crear la copia de seguridad: {e}")
    except Exception as ex:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {ex}")

# Función para exportar las tablas a CSV
def exportar_tablas_csv():
    conn = connect_db()
    if conn:
        try:
            # Lista de tablas que deseas exportar
            tablas = ["clientes", "citas"]
            
            # Verificar si el directorio de exportación existe, si no, crearlo
            if not os.path.exists(directorio_backup):
                os.makedirs(directorio_backup)
            
            for tabla in tablas:
                # Exportar la tabla a un DataFrame de pandas
                df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
                
                # Guardar el DataFrame como un archivo CSV
                df.to_csv(os.path.join(directorio_backup, f"{tabla}_backup.csv"), index=False, encoding="utf-8")
            
            messagebox.showinfo("Exportación", "Tablas exportadas a CSV exitosamente en la carpeta de copia de seguridad")
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo exportar las tablas: {e}")
        finally:
            conn.close()



# Conexión a la base de datos
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="clientes_db",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432",
            options="-c client_encoding=UTF8"
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"Conectado a la base de datos: {version}")
        return conn
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
        return None

# Cargar la imagen de fondo como marca de agua
# Cargar la imagen del logo
# Ruta correcta para el logo
logo_path = 'app_empresa_sgc/logo.png'  # Asegúrate de que esta ruta sea correcta

# Función para agregar el logo a los encabezados del Treeview
def agregar_logo():
    try:
        # Cargar y redimensionar la imagen del logo
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((20, 20), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Crear etiquetas para los encabezados de las columnas con el logo
        columns = ["ID", "Nombre", "Apellidos", "Edad", "Modalidad", "Fecha de Cita"]
        for i, col in enumerate(columns):
            label = ttk.Label(tree_clientes, text=col, image=logo_photo, compound='left')
            tree_clientes.heading(col, text=col, anchor='w')

        # Mantener una referencia a la imagen para evitar que sea recolectada por el recolector de basura
        tree_clientes.logo_photo = logo_photo
    except Exception as e:
        print(f"Error al cargar el logo: {e}")



# Colores
malva_fuerte = "#800080"   # Ejemplo de color malva fuerte
blanco = "#FFFFFF"
negro = "#000000"
light_mauve = "#cd00cd"  # Puedes ajustar el código de color según prefieras




# Crear ventana principal
root = tk.Tk()
root.iconbitmap('app_empresa_sgc/favicon.ico')
root.title("Gestión de Clientes y Citas - Silvia García Cuesta")
root.geometry("1200x700")
root.configure(bg=blanco)  # Fondo blanco para la ventana principal



# Estilo ttk
style = ttk.Style()
style.theme_use("clam")

# Configurar colores para los encabezados del Treeview
style.configure("Treeview.Heading", 
                font=("Helvetica", 12, "bold"), 
                background=malva_fuerte, 
                foreground=blanco)

style.map("Treeview.Heading", 
          background=[("active", light_mauve), ("!active", malva_fuerte)],
          foreground=[("active", blanco), ("!active", blanco)])

# Configurar colores para las filas del Treeview
style.configure("Treeview", 
                font=("Helvetica", 10), 
                rowheight=25, 
                background=blanco, 
                foreground=negro, 
                fieldbackground=blanco)



# Estilo para botones
style.configure("TButton", 
                font=("Helvetica", 12), 
                background=malva_fuerte, 
                foreground=blanco)

style.map("TButton", 
          background=[("active", light_mauve), ("!active", malva_fuerte)],
          foreground=[("active", blanco), ("!active", blanco)])

# Frame para la botonera
button_frame = tk.Frame(root, bg=blanco)  # Fondo blanco para el frame de botones
button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)



# Función para ordenar los datos en el Treeview
def ordenar_por_id():
    # Obtener los datos actuales del Treeview
    items = tree_clientes.get_children()
    datos = [(tree_clientes.set(item, "ID"), item) for item in items]
    
    # Ordenar los datos por la columna "ID"
    datos_ordenados = sorted(datos, key=lambda x: int(x[0]))  # Asegúrate de convertir a int para orden numérico
    
    # Reordenar los ítems en el Treeview
    for index, (valor, item) in enumerate(datos_ordenados):
        tree_clientes.move(item, '', index)
#___________________________________________________
# Frame para mostrar datos
data_frame = tk.Frame(root)
data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Treeview para mostrar datos de clientes
tree_clientes = ttk.Treeview(data_frame, columns=("ID", "Nombre", "Apellidos", "Edad", "Modalidad", "Fecha de Cita"), show="headings")

tree_clientes.heading("ID", text="ID", command=ordenar_por_id)

tree_clientes.heading("Nombre", text="Nombre")
tree_clientes.heading("Apellidos", text="Apellidos")
tree_clientes.heading("Edad", text="Edad")
tree_clientes.heading("Modalidad", text="Modalidad")
tree_clientes.heading("Fecha de Cita", text="Fecha de Cita")
tree_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Treeview para mostrar datos de citas
tree_citas = ttk.Treeview(data_frame, columns=("ID", "Fecha de Cita", "Notas"), show="headings")
tree_citas.heading("ID", text="ID")
tree_citas.heading("Fecha de Cita", text="Fecha de Cita")
tree_citas.heading("Notas", text="Notas")
tree_citas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#para la marca de agua
# Llama a esta función después de haber creado el Treeview y configurado las columnas
agregar_logo()





# Función para cargar citas de un cliente seleccionado
def cargar_citas(cliente_id):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            # Cambiar la consulta para obtener las citas
            cur.execute("SELECT fecha_cita, notas FROM citas WHERE cliente_id = %s ORDER BY fecha_cita", (cliente_id,))
            rows = cur.fetchall()

            # Borrar las citas anteriores en el Treeview
            tree_citas.delete(*tree_citas.get_children())

            # Insertar la fecha de la cita y las notas en el Treeview
            for row in rows:
                fecha_cita, notas = row  # Obtener la fecha de la cita y las notas
                tree_citas.insert("", "end", values=(fecha_cita, notas))  # Insertar la fecha de la cita y las notas
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar las citas: {e}")
        finally:
            conn.close()


# Función para manejar la selección de un cliente
def on_cliente_select(event):
    selected_item = tree_clientes.selection()
    if selected_item:
        cliente_id = tree_clientes.item(selected_item[0])["values"][0]
        cargar_citas(cliente_id)

tree_clientes.bind("<<TreeviewSelect>>", on_cliente_select)

# Funciones para CRUD de Clientes
def agregar_cliente():
    def submit():
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    sql.SQL("INSERT INTO clientes (nombre, apellidos, edad, modalidad, fecha_cita, sexo, movil, email, informacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                    (
                        entry_nombre.get(), 
                        entry_apellidos.get(), 
                        entry_edad.get(), 
                        entry_modalidad.get(), 
                        entry_fecha_cita.get(),
                        entry_sexo.get() if entry_sexo.get() else None, 
                        entry_movil.get() if entry_movil.get() else None, 
                        entry_email.get() if entry_email.get() else None,
                                entry_informacion.get("1.0", tk.END).strip() if entry_informacion.get("1.0", tk.END).strip() else None  # Cambiado aquí

                    )
                )
                conn.commit()
                messagebox.showinfo("Éxito", "Cliente agregado exitosamente")
                top.destroy()
                cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el cliente: {e}")
            finally:
                conn.close()
    
    top = tk.Toplevel(root)
    top.title("Agregar Cliente")
    top.iconbitmap('app_empresa_sgc/favicon.ico')
    
    tk.Label(top, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(top)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(top, text="Apellidos").grid(row=1, column=0, padx=10, pady=5)
    entry_apellidos = tk.Entry(top)
    entry_apellidos.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(top, text="Edad").grid(row=2, column=0, padx=10, pady=5)
    entry_edad = tk.Entry(top)
    entry_edad.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(top, text="Modalidad").grid(row=3, column=0, padx=10, pady=5)
    entry_modalidad = tk.Entry(top)
    entry_modalidad.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(top, text="Fecha de Cita").grid(row=4, column=0, padx=10, pady=5)
    entry_fecha_cita = tk.Entry(top)
    entry_fecha_cita.grid(row=4, column=1, padx=10, pady=5)
    
    tk.Label(top, text="Sexo").grid(row=5, column=0, padx=10, pady=5)
    entry_sexo = tk.Entry(top)
    entry_sexo.grid(row=5, column=1, padx=10, pady=5)
    
    tk.Label(top, text="Móvil").grid(row=6, column=0, padx=10, pady=5)
    entry_movil = tk.Entry(top)
    entry_movil.grid(row=6, column=1, padx=10, pady=5)
    
    tk.Label(top, text="Email").grid(row=7, column=0, padx=10, pady=5)
    entry_email = tk.Entry(top)
    entry_email.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(top, text="Información").grid(row=8, column=0, padx=10, pady=5)
    # Crear un widget Text para múltiples líneas y saltos de línea
    entry_informacion = tk.Text(top, font=("Arial", 12), height=5, width=40)
    entry_informacion.grid(row=8, column=1, padx=10, pady=5)
    
    tk.Button(top, text="Agregar", command=submit).grid(row=9, columnspan=2, pady=10)

def cargar_datos():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clientes")
            rows = cur.fetchall()
            tree_clientes.delete(*tree_clientes.get_children())
            for row in rows:
                tree_clientes.insert("", "end", values=row)
            if rows:
                first_cliente_id = rows[0][0]
                cargar_citas(first_cliente_id)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")
        finally:
            conn.close()

def editar_cliente():
    selected_item = tree_clientes.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un cliente para editar")
        return
    
    def submit():
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    sql.SQL("UPDATE clientes SET nombre=%s, apellidos=%s, edad=%s, modalidad=%s, fecha_cita=%s, sexo=%s, movil=%s, email=%s, informacion=%s WHERE id=%s"),
                    (entry_nombre.get(), entry_apellidos.get(), entry_edad.get(), entry_modalidad.get(), entry_fecha_cita.get(), 
                     entry_sexo.get() if entry_sexo.get() else None, 
                     entry_movil.get() if entry_movil.get() else None, 
                     entry_email.get() if entry_email.get() else None, 
                     entry_informacion.get("1.0", tk.END).strip() if entry_informacion.get("1.0", tk.END).strip() else None,
                     cliente_id)
                )
                conn.commit()
                messagebox.showinfo("Éxito", "Cliente actualizado exitosamente")
                top.destroy()
                cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")
            finally:
                conn.close()
    
    item = tree_clientes.item(selected_item)
    cliente_id, nombre, apellidos, edad, modalidad, fecha_cita, sexo, movil, email, informacion = item["values"]
    
    top = tk.Toplevel(root)
    top.title("Editar Cliente")
    top.iconbitmap('app_empresa_sgc/favicon.ico')

    
    tk.Label(top, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(top)
    entry_nombre.insert(0, nombre)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(top, text="Apellidos").grid(row=1, column=0, padx=10, pady=5)
    entry_apellidos = tk.Entry(top)
    entry_apellidos.insert(0, apellidos)
    entry_apellidos.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(top, text="Edad").grid(row=2, column=0, padx=10, pady=5)
    entry_edad = tk.Entry(top)
    entry_edad.insert(0, edad)
    entry_edad.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(top, text="Modalidad").grid(row=3, column=0, padx=10, pady=5)
    entry_modalidad = tk.Entry(top)
    entry_modalidad.insert(0, modalidad)
    entry_modalidad.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(top, text="Fecha de Cita").grid(row=4, column=0, padx=10, pady=5)
    entry_fecha_cita = tk.Entry(top)
    entry_fecha_cita.insert(0, fecha_cita)
    entry_fecha_cita.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(top, text="Sexo").grid(row=5, column=0, padx=10, pady=5)
    entry_sexo = tk.Entry(top)
    entry_sexo.insert(0, sexo if sexo else "")
    entry_sexo.grid(row=5, column=1, padx=10, pady=5)
    
    tk.Label(top, text="Móvil").grid(row=6, column=0, padx=10, pady=5)
    entry_movil = tk.Entry(top)
    entry_movil.insert(0, movil if movil else "")
    entry_movil.grid(row=6, column=1, padx=10, pady=5)
    
    tk.Label(top, text="Email").grid(row=7, column=0, padx=10, pady=5)
    entry_email = tk.Entry(top)
    entry_email.insert(0, email if email else "")
    entry_email.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(top, text="Información").grid(row=8, column=0, padx=10, pady=5)
    #tk.Label(top, text="Información", font=("Arial", 22)).grid(row=8, column=0, padx=10, pady=5)
    # Crear el Entry (puedes ajustar el tamaño también si lo deseas)
     # Crear el widget Text para "Información" y cargar el texto existente
    entry_informacion = tk.Text(top, font=("Arial", 12), height=5, width=40)
    entry_informacion.grid(row=8, column=1, padx=10, pady=5)
    
    # Insertar el texto de "información" de la base de datos en el widget Text
    if informacion:  # Si existe información previa
        entry_informacion.insert("1.0", informacion)  # Insertar el texto al inicio del Text
    # Crear un widget Text para múltiples líneas y saltos de línea
    #entry_informacion = tk.Text(top, font=("Arial", 12), height=5, width=40)
    #entry_informacion.grid(row=8, column=1, padx=10, pady=5)
    #entry_informacion = tk.Entry(top)
    #entry_informacion.grid(row=8, column=1, padx=10, pady=5)
    
    tk.Button(top, text="Actualizar", command=submit).grid(row=10, columnspan=2, pady=10)


def borrar_cliente():
    selected_item = tree_clientes.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un cliente para borrar")
        return
    
    cliente_id = tree_clientes.item(selected_item)["values"][0]
    
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
            cliente = cur.fetchone()
            if cliente:
                respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que quiere borrar el cliente seleccionado?")
                if respuesta:
                    cur.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Cliente borrado exitosamente")
                    cargar_datos()
                else:
                    messagebox.showinfo("Cancelado", "El cliente no ha sido borrado")
            else:
                messagebox.showerror("Error", "El cliente no existe")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar el cliente: {e}")
        finally:
            conn.close()


def buscar_cliente():
    def buscar():
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                query = "SELECT * FROM clientes WHERE"
                params = []
                
                if entry_id.get():
                    query += " id = %s"
                    params.append(entry_id.get())
                
                if entry_nombre.get():
                    if params:
                        query += " OR"
                    query += " nombre = %s"
                    params.append(entry_nombre.get())
                
                cur.execute(query, tuple(params))
                cliente = cur.fetchone()
                if cliente:
                    mostrar_ficha_cliente(cliente)
                else:
                    messagebox.showinfo("Información", "Cliente no encontrado")
                top.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo buscar el cliente: {e}")
            finally:
                conn.close()

    top = tk.Toplevel(root)
    top.title("Buscar Cliente")
    top.iconbitmap('app_empresa_sgc/favicon.ico')
    
    tk.Label(top, text="ID").grid(row=0, column=0, padx=10, pady=5)
    entry_id = tk.Entry(top)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(top, text="Nombre").grid(row=1, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(top)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Button(top, text="Buscar", command=buscar).grid(row=2, columnspan=2, pady=10)
ventana_notas = None
def mostrar_ficha_cliente(cliente):
    cliente_id, nombre, apellidos, edad, modalidad, fecha_cita, sexo, movil, email, informacion = cliente
    
    top = tk.Toplevel(root)
    top.title(f"Ficha de {nombre} {apellidos}")
    top.iconbitmap('app_empresa_sgc/favicon.ico')
    top.lift()  # Eleva la ventana
    top.focus_force()  # Obliga a que la ventana tenga el foco
    top.grab_set()  # Captura los eventos del mouse y teclado en esta ventana

    # Crear el Notebook (pestañas)
    notebook = ttk.Notebook(top)
    notebook.pack(padx=10, pady=10, fill='both', expand=True)

    # Primera pestaña: Información básica
    frame_info_basica = tk.Frame(notebook)
    frame_info_basica.pack(fill='both', expand=True)
    
    tk.Label(frame_info_basica, text="ID").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=cliente_id).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_info_basica, text="Nombre").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=nombre).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_info_basica, text="Apellidos").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=apellidos).grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame_info_basica, text="Edad").grid(row=3, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=edad).grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame_info_basica, text="Modalidad").grid(row=4, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=modalidad).grid(row=4, column=1, padx=10, pady=5)

    tk.Label(frame_info_basica, text="Fecha de Cita").grid(row=5, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=fecha_cita).grid(row=5, column=1, padx=10, pady=5)

    tk.Label(frame_info_basica, text="Sexo").grid(row=6, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=sexo if sexo else "No especificado").grid(row=6, column=1, padx=10, pady=5)

    tk.Label(frame_info_basica, text="Móvil").grid(row=7, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=movil if movil else "No especificado").grid(row=7, column=1, padx=10, pady=5)

    tk.Label(frame_info_basica, text="Email").grid(row=8, column=0, padx=10, pady=5)
    tk.Label(frame_info_basica, text=email if email else "No especificado").grid(row=8, column=1, padx=10, pady=5)

    # Segunda pestaña: Información extendida (más grande)
    frame_info_extendida = tk.Frame(notebook)
    frame_info_extendida.pack(fill='both', expand=True)

    tk.Label(frame_info_extendida, text="Ficha Cliente",font=("Helvetica", 30)).pack(pady=5)

    text_info_extendida = tk.Text(frame_info_extendida, wrap=tk.WORD, font=("Helvetica", 10), height=80, width=60)
    text_info_extendida.pack(padx=10, pady=5)
    text_info_extendida.insert(tk.END, informacion if informacion else "No especificado")
    text_info_extendida.config(state=tk.DISABLED)

    # Añadir las pestañas al Notebook
    notebook.add(frame_info_basica, text="Información Básica")
    notebook.add(frame_info_extendida, text="Información Completa")

    # Mostrar citas del cliente con scroll
    tk.Label(frame_info_basica, text="Citas:").grid(row=9, column=0, padx=10, pady=5)

    # Crear un frame para contener el Treeview y el Scrollbar
    frame_citas = tk.Frame(frame_info_basica)
    frame_citas.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

    # Crear el Treeview para mostrar las citas del cliente
    tree_citas_cliente = ttk.Treeview(frame_citas, columns=("ID", "Fecha de Cita", "Notas"), show="headings", height=5)
    tree_citas_cliente.heading("ID", text="ID")
    tree_citas_cliente.heading("Fecha de Cita", text="Fecha de Cita")
    tree_citas_cliente.heading("Notas", text="Notas")
    tree_citas_cliente.column("ID", width=50, anchor='center')
    tree_citas_cliente.column("Fecha de Cita", width=120, anchor='center')
    tree_citas_cliente.column("Notas", width=250, anchor='center')

    # Crear el Scrollbar vertical y asociarlo al Treeview
    scrollbar = ttk.Scrollbar(frame_citas, orient="vertical", command=tree_citas_cliente.yview)
    tree_citas_cliente.configure(yscrollcommand=scrollbar.set)

    # Empaquetar el Treeview y el Scrollbar juntos
    tree_citas_cliente.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Conectar a la base de datos y cargar las citas del cliente
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, fecha_cita, notas FROM citas WHERE cliente_id = %s ORDER BY fecha_cita", (cliente_id,))
            citas = cur.fetchall()
            for cita in citas:
                tree_citas_cliente.insert("", "end", values=cita)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las citas: {e}")
        finally:
            conn.close()

    # ----------------------------------------------------------
    # Mostrar las notas de la cita seleccionada en una nueva ventana
    # Declaramos la variable ventana_notas globalmente para rastrear la ventana de notas
    

    # Mostrar las notas de la cita seleccionada en una nueva ventana
    def mostrar_notas(event):
        global ventana_notas  # Usamos la variable global para controlar la ventana abierta

        # Obtenemos la cita seleccionada en el Treeview
        selected_item = tree_citas_cliente.selection()
        if not selected_item:
            return
        
        # Obtenemos la información de la cita seleccionada
        item = tree_citas_cliente.item(selected_item)
        cita_id, fecha_cita, notas = item["values"]

        # Si hay una ventana de notas abierta, la cerramos antes de abrir una nueva
        if ventana_notas is not None and ventana_notas.winfo_exists():
            ventana_notas.destroy()

        # Creamos una nueva ventana para mostrar las notas de la cita seleccionada
        ventana_notas = tk.Toplevel(root)
        ventana_notas.title(f"Notas de la cita {fecha_cita}")
        ventana_notas.iconbitmap('app_empresa_sgc/favicon.ico')

        # Añadimos un label para mostrar las notas de la cita
        tk.Label(ventana_notas, text=notas, wraplength=500).pack(padx=20, pady=20)

        # Permitimos que la ventana se cierre correctamente cuando se pulse la "X"
        ventana_notas.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana())

    # Función que actualiza la variable cuando se cierra la ventana de notas
    def cerrar_ventana():
        global ventana_notas
        ventana_notas.destroy()  # Cerramos la ventana
        ventana_notas = None  # Reiniciamos la variable para futuras notas

    # Asociamos el evento de selección del Treeview para mostrar las notas
    tree_citas_cliente.bind("<<TreeviewSelect>>", mostrar_notas)






# Funciones para CRUD de Citas
def agregar_cita():
    def submit():
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    sql.SQL("INSERT INTO citas (cliente_id, fecha_cita, notas) VALUES (%s, %s, %s)"),
                    (entry_cliente_id.get(), entry_fecha_cita.get(), entry_notas.get("1.0", tk.END).strip())
                )
                conn.commit()
                messagebox.showinfo("Éxito", "Cita agregada exitosamente")
                top.destroy()
                cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la cita: {e}")
            finally:
                conn.close()
    
    top = tk.Toplevel(root)
    top.title("Agregar Cita")
    top.geometry("400x300")
    top.iconbitmap('app_empresa_sgc/favicon.ico')
    
    tk.Label(top, text="Cliente ID").grid(row=0, column=0, padx=10, pady=5)
    entry_cliente_id = tk.Entry(top)
    entry_cliente_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(top, text="Fecha de Cita").grid(row=1, column=0, padx=10, pady=5)
    entry_fecha_cita = tk.Entry(top)
    entry_fecha_cita.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(top, text="Notas").grid(row=2, column=0, padx=10, pady=5)
    entry_notas = tk.Text(top, width=30, height=10)
    entry_notas.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Button(top, text="Agregar", command=submit).grid(row=3, columnspan=2, pady=10)

def editar_cita():
    # Verificar que se haya seleccionado un cliente
    selected_cliente = tree_clientes.selection()
    if not selected_cliente:
        messagebox.showwarning("Advertencia", "Seleccione un cliente para ver sus citas y luego seleccione una cita para editar.")
        return

    # Obtener el ID del cliente seleccionado
    cliente_id = tree_clientes.item(selected_cliente[0])["values"][0]

    # Cargar citas del cliente seleccionado
    def cargar_citas_cliente():
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, fecha_cita, notas FROM citas WHERE cliente_id = %s ORDER BY fecha_cita", (cliente_id,))
                rows = cur.fetchall()
                tree_citas_cliente.delete(*tree_citas_cliente.get_children())
                for row in rows:
                    tree_citas_cliente.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar las citas del cliente: {e}")
            finally:
                conn.close()

    # Crear ventana para mostrar citas y seleccionar una para editar
    top = tk.Toplevel(root)
    top.title("Editar Cita")
    top.geometry("600x400")
    top.iconbitmap('app_empresa_sgc/favicon.ico')

    tk.Label(top, text="Seleccione una cita para editar:").pack(pady=10)

    # Crear Treeview para mostrar citas del cliente
    tree_citas_cliente = ttk.Treeview(top, columns=("ID", "Fecha de Cita", "Notas"), show="headings")
    tree_citas_cliente.heading("ID", text="ID")
    tree_citas_cliente.heading("Fecha de Cita", text="Fecha de Cita")
    tree_citas_cliente.heading("Notas", text="Notas")
    tree_citas_cliente.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    cargar_citas_cliente()  # Cargar las citas del cliente seleccionado

    def submit():
        selected_cita = tree_citas_cliente.selection()
        if not selected_cita:
            messagebox.showwarning("Advertencia", "Seleccione una cita para editar.")
            return

        # Obtener los detalles de la cita seleccionada
        item = tree_citas_cliente.item(selected_cita)
        cita_id, fecha_cita, notas = item["values"]

        # Crear ventana para editar la cita
        top_edit = tk.Toplevel(top)
        top.iconbitmap('app_empresa_sgc/favicon.ico')
        top_edit.title("Editar Cita")
        top_edit.geometry("400x300")

        tk.Label(top_edit, text="Fecha de Cita").grid(row=0, column=0, padx=10, pady=5)
        entry_fecha_cita = tk.Entry(top_edit)
        entry_fecha_cita.insert(0, fecha_cita)
        entry_fecha_cita.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_edit, text="Notas").grid(row=1, column=0, padx=10, pady=5)
        entry_notas = tk.Text(top_edit, width=30, height=10)
        entry_notas.insert("1.0", notas)
        entry_notas.grid(row=1, column=1, padx=10, pady=5)

        def actualizar_cita():
            conn = connect_db()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE citas SET fecha_cita = %s, notas = %s WHERE id = %s",
                        (entry_fecha_cita.get(), entry_notas.get("1.0", tk.END).strip(), cita_id)
                    )
                    conn.commit()
                    messagebox.showinfo("Éxito", "Cita actualizada exitosamente.")
                    cargar_citas_cliente()  # Recargar citas después de la actualización
                    top_edit.destroy()
                    top.destroy()  # Cierra la ventana del listado de citas
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar la cita: {e}")
                finally:
                    conn.close()

        tk.Button(top_edit, text="Actualizar", command=actualizar_cita).grid(row=2, columnspan=2, pady=10)

    tk.Button(top, text="Editar Cita Seleccionada", command=submit).pack(pady=10)

    # Función para cerrar todas las ventanas y refrescar la interfaz principal
    def on_closing():
        top.destroy()
        cargar_datos()  # Asegurar que los datos se recarguen

    top.protocol("WM_DELETE_WINDOW", on_closing)




def borrar_cita():
    # Ventana para seleccionar el cliente y mostrar sus citas
    top = tk.Toplevel(root)
    top.title("Seleccionar Cita para Borrar")
    top.geometry("400x400")
    top.iconbitmap('app_empresa_sgc/favicon.ico')

    # Frame para mostrar las citas del cliente seleccionado
    frame_citas = tk.Frame(top)
    frame_citas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree_citas_cliente = ttk.Treeview(frame_citas, columns=("ID", "Fecha de Cita", "Notas"), show="headings")
    tree_citas_cliente.heading("ID", text="ID")
    tree_citas_cliente.heading("Fecha de Cita", text="Fecha de Cita")
    tree_citas_cliente.heading("Notas", text="Notas")
    tree_citas_cliente.pack(fill=tk.BOTH, expand=True)

    # Función para cargar citas del cliente seleccionado
    def cargar_citas(cliente_id):
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, fecha_cita, notas FROM citas WHERE cliente_id = %s ORDER BY fecha_cita", (cliente_id,))
                rows = cur.fetchall()
                tree_citas_cliente.delete(*tree_citas_cliente.get_children())
                for row in rows:
                    tree_citas_cliente.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar las citas: {e}")
            finally:
                conn.close()

    # Función para manejar la selección de la cita y confirmación de borrado
    def seleccionar_cita(event):
        selected_item = tree_citas_cliente.selection()
        if not selected_item:
            return

        item = tree_citas_cliente.item(selected_item)
        cita_id, fecha_cita, _ = item["values"]

        respuesta = messagebox.askyesno("Confirmación", f"¿Está seguro de que quiere borrar la cita del {fecha_cita}?")
        if respuesta:
            conn = connect_db()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM citas WHERE id = %s", (cita_id,))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Cita borrada exitosamente")
                    cargar_datos()  # Recargar los datos en la interfaz principal
                    top.destroy()  # Cerrar la ventana de selección de cita
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo borrar la cita: {e}")
                finally:
                    conn.close()

    # Cargar citas del cliente seleccionado
    cliente_id = tree_clientes.item(tree_clientes.selection())["values"][0]
    cargar_citas(cliente_id)

    # Asociar evento de selección de cita
    tree_citas_cliente.bind("<<TreeviewSelect>>", seleccionar_cita)

    
def ficha_completa():
    selected_item = tree_clientes.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un cliente para ver la ficha completa")
        return

    item = tree_clientes.item(selected_item)
    cliente_id, nombre, apellidos, edad, modalidad, fecha_cita = item["values"]

    top = tk.Toplevel(root)
    top.title(f"Ficha Completa de {nombre} {apellidos}")

    tk.Label(top, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(top)
    entry_nombre.insert(0, nombre)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(top, text="Apellidos").grid(row=1, column=0, padx=10, pady=5)
    entry_apellidos = tk.Entry(top)
    entry_apellidos.insert(0, apellidos)
    entry_apellidos.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(top, text="Edad").grid(row=2, column=0, padx=10, pady=5)
    entry_edad = tk.Entry(top)
    entry_edad.insert(0, edad)
    entry_edad.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(top, text="Modalidad").grid(row=3, column=0, padx=10, pady=5)
    entry_modalidad = tk.Entry(top)
    entry_modalidad.insert(0, modalidad)
    entry_modalidad.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(top, text="Fecha de Cita").grid(row=4, column=0, padx=10, pady=5)
    entry_fecha_cita = tk.Entry(top)
    entry_fecha_cita.insert(0, fecha_cita)
    entry_fecha_cita.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(top, text="Dirección").grid(row=5, column=0, padx=10, pady=5)
    entry_direccion = tk.Entry(top)
    entry_direccion.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(top, text="Email").grid(row=6, column=0, padx=10, pady=5)
    entry_email = tk.Entry(top)
    entry_email.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(top, text="Sexo").grid(row=7, column=0, padx=10, pady=5)
    entry_sexo = tk.Entry(top)
    entry_sexo.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(top, text="Teléfono").grid(row=8, column=0, padx=10, pady=5)
    entry_telefono = tk.Entry(top)
    entry_telefono.grid(row=8, column=1, padx=10, pady=5)

    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT direccion, email, sexo, telefono FROM clientes WHERE id = %s", (cliente_id,))
            cliente_info = cur.fetchone()
            if cliente_info:
                direccion, email, sexo, telefono = cliente_info
                entry_direccion.insert(0, direccion or "")
                entry_email.insert(0, email or "")
                entry_sexo.insert(0, sexo or "")
                entry_telefono.insert(0, telefono or "")
            else:
                messagebox.showerror("Error", "No se encontró información adicional para este cliente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la ficha completa del cliente: {e}")
        finally:
            conn.close()

    def guardar():
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    sql.SQL("UPDATE clientes SET nombre=%s, apellidos=%s, edad=%s, modalidad=%s, fecha_cita=%s, direccion=%s, email=%s, sexo=%s, telefono=%s WHERE id=%s"),
                    (entry_nombre.get(), entry_apellidos.get(), entry_edad.get(), entry_modalidad.get(), entry_fecha_cita.get(), entry_direccion.get(), entry_email.get(), entry_sexo.get(), entry_telefono.get(), cliente_id)
                )
                conn.commit()
                messagebox.showinfo("Éxito", "Ficha del cliente actualizada exitosamente")
                top.destroy()
                cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la ficha del cliente: {e}")
            finally:
                conn.close()

    tk.Button(top, text="Guardar", command=guardar).grid(row=9, columnspan=2, pady=10)



# Botones para operaciones CRUD de clientes y citas con estilo
ttk.Button(button_frame, text="Agregar Cliente", command=agregar_cliente, style="TButton").pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Editar Cliente", command=editar_cliente, style="TButton").pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Borrar Cliente", command=borrar_cliente, style="TButton").pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Buscar Cliente", command=buscar_cliente, style="TButton").pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Cargar Datos", command=cargar_datos, style="TButton").pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Agregar Cita", command=agregar_cita, style="TButton").pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Editar Cita", command=editar_cita, style="TButton").pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Borrar Cita", command=borrar_cita, style="TButton").pack(side=tk.LEFT, padx=5)

# Botones para realizar la copia de seguridad y exportar a CSV
ttk.Button(button_frame, text="Backup", command=realizar_backup, style="TButton").pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Exportar CSV", command=exportar_tablas_csv, style="TButton").pack(side=tk.LEFT, padx=5)



# Inicializar datos
cargar_datos()

root.mainloop()
