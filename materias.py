# módulo ligero para gestionar las materias del plan de estudios.
# permite cargar las asignaturas de la API, guardarlas en memoria
# y consultar, agregar, borrar o cambiar el número de secciones.


class Materia:
    # un objeto simple que guarda código, nombre y cuántas secciones hay
    def __init__(self, codigo, nombre, num_secciones):
        self.Codigo = codigo
        self.Nombre = nombre
        self.Secciones = num_secciones

    def __str__(self):
        return f"[{self.Codigo}] {self.Nombre} | Secciones a programar: {self.Secciones}"

class ModuloMaterias:
    def __init__(self, modulo_profesores):
        # Este módulo conoce a modulo_profesores por si necesita hacer validaciones cruzadas
        self.modulo_profesores = modulo_profesores
        self.materias = []

    def cargar_datos_api(self, datos_api):
        """Convierte los diccionarios de la API en objetos Materia.

        Las claves del JSON están en mayúsculas, así que usamos los nombres
        correctos y mostramos un resumen tras la carga.
        """
        self.materias = []
        for dato in datos_api:
            nueva_materia = Materia(
                dato.get('Código', 'SIN_CODIGO'), 
                dato.get('Nombre', 'Materia Desconocida'), 
                dato.get('Secciones', 1)
            )
            self.materias.append(nueva_materia)
        print(f" {len(self.materias)} materias cargadas desde la API.")

    def ver_lista(self):
        """Muestra todas las materias disponibles."""
        # simplemente recorre la lista y las imprime en modo amigable
        if not self.materias:
            print("No hay materias registradas.")
            return
        print("\n--- LISTA DE MATERIAS ---")
        for m in self.materias:
            print(f"- [{m.Codigo}] {m.Nombre} (Secciones: {m.Secciones})")

    def ver_materia(self, codigo):
        """Muestra los detalles de una materia en particular."""
        materia = self.buscar_materia(codigo)
        if materia:
            print("\n Materia encontrada:")
            print(materia)
        else:
            print(f" Materia con código {codigo} no encontrada.")

    def agregar_materia(self):
        """Agrega una materia pidiendo datos por teclado."""
        print("\n--- Agregar Nueva Materia ---")
        codigo = input("Código (Ej. BPTSP04): ")
        
        if self.buscar_materia(codigo):
            # no podemos duplicar códigos, así que avisamos y paramos
            print(" Error: Ya existe una materia con ese código.")
            return
            
        nombre = input("Nombre de la materia: ")
        try:
            secciones = int(input("Número de secciones a programar: "))
        except ValueError:
            # si el usuario escribe cualquier cosa, usamos 1 por seguridad
            print("Valor inválido. Se asignará 1 sección por defecto.")
            secciones = 1
            
        nueva_materia = Materia(codigo, nombre, secciones)
        self.materias.append(nueva_materia)
        print(f"Materia {nombre} agregada con éxito.")

    def eliminar_materia(self, codigo):
        """Elimina una materia del sistema."""
        materia = self.buscar_materia(codigo)
        if not materia:
            # si no existe, nada que hacer
            print(" Error: Materia no encontrada.")
            return
        self.materias.remove(materia)
        print(f"Éxito: Materia {materia.Nombre} eliminada.")

    def modificar_secciones(self, codigo):
        """Permite cambiar cuántas secciones se van a dar de una materia (Requisito PDF)."""
        # el usuario puede corregir la cantidad si se equivoca al crearla
        materia = self.buscar_materia(codigo)
        if not materia:
            print(" Error: Materia no encontrada.")
            return
        try:
            nuevas_secciones = int(input(f"Ingrese el nuevo número de secciones para {materia.Nombre} (Actual: {materia.Secciones}): "))
            materia.Secciones = nuevas_secciones
            print(f"Éxito: Secciones actualizadas a {nuevas_secciones}.")
        except ValueError:
            print(" Valor inválido. Debe ser un número entero.")

    def buscar_materia(self, codigo):
        """Herramienta interna para buscar materia por código."""
        for m in self.materias:
            if m.Codigo.upper() == codigo.upper():
                return m
        return None
