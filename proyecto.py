# CÓDIGO PRINCIPAL -- archivo: proyecto.py
"""""
este es el script principal, el que arranca el sistema.
 define los menús que el usuario ve, coordina los módulos de
 profesores, materias, creación y modificación de horarios.
 la def de menu_inicio() al final para poner todo en marcha.
"""""

import requests

from profesores import ModuloProfesores, Profesor
from materias import ModuloMaterias, Materia
from creacion_de_horarios import ModuloControlEstudios
from modificacion_horarios import ModuloModificacionHorarios

def menu_horarios(sis_control, sis_modificacion):
    # este menu aparece cuando ya se genero o se cargo un horario
    # y el usuario quiere consultarlo o guardarlo en archivo
    while True:
        print("\n" + "="*40)
        print("MÓDULO DE CONTROL DE ESTUDIOS")
        print("="*40)
        print("1. Ver el horario de una materia")
        print("2. Ver el horario de un profesor")
        print("3. Ver salones asignados a una hora")
        print("4. Guardar asignación de horarios en CSV")
        print("5. Modificar asignación de horarios")
        print("6. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cod = input("Ingrese el código de la materia (Ej. FPTSP22): ")
            sis_control.ver_horario_materia(cod)
            
        elif opcion == "2":
            ced = input("Ingrese la cédula del profesor: ")
            sis_control.ver_horario_profesor(ced)
            
        elif opcion == "3":
            print("\nBloques disponibles:")
            for i in range(len(sis_control.horarios)):
                print(f"  - {sis_control.horarios[i]}")
            bloque = input("\nEscriba el bloque exacto (Ej. Lunes y Miércoles 7:00 - 8:30): ")
            sis_control.ver_salones_hora(bloque)
            
        elif opcion == "4":
            sis_control.guardar_csv()
            
        elif opcion == "5":
            sis_modificacion.iniciar_modificacion()
            
        elif opcion == "6":
            print("Saliendo de la generacion de horarios...")
            break 
        else:
            print("Opción inválida.")


def menu_fundamentales(sis_profes, sis_materias, sis_control, sis_modificacion):
    # advertencia inicial si el usuario accede sin datos cargados
    if not sis_profes.profesores and not sis_materias.materias:
        print("\nNo hay datos de profesores ni materias. Use la opción 2 del menú inicial para descargar de la API.")
    elif not sis_profes.profesores:
        print("\n No hay profesores registrados. Descargue los datos de la API (opción 2 en el inicio).")
    elif not sis_materias.materias:
        print("\nNo hay materias registradas. Descargue los datos de la API (opción 2 en el inicio).")

    while True:
        print("\n" + "="*40)
        print("MÓDULOS FUNDAMENTALES")
        print("="*40)
        print("1. Gestionar Profesores")
        print("2. Gestionar Materias")
        print("3. Generar Horarios (Pasar a Creacion de Horarios)")
        print("4. Volver al inicio")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # MINI-MENÚ PROFESORES 

            while True:
                print("\n" + "-"*30)
                print("GESTIÓN DE PROFESORES")
                print("-"*30)
                print("1. Ver lista de todos los profesores")
                print("2. Ver un profesor en específico")
                print("3. Agregar un nuevo profesor")
                print("4. Eliminar un profesor")
                print("5. Agregar materias a un profesor")
                print("6. Eliminar materias a un profesor")
                print("7. Volver a Módulos Fundamentales")
                
                sub_op = input("Seleccione una opción: ")
                
                if sub_op == "1": sis_profes.ver_lista() 
                elif sub_op == "2": 
                    cedula = input("\nIngrese la cédula a buscar: ")
                    sis_profes.ver_profesor(cedula)
                elif sub_op == "3": sis_profes.agregar_profesor()
                elif sub_op == "4": 
                    cedula = input("\nIngrese la cédula a eliminar: ")
                    sis_profes.eliminar_profesor(cedula)
                elif sub_op == "5":
                    cedula = input("Cedula del profesor: ")
                    codigo = input("Codigo de la materia a agregar: ")
                    sis_profes.agregar_materia_a_profesor(cedula, codigo)
                elif sub_op == "6":
                    cedula = input("Cedula del profesor: ")
                    codigo = input("Codigo de la materia a eliminar: ")
                    sis_profes.quitar_materia_a_profesor(cedula, codigo)
                elif sub_op == "7": break
                else: print("Opción inválida.")
            
        elif opcion == "2":
            # MINI-MENÚ MATERIAS
            
            while True:
                print("\n" + "-"*30)
                print("GESTIÓN DE MATERIAS")
                print("-"*30)
                print("1. Ver lista de todas las materias")
                print("2. Ver una materia en específico")
                print("3. Agregar una nueva materia")
                print("4. Eliminar una materia")
                print("5. Modificar número de secciones")
                print("6. Volver a Módulos Fundamentales")
                
                sub_op = input("Seleccione una opción: ")
                
                if sub_op == "1": sis_materias.ver_lista()
                elif sub_op == "2":
                    codigo = input("\nIngrese el código de la materia (Ej. BPTSP04): ")
                    sis_materias.ver_materia(codigo)
                elif sub_op == "3": sis_materias.agregar_materia()
                elif sub_op == "4":
                    codigo = input("\nIngrese el código de la materia a eliminar: ")
                    sis_materias.eliminar_materia(codigo)
                elif sub_op == "5":
                    codigo = input("\nIngrese el código de la materia a modificar: ")
                    sis_materias.modificar_secciones(codigo)
                elif sub_op == "6": break
                else: print("Opción inválida.")
            
        elif opcion == "3":
            sis_control.generar_horarios()
            menu_horarios(sis_control, sis_modificacion)
            
        elif opcion == "4":
            print("Volviendo al menú de inicio...")
            break 
        else:
            print("Opción inválida.")

def menu_inicio():
    """El menú principal."""
    sis_profes = ModuloProfesores()
    sis_materias = ModuloMaterias(sis_profes)
    sis_control = ModuloControlEstudios(sis_profes, sis_materias)
    sis_modificacion = ModuloModificacionHorarios(sis_control)

    while True:
        # el bucle central del programa; se repite hasta que el usuario elige salir
        print("\n" + "="*40)
        print("SISTEMA DE GESTIÓN DE HORARIOS")
        print("="*40)
        print("1. Crear Horarios en blanco (borra datos existentes)")
        print("2. Descargar datos de la API de Github")
        print("3. Cargar un horario en CSV")
        print("4. Salir del programa")
        
        opcion = input("Seleccione una opción de inicio: ")

        if opcion == "1":
            sis_profes.profesores = []
            sis_materias.materias = []
            print("\nListas inicializadas en blanco.")
            menu_fundamentales(sis_profes, sis_materias, sis_control, sis_modificacion)

        elif opcion == "2":
            print("\nDescargando datos de la API de Github...")
            try:
                url_profesores = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/profesores.json"
                url_materias = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-2.json" 
                
                respuesta_profes = requests.get(url_profesores)
                respuesta_materias = requests.get(url_materias)
                
                if respuesta_profes.status_code == 200 and respuesta_materias.status_code == 200:
                    sis_profes.cargar_datos_api(respuesta_profes.json())
                    sis_materias.cargar_datos_api(respuesta_materias.json())
                    print("¡Datos descargados y procesados correctamente!")
                    menu_fundamentales(sis_profes, sis_materias, sis_control, sis_modificacion)
                else:
                    print("Error de servidor al descargar de Github.")
            except Exception as e:
                print(f"Error de conexión: {e}")

        elif opcion == "3":
            archivo = input("\nIngrese el nombre del archivo (presione Enter para 'horarios.csv'): ")
            if not archivo: archivo = "horarios.csv"
            if sis_control.cargar_desde_csv(archivo):
                menu_horarios(sis_control, sis_modificacion)

        elif opcion == "4":
            print("\n¡Gracias por usar el sistema! Hasta luego.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_inicio()
