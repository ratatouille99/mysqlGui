import mysql.connector
from mysql.connector import Error

class Comunicar():
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "epg_absmain"   
        )
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor()    
        
        except Error as e:
            print("Ha ocurrido un error durante la ejecucion \n", e)
    
    def estructura_tabla(self, tabla):
        query = f"DESCRIBE {tabla}"
        self.cursor.execute(query)
        
        return self.cursor.fetchall()
    
    def insertar(self, tabla, datos):
        campos = ', '.join(datos.keys())
        valores = ', '.join(['%s'] * len(datos))
        query = f"INSERT INTO {tabla} ({campos}) VALUES ({valores})"
        self.cursor.execute(query, list(datos.values()))
        self.conexion.commit()
        print("Registro insertado correctamente.")
    
    def mostrar_datos(self, tabla):
        try:
            query = f"SELECT * FROM {tabla}"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al consultar datos desde la base de datos: {str(e)}")
            return None  # Devuelve None en caso de error

    
    def eliminar(self, tabla, clave_primaria, valor_clave):
        try:
            query = f"DELETE FROM {tabla} WHERE {clave_primaria} = %s"
            self.cursor.execute(query, (valor_clave,))
            self.conexion.commit()
            print("Registro eliminado correctamente.")
        except Error as e:
            print("Error al eliminar el registro:", e)

