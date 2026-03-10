class Profesor:
    def __init__(self, nombre, cedula, correo, max_materias):
        self.nombre = nombre
        self.cedula = cedula
        self.correo = correo
        self.max_materias = max_materias
        self.materias = []

class ModuloProfesores:
    def __init__(self):
        self.profesores = []

    def cargar_datos_api(self, datos_api):
        self.profesores = []
        for dato in datos_api:
            # Recuerda ajustar las claves si tu JSON las llama diferente
            nuevo_profe = Profesor(dato.get('nombre', ''), dato.get('cedula', ''), dato.get('correo', ''), dato.get('max_materias', 1))
            if 'materias' in dato:
                nuevo_profe.materias = dato['materias']
            self.profesores.append(nuevo_profe)
            
    def _buscar_profesor(self, cedula):
        for profe in self.profesores:
            if profe.cedula == cedula:
                return profe
        return None
        
    # (Aquí van los demás métodos que hayas hecho para agregar, eliminar, ver profes, etc.)
    # --- MÉTODOS AUXILIARES ---
    def _buscar_profesor(self, cedula):
        for profe in self.profesores:
            if profe.cedula == cedula:
                return profe
        return None

    def _materia_quedara_vacia(self, materia, profe_a_ignorar):
        for profe in self.profesores:
            if profe != profe_a_ignorar and materia in profe.materias:
                return False 
        return True 

    # --- 1 y 2. Ver listas (Se mantienen iguales) ---
    def ver_lista(self):
        if not self.profesores:
            print("No hay profesores registrados.")
            return
        print("\n--- LISTA DE PROFESORES ---")
        for profe in self.profesores:
            print(profe)

    def ver_profesor(self, cedula):
        profe = self._buscar_profesor(cedula)
        if profe:
            print(profe)
        else:
            print("Error: Profesor no encontrado.")

    # --- 3. Agregar un profesor ---
    def agregar_profesor(self, nombre, cedula, correo, max_materias):
        if self._buscar_profesor(cedula):
            print("Error: Ya existe un profesor con esa cédula.")
            return
        
        nuevo_profe = Profesor(nombre, cedula, correo, max_materias)
        self.profesores.append(nuevo_profe)
        
        # NOTA PARA EL FUTURO:
        print(f"Éxito: Profesor '{nombre}' agregado localmente.")
        print("-> (Aquí iría el código para enviar el nuevo profesor a la API)")

    # --- 4. Eliminar un profesor ---
    def eliminar_profesor(self, cedula):
        profe = self._buscar_profesor(cedula)
        if not profe:
            return

        materias_en_peligro = []
        for materia in profe.materias:
            if self._materia_quedara_huerfana(materia, profe):
                materias_en_peligro.append(materia)
        
        if len(materias_en_peligro) > 0:
            print(f"\n¡ADVERTENCIA! Al eliminar este profesor, estas materias quedarán sin docentes: {', '.join(materias_en_peligro)}")
            confirmacion = input("¿Estás seguro de que deseas continuar? (s/n): ")
            if confirmacion.lower() != 's':
                print("Operación cancelada.")
                return

        self.profesores.remove(profe)
        print("Éxito: Profesor eliminado localmente.")
        print(f"-> (Aquí iría el código para borrar al profesor con cédula {cedula} en la API)")

    # --- 5. Modificar materias ---
    def agregar_materia_a_profesor(self, cedula, materia):
        profe = self._buscar_profesor(cedula)
        if not profe: return
        if len(profe.materias) >= profe.max_materias: return
        if materia in profe.materias: return

        profe.materias.append(materia)
        print(f"Éxito: '{materia}' agregada a {profe.nombre}.")
        print("-> (Aquí iría el código para actualizar la lista de materias en la API)")

    def quitar_materia_a_profesor(self, cedula, materia):
        profe = self._buscar_profesor(cedula)
        if not profe or materia not in profe.materias: return

        if self._materia_quedara_huerfana(materia, profe):
            print(f"\n¡ADVERTENCIA! Nadie más dicta '{materia}'.")
            if input("¿Quitar de todas formas? (s/n): ").lower() != 's': return

        profe.materias.remove(materia)
        print(f"Éxito: '{materia}' removida de {profe.nombre}.")
        print("-> (Aquí iría el código para actualizar la lista de materias en la API)")
