#archivo: profesores.py
"""""
este módulo se encarga de manejar los datos de los profesores
 y de mantener una lista que puede llenarse desde la API o manualmente.
 aquí también encontramos funciones para ver, agregar o eliminar
profesores y sus materias.
"""""

class Profesor:
    def __init__(self, nombre, apellido, cedula, correo, max_materias, materias=None):
        self.Nombre = nombre
        self.Apellido = apellido
        self.Cedula = cedula
        self.Correo = correo
        self.Max_Materias = max_materias
        self.Materias = materias if materias is not None else []

    @property
    def nombre_completo(self):
        return f"{self.Nombre} {self.Apellido}".strip()

    def __str__(self):
        return (f"Profesor: {self.nombre_completo} | C.I: {self.Cedula} | "
                f"Correo: {self.Correo} | Carga: {self.Max_Materias} | Materias: {self.Materias}")

class ModuloProfesores:
    def __init__(self):
        # empieza vacío, la lista se puede llenar desde la API o a mano
        self.profesores = []

    def cargar_datos_api(self, respuesta_profes):
        """Convierte los diccionarios descargados de Github en objetos Profesor.
        También imprime cuántos profesores se cargaron para que el usuario pueda
        verificar inmediatamente que la descarga tuvo efecto.
        """
        self.profesores = []
        for dato in respuesta_profes:
            materias_api = dato.get('materias', dato.get('Materias', []))
            nuevo_profe = Profesor(
                nombre = dato.get('nombre', dato.get('Nombre', 'Sin Nombre')), 
                apellido = dato.get('apellido', dato.get('Apellido', '')),
                cedula = dato.get('cedula', dato.get('Cedula', 'Sin Cédula')), 
                correo = dato.get('correo', dato.get('Email', 'Sin Correo')), 
                max_materias = dato.get('max_materias', dato.get('Max_Materias', dato.get('Max Carga', 1))),
                materias = materias_api
            )
            self.profesores.append(nuevo_profe)
            
        print(f" {len(self.profesores)} profesores cargados desde la API con sus respectivas materias.")

    def ver_lista(self):
        """Muestra a todos los profesores en pantalla."""
        if not self.profesores:
            print("No hay profesores registrados.")
            return
        print("\n--- LISTA DE PROFESORES ---")
        for profe in self.profesores:
            materias_txt = ", ".join(profe.Materias) if profe.Materias else "(sin materias asignadas)"
            print(f"- {profe.nombre_completo} (C.I: {profe.Cedula}) - Carga: {profe.Max_Materias} - Materias: {materias_txt}")

    def ver_profesor(self, cedula):
        """Busca y muestra el detalle de un solo profesor."""
        profe = self.buscar_profesor(cedula)
        if profe:
            print("\nProfesor encontrado:")
            print(profe)
        else:
            print(f"Error: Profesor con cédula {cedula} no encontrado.")

    def agregar_profesor(self):
        """Pide datos por teclado y agrega un profesor nuevo."""
        print("\n--- Agregar Nuevo Profesor ---")
        nombre = input("Nombre(s): ")
        apellido = input("Apellido(s): ")
        cedula = input("Cédula: ")
        
        if self.buscar_profesor(cedula):
            print("Error: Ya existe un profesor con esa cédula.")
            return
        correo = input("Correo electrónico: ")
        try:
            carga = int(input("Número máximo de materias: "))
        except ValueError:
            carga = 1
            
        materias_input = input("Ingrese las materias separadas por coma: ")
        lista_materias = [m.strip() for m in materias_input.split(",") if m.strip() != ""]
        
        nuevo_profe = Profesor(nombre, apellido, cedula, correo, carga, materias=lista_materias)
        self.profesores.append(nuevo_profe)
        print(f"Profesor {nombre} {apellido if 'apellido' in locals() else ''} agregado con éxito.")

    def eliminar_profesor(self, cedula):
        """Busca y elimina un profesor validando que no deje materias sin profesor."""
        profe = self.buscar_profesor(cedula)
        if not profe:
            print("Error: Profesor no encontrado.")
            return

        materias_en_peligro = []
        for materia in profe.Materias:
            if self.materia_quedara_huerfana(materia, profe):
                materias_en_peligro.append(materia)
        
        if len(materias_en_peligro) > 0:
            print(f"\n¡ADVERTENCIA! Al eliminar a este profesor, estas materias quedarán sin docentes: {', '.join(materias_en_peligro)}")
            confirmacion = input("¿Estás seguro de que deseas continuar? (s/n): ")
            if confirmacion.lower() != 's':
                print("Operación cancelada.")
                return

        self.profesores.remove(profe)
        print(f"Éxito: Profesor {profe.nombre_completo} eliminado.")

    def agregar_materia_a_profesor(self, cedula, codigo):
        """Le asigna una nueva materia a un profesor existente."""
        profe = self.buscar_profesor(cedula)
        if not profe: return print("Profesor no encontrado.")
        if len(profe.Materias) >= profe.Max_Materias: return print("El profesor alcanzó su carga máxima.")
        if codigo in profe.Materias: return print("El profesor ya tiene esa materia.")

        profe.Materias.append(codigo)
        print(f"Éxito: '{codigo}' agregada a {profe.Nombre}.")

    def quitar_materia_a_profesor(self, cedula, codigo):
        """Le quita una materia a un profesor."""
        profe = self.buscar_profesor(cedula)
        if not profe or codigo not in profe.Materias: return print("Profesor no encontrado o no dicta esa materia.")

        if self.materia_quedara_huerfana(codigo, profe):
            print(f"\n¡ADVERTENCIA! Nadie más dicta '{codigo}'.")
            if input("¿Quitar de todas formas? (s/n): ").lower() != 's': return

        profe.Materias.remove(codigo)
        print(f"Éxito: '{codigo}' removida de {profe.Nombre}.")

    def buscar_profesor(self, cedula):
        """Herramienta interna para encontrar el objeto Profesor dada su cédula."""
        query = str(cedula).strip().lower()
        for profe in self.profesores:
            ced_profe = str(profe.Cedula).strip().lower()
            nombre_profe = str(profe.nombre_completo).strip().lower()
            if ced_profe == query or nombre_profe == query:
                return profe
        return None

    def materia_quedara_huerfana(self, materia, profe_a_ignorar):
        """Verifica si al borrar a un profesor, la materia se queda sin nadie que la dicte."""
        for profe in self.profesores:
            if profe != profe_a_ignorar and materia in profe.Materias:
                return False 
        return True
