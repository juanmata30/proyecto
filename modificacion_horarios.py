class ModuloModificacionHorarios:
    def __init__(self, modulo_control_estudios):
        # Recibimos el control de estudios porque ahí están los horarios generados
        self.ce = modulo_control_estudios

    def iniciar_modificacion(self):
        print("\n" + "="*40)
        print("MÓDULO DE MODIFICACIÓN DE HORARIOS")
        print("="*40)

        # PASO 1: Seleccionar una materia
        cod_materia = input("1. Ingrese el código de la materia que desea modificar: ")
        
        # Buscamos todas las secciones asignadas a esa materia
        secciones_materia = []
        for sec in self.ce.asignaciones:
            if sec.materia.codigo == cod_materia:
                secciones_materia.append(sec)

        if len(secciones_materia) == 0:
            print("Error: No se encontraron secciones asignadas para esa materia.")
            return

        # PASO 2: Seleccionar una sección
        print("\n2. Secciones encontradas para esta materia:")
        for i in range(len(secciones_materia)):
            sec = secciones_materia[i]
            print(f"   [{i + 1}] ID: {sec.id_seccion} | Horario: {sec.bloque} | Prof: {sec.profesor.nombre}")
        
        try:
            opcion_sec = int(input("\nSeleccione el número de la sección a modificar: ")) - 1
            seccion_elegida = secciones_materia[opcion_sec]
        except (ValueError, IndexError):
            print("Error: Selección inválida.")
            return

        # PASO 3: Seleccionar la acción a realizar
        print(f"\nModificando la sección {seccion_elegida.id_seccion}...")
        print("a. Cambiar el profesor de esta sección")
        print("b. Cambiar el horario de esta sección")
        opcion_accion = input("Seleccione una opción (a/b): ").lower()

        if opcion_accion == 'a':
            self._cambiar_profesor_interactivo(seccion_elegida)
        elif opcion_accion == 'b':
            self._cambiar_horario_interactivo(seccion_elegida)
        else:
            print("Opción no válida. Volviendo al menú anterior...")

    # --- Lógica de la Opción A ---
    def _cambiar_profesor_interactivo(self, seccion):
        print(f"\nBuscando profesores disponibles para dar '{seccion.materia.nombre}' en el bloque [{seccion.bloque}]...")
        
        profes_disponibles = []
        for profe in self.ce.mod_profes.profesores:
            # Debe dar la materia
            if seccion.materia.nombre in profe.materias:
                # No mostramos al profesor que ya la está dando
                if profe.cedula != seccion.profesor.cedula:
                    # Validamos que tenga espacio en su carga y no esté ocupado a esa hora
                    if self.ce.cargas_profesores[profe.cedula] < profe.max_materias:
                        if not self.ce._profe_ocupado_en_bloque(profe.cedula, seccion.bloque):
                            profes_disponibles.append(profe)

        if not profes_disponibles:
            print("No hay otros profesores disponibles para esta materia a esta hora.")
            return

        # Mostramos los profesores disponibles
        for i in range(len(profes_disponibles)):
            p = profes_disponibles[i]
            print(f"  [{i + 1}] {p.nombre} (Cédula: {p.cedula}) - Carga actual: {self.ce.cargas_profesores[p.cedula]}/{p.max_materias}")

        try:
            op_profe = int(input("\nSeleccione el número del nuevo profesor: ")) - 1
            nuevo_profe = profes_disponibles[op_profe]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        # Aplicamos los cambios y actualizamos las cargas
        self.ce.cargas_profesores[seccion.profesor.cedula] -= 1 # Le quitamos la clase al viejo
        self.ce.cargas_profesores[nuevo_profe.cedula] += 1      # Se la sumamos al nuevo
        seccion.profesor = nuevo_profe                          # Asignamos al nuevo
        
        print(f"¡Éxito! El profesor de la sección {seccion.id_seccion} ha sido cambiado a {nuevo_profe.nombre}.")

    # --- Lógica de la Opción B ---
    def _cambiar_horario_interactivo(self, seccion):
        print("\nBuscando bloques horarios con salones disponibles...")
        
        bloques_disponibles = []
        for bloque in self.ce.horarios:
            if bloque != seccion.bloque:
                if self.ce._salones_usados_en_bloque(bloque) < self.ce.salones_disponibles:
                    bloques_disponibles.append(bloque)

        if not bloques_disponibles:
            print("No hay otros bloques con salones disponibles.")
            return

        # Mostramos los bloques
        for i in range(len(bloques_disponibles)):
            print(f"  [{i + 1}] {bloques_disponibles[i]}")

        try:
            op_bloque = int(input("\nSeleccione el número del nuevo horario: ")) - 1
            nuevo_bloque = bloques_disponibles[op_bloque]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        print(f"\nAhora seleccione un profesor para el nuevo horario [{nuevo_bloque}]:")
        
        # Ahora buscamos profes para ese NUEVO bloque
        profes_disponibles = []
        for profe in self.ce.mod_profes.profesores:
            if seccion.materia.nombre in profe.materias:
                # Si es el mismo profesor, verificamos si está libre a la nueva hora
                if profe.cedula == seccion.profesor.cedula:
                    if not self.ce._profe_ocupado_en_bloque(profe.cedula, nuevo_bloque):
                        profes_disponibles.append(profe)
                # Si es otro profesor, verificamos carga y disponibilidad a la nueva hora
                else:
                    if self.ce.cargas_profesores[profe.cedula] < profe.max_materias:
                        if not self.ce._profe_ocupado_en_bloque(profe.cedula, nuevo_bloque):
                            profes_disponibles.append(profe)

        if not profes_disponibles:
            print("Lamentablemente, ningún profesor de esta materia está libre en ese horario.")
            return

        for i in range(len(profes_disponibles)):
            p = profes_disponibles[i]
            print(f"  [{i + 1}] {p.nombre} (Cédula: {p.cedula})")

        try:
            op_profe = int(input("\nSeleccione el número del profesor: ")) - 1
            nuevo_profe = profes_disponibles[op_profe]
        except (ValueError, IndexError):
            print("Selección inválida.")
            return

        # Aplicamos los cambios
        if seccion.profesor.cedula != nuevo_profe.cedula:
            self.ce.cargas_profesores[seccion.profesor.cedula] -= 1
            self.ce.cargas_profesores[nuevo_profe.cedula] += 1
            
        seccion.bloque = nuevo_bloque
        seccion.profesor = nuevo_profe
        print(f"¡Éxito! Horario actualizado a {nuevo_bloque} con el profesor {nuevo_profe.nombre}.")
