class Materia:
    def __init__(self, codigo, nombre, num_secciones):
        self.codigo = codigo
        self.nombre = nombre
        self.num_secciones = num_secciones

class ModuloMaterias:
    def __init__(self, modulo_profesores):
        self.modulo_profesores = modulo_profesores 
        self.materias = []

    def cargar_datos_api(self, datos_api):
        self.materias = []
        for dato in datos_api:
            nueva_materia = Materia(dato.get('codigo', ''), dato.get('nombre', ''), dato.get('num_secciones', 0))
            self.materias.append(nueva_materia)
            
# --- MÉTODOS AUXILIARES ---
    def _buscar_materia(self, codigo):
        for materia in self.materias:
            if materia.codigo == codigo:
                return materia
        return None

    # --- 1. Ver la lista de materias ---
    def ver_lista(self):
        if not self.materias:
            print("No hay materias registradas.")
            return
        print("\n--- LISTA DE MATERIAS ---")
        for materia in self.materias:
            print(materia)

    # --- 2. Ver detalles de una materia específica ---
    def ver_materia(self, codigo):
        materia = self._buscar_materia(codigo)
        if materia:
            print("\n--- DETALLES DE LA MATERIA ---")
            print(materia)
        else:
            print("Error: Materia no encontrada.")

    # --- 3. Ver profesores asociados a una materia ---
    def ver_profesores_asociados(self, codigo):
        materia = self._buscar_materia(codigo)
        if not materia:
            print("Error: Materia no encontrada.")
            return

        print(f"\n--- Profesores que dictan '{materia.nombre}' ---")
        encontrados = False
        
        # Aquí usamos el módulo de profesores para revisar sus listas
        for profe in self.modulo_profesores.profesores:
            if materia.nombre in profe.materias:
                print(f"- {profe.nombre} (Cédula: {profe.cedula})")
                encontrados = True
                
        if not encontrados:
            print("Ningún profesor tiene asignada esta materia actualmente.")

    # --- 4. Agregar una materia ---
    def agregar_materia(self, codigo, nombre, num_secciones):
        if self._buscar_materia(codigo):
            print("Error: Ya existe una materia con ese código.")
            return
        
        nueva_materia = Materia(codigo, nombre, num_secciones)
        self.materias.append(nueva_materia)
        print(f"Éxito: Materia '{nombre}' agregada localmente.")
        print("-> (Aquí iría el código para enviar la nueva materia a la API)")

    # --- 5. Eliminar una materia ---
    def eliminar_materia(self, codigo):
        materia = self._buscar_materia(codigo)
        if not materia:
            print("Error: Materia no encontrada.")
            return

        # Validar si al eliminarla, algún profesor se queda con 0 materias
        profes_en_peligro = []
        for profe in self.modulo_profesores.profesores:
            # Si el profe da la materia Y además es la única que da
            if materia.nombre in profe.materias and len(profe.materias) == 1:
                profes_en_peligro.append(profe.nombre)
        
        if len(profes_en_peligro) > 0:
            print(f"\n¡ADVERTENCIA! Al eliminar esta materia, los siguientes profesores quedarán SIN materias asignadas: {', '.join(profes_en_peligro)}")
            confirmacion = input("¿Estás seguro de que deseas eliminar la materia? (s/n): ")
            if confirmacion.lower() != 's':
                print("Operación cancelada.")
                return

        # Si confirmamos, la eliminamos de la lista de materias...
        self.materias.remove(materia)
        
        # ... ¡Y también debemos borrarla de las listas de los profesores!
        for profe in self.modulo_profesores.profesores:
            if materia.nombre in profe.materias:
                profe.materias.remove(materia.nombre)
                
        print(f"Éxito: Materia '{materia.nombre}' eliminada localmente del sistema y de los profesores.")
        print(f"-> (Aquí iría el código para borrar la materia {codigo} en la API)")

    # --- 6. Modificar número de secciones ---
    def modificar_secciones(self, codigo, nuevas_secciones):
        materia = self._buscar_materia(codigo)
        if not materia:
            print("Error: Materia no encontrada.")
            return

        # Validar si se fijará en cero
        if nuevas_secciones == 0:
            print(f"\n¡ADVERTENCIA! Vas a fijar las secciones en 0. Esto indicará que '{materia.nombre}' NO se ofertará en el trimestre actual.")
            confirmacion = input("¿Deseas continuar? (s/n): ")
            if confirmacion.lower() != 's':
                print("Operación cancelada.")
                return

        materia.num_secciones = nuevas_secciones
        print(f"Éxito: Las secciones de '{materia.nombre}' han sido actualizadas a {nuevas_secciones}.")
        print("-> (Aquí iría el código para actualizar las secciones en la API)")

# Importamos csv para guardar fácilmente el archivo al final
import csv

class SeccionAsignada:
    """Clase sencilla para guardar los datos de una sección ya programada."""
    def __init__(self, id_seccion, materia, profesor, bloque):
        self.id_seccion = id_seccion
        self.materia = materia
        self.profesor = profesor
        self.bloque = bloque

    def __str__(self):
        return f"[{self.bloque}] {self.id_seccion} ({self.materia.nombre}) - Prof. {self.profesor.nombre}"
