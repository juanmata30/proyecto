# módulo sencillo que permite cambiar una asignación ya hecha.
# desde aquí puedes elegir una sección y modificar el profesor o el bloque
# cuando el horario ya está generado.


class ModuloModificacionHorarios:
    # este módulo recibe el control de estudios para poder tocar sus asignaciones
    def __init__(self, modulo_control_estudios):
        self.ce = modulo_control_estudios

    def iniciar_modificacion(self):
        """Menú para modificar una asignación existente."""
        # si todavía no se generó ningún horario, no hay nada que haga aquí
        if not self.ce.asignaciones:
            print(" No hay horarios generados para modificar.")
            return

        print("\n--- Modificación de Asignaciones ---")
        id_sec = input("Ingrese el ID de la sección a modificar (Ej. FPTSP22-Sec1): ")
        
        # Buscar la sección en la lista de asignaciones
        asignacion_actual = None
        for asig in self.ce.asignaciones:
            if asig.id_seccion == id_sec:
                asignacion_actual = asig
                break
                
        if not asignacion_actual:
            print(f"No se encontró ninguna asignación para {id_sec}.")
            return

        # mostramos los datos actuales para que el usuario sepa qué está cambiando
        print(f"\nSección encontrada:")
        print(f"Materia: {asignacion_actual.materia.Nombre}")
        print(f"Profesor Actual: {asignacion_actual.profesor.Nombre}")
        print(f"Bloque Actual: {asignacion_actual.bloque}")

        print("\n¿Qué desea modificar?")
        print("1. Cambiar Profesor")
        print("2. Cambiar Bloque Horario")
        print("3. Cancelar")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self._cambiar_profesor(asignacion_actual)
        elif opcion == "2":
            self._cambiar_bloque(asignacion_actual)
        else:
            # cualquier otra entrada se considera cancelar
            print("Modificación cancelada.")

    def _cambiar_profesor(self, asignacion):
        nueva_cedula = input("Ingrese la cédula del nuevo profesor: ")
        nuevo_profe = self.ce.mod_profes.buscar_profesor(nueva_cedula)
        
        if not nuevo_profe:
            print("Error: Profesor no encontrado en el sistema.")
            return
            
        # verificamos que el profe realmente pueda dar la materia
        if asignacion.materia.Nombre not in nuevo_profe.Materias:
            print(f"Error: {nuevo_profe.Nombre} no está habilitado para dar esta materia.")
            return

        # Aplicamos el cambio
        asignacion.profesor = nuevo_profe
        print(f"Éxito: Profesor actualizado a {nuevo_profe.Nombre}.")

    def _cambiar_bloque(self, asignacion):
        print("\nBloques Disponibles:")
        for i in range(len(self.ce.horarios)):
            print(f"{i+1}. {self.ce.horarios[i]}")
            
        try:
            opcion = int(input("\nSeleccione el número del nuevo bloque: ")) - 1
            if 0 <= opcion < len(self.ce.horarios):
                nuevo_bloque = self.ce.horarios[opcion]
                asignacion.bloque = nuevo_bloque
                print(f"Éxito: Bloque actualizado a {nuevo_bloque}.")
            else:
                print("Opción fuera de rango.")
        except ValueError:
            print("Debe ingresar un número válido.")
