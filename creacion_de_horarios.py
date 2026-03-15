#archivo: creacion_de_horarios.py
"""""
este archivo es el que genera horarios automáticos.
combina listas de materias y profesores, observa los border cases bloqueos y salones,
y produce asignaciones. también ofrece vistas y exportación a CSV.
"""""
import csv     
from materias import Materia    

class SeccionAsignada:
    # objeto que guarda los datos de una sección ya colocada en el horario
    def __init__(self, id_seccion: str, materia: Materia, profesor, bloque: str):
        self.id_seccion = id_seccion
        self.materia = materia
        self.profesor = profesor
        self.bloque = bloque

class ModuloControlEstudios:
    def __init__(self, modulo_profesores, modulo_materias):
        self.mod_profes = modulo_profesores
        self.mod_materias = modulo_materias
        self.salones_disponibles = 0
        self.asignaciones: list[SeccionAsignada] = [] 
        self.horarios: list[str] = []
        dias = ["Lunes y Miércoles", "Martes y Jueves"]
        horas = ["7:00 - 8:30", "8:45 - 10:15", "10:30 - 12:00", 
                 "12:15 - 1:45", "2:00 - 3:30", "3:45 - 5:15", "5:30 - 7:00"]
        for dia in dias:
            for hora in horas:
                self.horarios.append(f"{dia} | {hora}")

    def generar_horarios(self):
        """Generador DE HORARIO."""
        print("\n" + "="*40)
        print("GENERANDO HORARIO...")
        print("="*40)
        
        # 0. si no hay datos en los módulos avisamos y abandonamos
        if not self.mod_profes.profesores:
            print("\nError: No hay profesores registrados. Cargue la lista antes de generar el horario.")
            return
        if not self.mod_materias.materias:
            print("\nError: No hay materias registradas. Cargue la lista antes de generar el horario.")
            return

        # 1. Solicitar salones al usuario (o 30 por defecto)
        entrada = input("Ingrese el número de salones disponibles por bloque (Coloque 30): ")
        try:
            self.salones_disponibles = int(entrada) if entrada.strip() != "" else 30
        except ValueError:
            self.salones_disponibles = 30
        self.asignaciones = []
        secciones_sin_horario = []   
        secciones_con_horario = []  
        cargas_profesores = {p.Cedula: 0 for p in self.mod_profes.profesores}
        horario_profesores = {p.Cedula: [] for p in self.mod_profes.profesores}
        uso_salones = {b: 0 for b in self.horarios}

        indice_bloque = 0
        total_bloques = len(self.horarios)

        # 2. Recorrer la lista de materias en orden
        for materia in self.mod_materias.materias:
            # Aseguramos que Secciones sea un número entero para el bucle
            num_secciones = int(getattr(materia, 'Secciones', 1))
            
            for num_sec in range(num_secciones):
                # cada sección tiene un identificador único
                id_seccion = f"{materia.Codigo}-Sec{num_sec + 1}"
                asignado = False
                intentos = 0
                
                # 3. Asignación Round-Robin
                while intentos < total_bloques and not asignado:
                    bloque_actual = self.horarios[indice_bloque]

                    if uso_salones[bloque_actual] < self.salones_disponibles:
                        # Buscar un profesor disponible
                        for p in self.mod_profes.profesores:
                            
                            #Buscamos si el Código (o el Nombre por si acaso) está en su lista de materias
                            if (materia.Codigo in p.Materias or materia.Nombre in p.Materias):
                                
                                if cargas_profesores[p.Cedula] < p.Max_Materias:
                                    # el profe no llegó a su tope de horas
                                    if bloque_actual not in horario_profesores[p.Cedula]:
                                        # no está ocupado en este bloque
                                        # Asignación exitosa
                                        nueva_seccion = SeccionAsignada(id_seccion, materia, p, bloque_actual)
                                        self.asignaciones.append(nueva_seccion)
                                        secciones_con_horario.append((id_seccion, p.nombre_completo))
                                        cargas_profesores[p.Cedula] += 1
                                        horario_profesores[p.Cedula].append(bloque_actual)
                                        uso_salones[bloque_actual] += 1
                                        asignado = True
                                        break

                    # Pasamos al siguiente bloque para la próxima sección/materia
                    indice_bloque = (indice_bloque + 1) % total_bloques
                    intentos += 1

                if not asignado:
                        secciones_sin_horario.append(id_seccion)
                        
        print(f"\nHorario generado. Se programaron {len(self.asignaciones)} secciones en total.")
        # muestra resumen por separado
        if secciones_con_horario:
            print("\nSecciones con horario asignado:")
            for sec, prof in secciones_con_horario:
                print(f" * {sec} (Prof. {prof})")
        if secciones_sin_horario:
            print("\nSecciones sin horario:")
            for sec in secciones_sin_horario:
                print(f" - {sec}")
        elif not secciones_con_horario:
            # no se programó nada
            print("\nNo se programó ninguna sección.")

    def ver_horario_materia(self, codigo):
        # busca cada asignación que tenga el código pedido y la muestra
        print(f"\n--- Horario de la materia [{codigo}] ---")
        encontrado = False
        for asig in self.asignaciones:
            if asig.materia.Codigo.upper() == codigo.upper():
                print(f"- {asig.id_seccion} | {asig.bloque} | Prof. {asig.profesor.nombre_completo}")
                encontrado = True
        if not encontrado:
            print("No hay secciones programadas para esta materia.")

    def ver_horario_profesor(self, cedula):
        # la consulta puede ser la cédula o el nombre completo del docente
        print(f"\n--- Horario del Profesor (C.I: {cedula}) ---")
        encontrado = False
        query = str(cedula).strip().lower()
        for asig in self.asignaciones:
            ced_profe = str(asig.profesor.Cedula).strip().lower()
            if ced_profe == query or str(asig.profesor.nombre_completo).strip().lower() == query:
                print(f"- {asig.materia.Nombre} ({asig.id_seccion}) | {asig.bloque}")
                encontrado = True
        if not encontrado:
            print("El profesor no tiene materias asignadas en este horario.")

    def ver_salones_hora(self, bloque):
        # muestra lo que hay en un único bloque: qué salones están ocupados
        print(f"\n--- Asignaciones en el bloque: {bloque} ---")
        count = 0
        for asig in self.asignaciones:
            if asig.bloque == bloque:
                print(f"Salón {count+1}: {asig.materia.Nombre} ({asig.id_seccion}) - Prof. {asig.profesor.nombre_completo}")
                count += 1
        if count == 0:
            print("No hay clases programadas en este bloque.")
        else:
            print(f"\nTotal salones ocupados: {count}/{self.salones_disponibles}")

    def guardar_csv(self, nombre_archivo="horarios.csv"):
        # exporta la lista de asignaciones a un archivo CSV simple
        try:
            with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['Id_Seccion', 'Materia', 'Profesor_CI', 'Bloque'])
                for asig in self.asignaciones:
                    escritor.writerow([asig.id_seccion, asig.materia.Codigo, asig.profesor.Cedula, asig.bloque])
            print(f"\nHorarios guardados exitosamente en {nombre_archivo}")
        except Exception as e:
            print(f"Error al guardar CSV: {e}")

    def cargar_desde_csv(self, nombre_archivo):
        # carga un horario ya generado desde un archivo, útil para seguir trabajando
        try:
            with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                self.asignaciones = []
                for fila in lector:
                    materia = self.mod_materias.buscar_materia(fila['Materia'])
                    profesor = self.mod_profes.buscar_profesor(fila['Profesor_CI'])
                    
                    if materia and profesor:
                        nueva_asig = SeccionAsignada(fila['Id_Seccion'], materia, profesor, fila['Bloque'])
                        self.asignaciones.append(nueva_asig)
            print(f"\nHorarios cargados exitosamente desde {nombre_archivo}")
            return True
        except FileNotFoundError:
            print(f"\nError: El archivo {nombre_archivo} no existe.")
            return False
        except Exception as e:
            print(f"\nError al cargar CSV: {e}")
            return False
