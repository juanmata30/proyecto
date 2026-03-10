# ==========================================
# MENÚS DE NAVEGACIÓN DEL SISTEMA
# ==========================================


from profesores import ModuloProfesores
from materias import ModuloMaterias
from creacion_de_horarios import ModuloControlEstudios
from modificacion_horarios import ModuloModificacionHorarios

def menu_control_estudios(sis_control, sis_modificacion):
    # (Pega aquí el código del submenú de control de estudios que hicimos antes)
    while True:
        print("\n" + "="*40)
        print("RESULTADOS Y CONTROL DE ESTUDIOS")
        print("="*40)
        print("1. Ver el horario de una materia")
        print("2. Ver el horario de un profesor")
        print("3. Ver salones asignados a una hora")
        print("4. Guardar asignación de horarios en CSV")
        print("5. Modificar asignación de horarios")
        print("6. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cod = input("Ingrese el código de la materia (Ej. MAT101): ")
            sis_control.ver_horario_materia(cod)
            
        elif opcion == "2":
            ced = input("Ingrese la cédula del profesor: ")
            sis_control.ver_horario_profesor(ced)
            
        elif opcion == "3":
            print("\nBloques disponibles:")
            # Mostramos los bloques para que el usuario sepa qué escribir
            for i in range(len(sis_control.horarios)):
                print(f"  - {sis_control.horarios[i]}")
            bloque = input("\nEscriba el bloque exacto que desea consultar: ")
            sis_control.ver_salones_hora(bloque)
            
        elif opcion == "4":
            sis_control.guardar_csv()
            
        elif opcion == "5":
            # Llamamos al módulo de modificación que creamos
            sis_modificacion.iniciar_modificacion()
            
        elif opcion == "6":
            print("Saliendo del control de estudios...")
            break # Sale de este submenú
        else:
            print("Opción inválida. Intente de nuevo.")
    
    pass

def menu_fundamentales(sis_profes, sis_materias, sis_control, sis_modificacion):
    # (Pega aquí el código del submenú de módulos fundamentales)

    while True:
        print("\n" + "="*40)
        print("MÓDULOS FUNDAMENTALES")
        print("="*40)
        print("1. Gestionar Profesores (Ver, agregar, eliminar)")
        print("2. Gestionar Materias (Ver, agregar, eliminar)")
        print("3. Generar Horarios (Pasar a Control de Estudios)")
        print("4. Volver al inicio")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Aquí podrías poner un mini-menú si luego quieres agregar funciones de 
            # agregar o eliminar profesores manualmente. Por ahora, podemos mostrar la lista:
            print("\n--- Lista de Profesores ---")
            for p in sis_profes.profesores:
                print(f"- {p.nombre} (C.I: {p.cedula}) - Carga Máxima: {p.max_materias}")
            if not sis_profes.profesores:
                print("No hay profesores registrados.")
            
        elif opcion == "2":
            # Igual para las materias
            print("\n--- Lista de Materias ---")
            for m in sis_materias.materias:
                print(f"- [{m.codigo}] {m.nombre} - Secciones: {m.num_secciones}")
            if not sis_materias.materias:
                print("No hay materias registradas.")
            
        elif opcion == "3":
            # Generamos el horario y pasamos automáticamente al menú final
            sis_control.generar_horarios()
            menu_control_estudios(sis_control, sis_modificacion)
            
        elif opcion == "4":
            print("Volviendo al menú de inicio...")
            break # Esto nos regresa al menú principal
        else:
            print("Opción inválida. Intente de nuevo.")
    pass
    while True:
        print("\n" + "="*40)
        print("RESULTADOS Y CONTROL DE ESTUDIOS")
        print("="*40)
        print("1. Ver el horario de una materia")
        print("2. Ver el horario de un profesor")
        print("3. Ver salones asignados a una hora")
        print("4. Guardar asignación de horarios en CSV")
        print("5. Modificar asignación de horarios")
        print("6. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cod = input("Ingrese el código de la materia: ")
            sis_control.ver_horario_materia(cod)
        elif opcion == "2":
            ced = input("Ingrese la cédula del profesor: ")
            sis_control.ver_horario_profesor(ced)
        elif opcion == "3":
            bloque = input("Ingrese el bloque (ej. Lunes y Miércoles | 7:00 - 8:30): ")
            sis_control.ver_salones_hora(bloque)
        elif opcion == "4":
            sis_control.guardar_csv()
        elif opcion == "5":
            sis_modificacion.iniciar_modificacion()
        elif opcion == "6":
            break # Sale de este submenú
        else:
            print("Opción inválida.")


def menu_fundamentales(sis_profes, sis_materias, sis_control, sis_modificacion):
    """Submenú para gestionar Profesores, Materias y generar el horario."""
    while True:
        print("\n" + "="*40)
        print("MÓDULOS FUNDAMENTALES")
        print("="*40)
        print("1. Gestionar Profesores (Módulo Profesores)")
        print("2. Gestionar Materias (Módulo Materias)")
        print("3. Generar Horarios (Pasar a Control de Estudios)")
        print("4. Volver al inicio")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n(Aquí puedes llamar a las funciones del sis_profes: ver_lista, agregar, eliminar...)")
            # Ejemplo: sis_profes.ver_lista()
            
        elif opcion == "2":
            print("\n(Aquí puedes llamar a las funciones del sis_materias: ver_lista, agregar, eliminar...)")
            # Ejemplo: sis_materias.ver_lista()
            
        elif opcion == "3":
            # Generamos el horario y pasamos automáticamente al siguiente menú
            sis_control.generar_horarios()
            menu_control_estudios(sis_control, sis_modificacion)
            
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")


def menu_inicio():
    """El menú principal que pide el enunciado."""
    # 1. Instanciamos todas nuestras "oficinas" (Clases)
    sis_profes = ModuloProfesores()
    sis_materias = ModuloMaterias(sis_profes)
    sis_control = ModuloControlEstudios(sis_profes, sis_materias)
    sis_modificacion = ModuloModificacionHorarios(sis_control)

    while True:
        print("\n" + "="*40)
        print("SISTEMA DE GESTIÓN UNIVERSITARIA")
        print("="*40)
        print("1. Crear listas en blanco")
        print("2. Descargar los datos de la API de Github")
        print("3. Cargar un horario en CSV")
        print("4. Salir del programa")
        
        opcion = input("Seleccione una opción de inicio: ")

        if opcion == "1":
            # Listas en blanco. Limpiamos por si acaso y vamos a los módulos.
            sis_profes.profesores = []
            sis_materias.materias = []
            print("\nListas inicializadas en blanco.")
            menu_fundamentales(sis_profes, sis_materias, sis_control, sis_modificacion)

        elif opcion == "2":
            print("\nConectando con la API de Github...")
            # -> AQUÍ VA TU CÓDIGO DE REQUESTS A LA API <-
            url_profesores = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/profesores.json"
            url_materias = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-1.json"
            # datos_p = requests.get("url_profes").json()
            # sis_profes.cargar_datos_api(datos_p)
            print("Datos descargados correctamente (Simulación).")
            # Luego de descargar, vamos a los módulos fundamentales
            menu_fundamentales(sis_profes, sis_materias, sis_control, sis_modificacion)

        elif opcion == "3":
            # Cargamos el CSV y saltamos directo al resultado (Menú Control Estudios)
            archivo = input("\nIngrese el nombre del archivo (presione Enter para 'horarios.csv'): ")
            if not archivo:
                archivo = "horarios.csv"
                
            if sis_control.cargar_desde_csv(archivo):
                menu_control_estudios(sis_control, sis_modificacion)

        elif opcion == "4":
            print("\n¡Gracias por usar el sistema! Hasta luego.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

# ==========================================
# PUNTO DE ARRANQUE DEL SCRIPT
# ==========================================
if __name__ == "__main__":
    menu_inicio() 