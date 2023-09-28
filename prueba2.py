import tkinter as tk
from tkinter import ttk
import mysql.connector

class GUI:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Consulta Multitabla")
        
        self.frame = ttk.Frame(ventana)
        self.frame.pack(padx=20, pady=20)
        
        self.treeview = ttk.Treeview(self.frame, columns=("Numero", "Abreviatura", "Nombre del Programa"))
        self.treeview.heading("#1", text="Número")
        self.treeview.heading("#2", text="Abreviatura")
        self.treeview.heading("#3", text="Nombre del Programa")
        self.treeview.pack(padx=10, pady=10)
        
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            # Conectar a la base de datos MySQL
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="epg_absmain"
            )
            
            cursor = conexion.cursor()
            
            # Consulta SQL con numeración en la primera columna
            consulta = """
            SELECT
                ROW_NUMBER() OVER (ORDER BY f.abrev) AS Numero,
                f.abrev AS Abreviatura,
                p.nombre AS NombrePrograma
            FROM
                dicprogramas AS p
            JOIN
                dicfacultades AS f
            ON
                f.id = p.idfacultad;"""
            
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            
            for resultado in resultados:
                self.treeview.insert("", "end", values=resultado)
            
            cursor.close()
            conexion.close()
        
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = GUI(ventana)
    ventana.mainloop()
