from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from conexion import *

class InterfazGrafica:
    def __init__(self):
        self.comunicador = Comunicar()

        self.ventana = Tk()
        self.ventana.title("Inserción y Visualización de Datos")
        self.ventana.geometry("1100x400")
        
       # Crear un menú en la parte superior
        self.menu_superior = Menu(self.ventana)
        self.ventana.config(menu=self.menu_superior)

        # Menú desplegable para seleccionar la tabla
        self.tabla_menu = Menu(self.menu_superior, tearoff=0)
        self.menu_superior.add_cascade(label="Seleccionar Tabla", menu=self.tabla_menu)
        self.tabla_menu.add_command(label="Tabla 1", command=self.seleccionar_tabla1)
        self.tabla_menu.add_command(label="Tabla 2", command=self.seleccionar_tabla2)

        # Botón para eliminar registro
        self.boton_eliminar = Button(self.menu_superior, text="Eliminar Registro", command=self.eliminar_registro)
        self.menu_superior.add_cascade(label="Eliminar", menu=self.boton_eliminar)
        
        # Botón para actualizar registro
        self.boton_actualizar = Button(self.menu_superior, text="Actualizar", command=None)
        self.menu_superior.add_cascade(label="Actualizar", menu=self.boton_actualizar)
        
        # Parte superior: Campos de entrada para ingresar datos
        self.frame_superior = Frame(self.ventana)
        self.frame_superior.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        # Botón para insertar
        self.insertar_button = Button(self.frame_superior, text="Insertar", command=self.insertar_registro)
        self.insertar_button.grid(row=0, column=5, columnspan=2)

        # Parte inferior: Vista de los datos existentes
        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        self.vista_label = Label(self.frame_inferior, text="Datos existentes:")
        self.vista_label.grid(row=0, column=0, columnspan=2)

        self.vista_tabla = ttk.Treeview(self.frame_inferior, columns=("ID", "Id Area","Nombre", "Abreviatura"))
        self.vista_tabla.heading("#1", text="ID")
        self.vista_tabla.heading("#2", text="Id Area")
        self.vista_tabla.heading("#3", text="Nombre")
        self.vista_tabla.heading("#4", text="Abreviatura")
        self.vista_tabla.grid(row=1, column=0, columnspan=2)

        # Inicialmente, muestra los datos de la tabla 1
        self.seleccionar_tabla1()

    def seleccionar_tabla1(self):
        self.destruir_campos_existente()
        self.crear_campos_tabla1()
        self.cargar_datos_existentes("Tabla 1")

    def seleccionar_tabla2(self):
        self.destruir_campos_existente()
        self.crear_campos_tabla2()
        self.cargar_datos_existentes("Tabla 2")
    
    def crear_campos_tabla1(self):
        self.campo1_label = Label(self.frame_superior, text="Nombre:")
        self.campo1_label.grid(row=0, column=0,padx=10)
        self.campo1_entry = Entry(self.frame_superior)
        self.campo1_entry.grid(row=0, column=1,padx=10)

        self.campo2_label = Label(self.frame_superior, text="Abreviatura:")
        self.campo2_label.grid(row=1, column=0,padx=10)
        self.campo2_entry = Entry(self.frame_superior)
        self.campo2_entry.grid(row=1, column=1,padx=10)
        
        self.campo3_label = Label(self.frame_superior, text="Id Area:")
        self.campo3_label.grid(row=2, column=0,padx=10)
        self.campo3_entry = Entry(self.frame_superior)
        self.campo3_entry.grid(row=2, column=1,padx=10)
        
    def crear_campos_tabla2(self):
        self.campo1_label = Label(self.frame_superior, text="Id Facultad:")
        self.campo1_label.grid(row=0, column=4)
        self.campo1_entry = Entry(self.frame_superior)
        self.campo1_entry.grid(row=0, column=5)

        self.campo2_label = Label(self.frame_superior, text="Nombre:")
        self.campo2_label.grid(row=1, column=4)
        self.campo2_entry = Entry(self.frame_superior)
        self.campo2_entry.grid(row=1, column=5)

        self.campo3_label = Label(self.frame_superior, text="Codigo Programa:")  # Campo adicional para la tabla 2
        self.campo3_label.grid(row=2, column=4)
        self.campo3_entry = Entry(self.frame_superior)
        self.campo3_entry.grid(row=2, column=5)
        
        self.campo4_label = Label(self.frame_superior, text="Tipo:")  # Campo adicional para la tabla 2
        self.campo4_label.grid(row=3, column=4)
        self.campo4_entry = Entry(self.frame_superior)
        self.campo4_entry.grid(row=3, column=5)
    
    def destruir_campos_existente(self):
        for widget in self.frame_superior.winfo_children():
            widget.destroy()

    def cargar_datos_existentes(self, tabla):
        try:
            query = "SELECT * FROM dicfacultades" if tabla == "Tabla 1" else "SELECT * FROM dicprogramas"
            self.comunicador.cursor.execute(query)
            resultados = self.comunicador.cursor.fetchall()
            
            # Limpiar la tabla antes de cargar nuevos datos
            self.vista_tabla.delete(*self.vista_tabla.get_children())
            
            # Configurar las columnas en la vista de la tabla
            columnas_tabla1 = ("ID", "Nombre", "Abreviatura","Id Area")
            columnas_tabla2 = ("ID","ID Facultad", "Nombre", "Codigo Programa","Tipo")
            columnas = columnas_tabla1 if tabla == "Tabla 1" else columnas_tabla2
            self.vista_tabla["columns"] = columnas
            for i, columna in enumerate(columnas, 1):
                self.vista_tabla.heading(f"#{i}", text=columna, anchor='center')  # Alinea al centro
                
            for resultado in resultados:
                self.vista_tabla.insert("", "end", values=resultado)
        except Exception as e:
            print(f"Error al cargar datos desde la base de datos: {str(e)}")
            
    def insertar_registro(self):
        tabla_seleccionada = self.tabla_var.get()
        campo1_valor = self.campo1_entry.get()
        campo2_valor = self.campo2_entry.get()

        if tabla_seleccionada == "Tabla 1":
            datos = {
                "campo1": campo1_valor,
                "campo2": campo2_valor
            }
            self.comunicador.insertar_tabla1(datos)
        elif tabla_seleccionada == "Tabla 2":
            datos = {
                "campo1": campo1_valor,
                "campo2": campo2_valor
            }
            self.comunicador.insertar_tabla2(datos)

        messagebox.showinfo("Inserción", "Registro insertado correctamente.")

        # Limpiar campos de entrada después de la inserción
        self.campo1_entry.delete(0, END)
        self.campo2_entry.delete(0, END)

    def eliminar_registro(self):
        # Verificar si se ha seleccionado un registro
        if self.id_seleccionado is None:
            messagebox.showwarning("Eliminar Registro", "Por favor, seleccione un registro para eliminar.")
            return

        # Preguntar al usuario si realmente desea eliminar el registro
        confirmacion = messagebox.askyesno("Eliminar Registro", "¿Está seguro de que desea eliminar este registro?")

        if confirmacion:
            try:
                # Ejecutar la consulta SQL para eliminar el registro utilizando self.id_seleccionado
                query = "DELETE FROM dicprogramas WHERE ID = %s"
                self.comunicador.cursor.execute(query, (self.id_seleccionado,))
                self.comunicador.conexion.commit()

                # Actualizar la vista de la tabla para reflejar los cambios
                self.cargar_datos_existentes("Tabla 1")
                messagebox.showinfo("Eliminar Registro", "Registro eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Eliminar Registro", f"Error al eliminar el registro: {str(e)}")

    def iniciar(self):
        self.ventana.mainloop()

interfaz = InterfazGrafica()
interfaz.iniciar()
