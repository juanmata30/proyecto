# ==========================================
# MENÚS DE NAVEGACIÓN DEL SISTEMA
# ==========================================
import requests 


from profesores import ModuloProfesores
from materias import ModuloMaterias
from creacion_de_horarios import ModuloControlEstudios
from modificacion_horarios import ModuloModificacionHorarios

def menu_horarios(sis_control, sis_modificacion):
    
    while True:
        print("\n" + "="*40)
        print("Horarios")
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
            # Aquí va un mini menú para agregar funciones de 
            # agregar o eliminar profesores manualmente. Por ahora, muestro la lista:
            print("\n--- Lista de Profesores ---")
            for p in sis_profes.profesores:
                print(f"- {p.Nombre} (C.I: {p.Cedula}) - Carga Máxima: {p.Max_Materias}")
            if not sis_profes.profesores:
                print("No hay profesores registrados.")
            
        elif opcion == "2":
            # Igual para las materias
            print("\n--- Lista de Materias ---")
            for m in sis_materias.materias:
                print(f"- [{m.Codigo}] {m.Nombre} - Secciones: {m.Secciones}")
            if not sis_materias.materias:
                print("No hay materias registradas.")
            
        elif opcion == "3":
            # Generamos el horario y pasamos automáticamente al menú final
            sis_control.generar_horarios()
            menu_horarios(sis_control, sis_modificacion)
            
        elif opcion == "4":
            print("Volviendo al menú de inicio...")
            break # Esto nos regresa al menú principal
        else:
            print("Opción inválida. Intente de nuevo.")
    pass
    

def menu_inicio():
    """El menú principal que pide el enunciado."""
    # 1. Instanciamos todas nuestras "oficinas" (Clases)
    sis_profes = ModuloProfesores()
    sis_materias = ModuloMaterias(sis_profes)
    sis_control = ModuloControlEstudios(sis_profes, sis_materias)
    sis_modificacion = ModuloModificacionHorarios(sis_control)

    while True:
        print("\n" + "="*40)
        print("SISTEMA DE CREACION DE HORARIOS")
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
            url_profes = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/profesores.json"
            url_materias = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-1.json"
            datos_p = requests.get("url_profes").json()
            sis_profes.cargar_datos_api(datos_p)
            print("Datos descargados correctamente (Simulación).")
            # Luego de descargar, vamos a los módulos fundamentales
            menu_fundamentales(sis_profes, sis_materias, sis_control, sis_modificacion)

        elif opcion == "3":
            # Cargamos el CSV y saltamos directo al resultado (Menú Control Estudios)
            archivo = input("\nIngrese el nombre del archivo (presione Enter para 'horarios.csv'): ")
            if not archivo:
                archivo = "horarios.csv"
                
            if sis_control.cargar_desde_csv(archivo):
                menu_horarios(sis_control, sis_modificacion)

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
