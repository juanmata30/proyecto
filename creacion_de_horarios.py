import csv
from profesores import Profesor
from materias import Materia

class SeccionAsignada:
    def __init__(self, id_seccion, materia, profesor, bloque):
        self.id_seccion = id_seccion
        self.materia = materia
        self.profesor = profesor
        self.bloque = bloque

    def __str__(self):
        return f"[{self.bloque}] {self.id_seccion} ({self.materia.nombre}) - Prof. {self.profesor.nombre}"

class ModuloControlEstudios:
    def __init__(self, modulo_profesores, modulo_materias):
        self.mod_profes = modulo_profesores
        self.mod_materias = modulo_materias
        self.salones_disponibles = 0
        self.asignaciones = [] 
        self.cargas_profesores = {} 
        self.secciones_cerradas = {} 
        self.secciones_sin_salon = {} 
        
        self.horarios = []
        dias = ["Lunes y Miércoles", "Martes y Jueves"]
        horas = ["7:00 - 8:30", "8:45 - 10:15", "10:30 - 12:00", 
                 "12:15 - 1:45", "2:00 - 3:30", "3:45 - 5:15", "5:30 - 7:00"]
        for dia in dias:
            for hora in horas:
                self.horarios.append(f"{dia} | {hora}")

    # (AQUÍ PEGAS TODO EL RESTO DEL CÓDIGO DE ESTA CLASE: 
    # generar_horarios, _obtener_profesor, guardar_csv, cargar_desde_csv, etc.)

    def _salones_usados_en_bloque(self, bloque):
        """Cuenta cuántas secciones ya están asignadas a una hora específica."""
        contador = 0
        for sec in self.asignaciones:
            if sec.bloque == bloque:
                contador += 1
        return contador

    def _profe_ocupado_en_bloque(self, cedula, bloque):
        """Verifica si el profesor ya está dando otra clase a esa misma hora."""
        for sec in self.asignaciones:
            if sec.profesor.cedula == cedula and sec.bloque == bloque:
                return True
        return False

    def _obtener_profesor(self, materia_nombre, bloque_actual):
        """Intenta conseguir un profesor. Si todos están llenos, intenta reasignar."""
        
        # INTENTO 1: Buscar un profesor que dé la materia, tenga espacio y esté libre a esa hora
        for profe in self.mod_profes.profesores:
            if materia_nombre in profe.materias:
                if self.cargas_profesores[profe.cedula] < profe.max_materias:
                    if not self._profe_ocupado_en_bloque(profe.cedula, bloque_actual):
                        return profe # ¡Lo encontramos rápido!
                        
        # INTENTO 2: REASIGNACIÓN (Si llegamos aquí, los profes están a su límite)
        for profe in self.mod_profes.profesores:
            if materia_nombre in profe.materias and not self._profe_ocupado_en_bloque(profe.cedula, bloque_actual):
                # Este profesor podría darla, pero su carga está al máximo.
                # Vamos a ver si le podemos quitar una de sus secciones actuales a favor de OTRO profesor.
                for sec in self.asignaciones:
                    if sec.profesor.cedula == profe.cedula:
                        # Buscamos otro profe que pueda dar esta sección antigua (sec)
                        for otro_profe in self.mod_profes.profesores:
                            if otro_profe.cedula != profe.cedula and sec.materia.nombre in otro_profe.materias:
                                if self.cargas_profesores[otro_profe.cedula] < otro_profe.max_materias:
                                    if not self._profe_ocupado_en_bloque(otro_profe.cedula, sec.bloque):
                                        # ¡Bingo! Hacemos el trueque
                                        sec.profesor = otro_profe
                                        self.cargas_profesores[otro_profe.cedula] += 1
                                        self.cargas_profesores[profe.cedula] -= 1
                                        return profe # Ahora nuestro profe original tiene 1 espacio libre
        return None # No hubo manera

    # --- MÉTODO PRINCIPAL: GENERAR HORARIOS ---
    def generar_horarios(self):
        try:
            self.salones_disponibles = int(input("Ingrese el número de salones disponibles por bloque: "))
        except ValueError:
            print("Valor inválido. Se usarán 30 salones por defecto.")
            self.salones_disponibles = 30

        self.asignaciones = []
        self.secciones_cerradas = {}
        self.secciones_sin_salon = {}
        
        # Inicializamos las cargas de los profesores en 0
        for profe in self.mod_profes.profesores:
            self.cargas_profesores[profe.cedula] = 0

        indice_bloque = 0 # Usar este índice y avanzarlo evita que todas las secciones queden a la misma hora

        for materia in self.mod_materias.materias:
            if materia.num_secciones == 0:
                continue # Saltamos las que no se ofertan

            for i in range(materia.num_secciones):
                id_seccion = f"{materia.codigo}-{i+1}"
                asignado = False

                # Probaremos todos los bloques disponibles hasta encontrar uno que sirva
                for _ in range(len(self.horarios)):
                    bloque = self.horarios[indice_bloque]
                    
                    if self._salones_usados_en_bloque(bloque) < self.salones_disponibles:
                        profe = self._obtener_profesor(materia.nombre, bloque)
                        if profe:
                            nueva_seccion = SeccionAsignada(id_seccion, materia, profe, bloque)
                            self.asignaciones.append(nueva_seccion)
                            self.cargas_profesores[profe.cedula] += 1
                            asignado = True
                            
                            # Avanzamos el bloque para la próxima materia (distribución equitativa)
                            indice_bloque = (indice_bloque + 1) % len(self.horarios)
                            break
                    
                    # Si no sirvió este bloque, pasamos al siguiente
                    indice_bloque = (indice_bloque + 1) % len(self.horarios)

                # Si terminó el ciclo de 14 bloques y no se asignó, analizamos por qué falló
                if not asignado:
                    hay_al_menos_un_salon_global = any(self._salones_usados_en_bloque(b) < self.salones_disponibles for b in self.horarios)
                    if hay_al_menos_un_salon_global:
                        # Falló porque no hay profesor para las horas disponibles
                        self.secciones_cerradas[materia.nombre] = self.secciones_cerradas.get(materia.nombre, 0) + 1
                    else:
                        # Falló porque todo el edificio está lleno a toda hora
                        self.secciones_sin_salon[materia.nombre] = self.secciones_sin_salon.get(materia.nombre, 0) + 1

        self._reportar_resultados()

    # --- REPORTES Y OPCIONES ---
    def _reportar_resultados(self):
        print("\n" + "="*40)
        print("RESULTADOS DE LA ASIGNACIÓN AUTOMÁTICA")
        print("="*40)
        
        # 1. Materias cerradas por falta de profes
        if self.secciones_cerradas:
            print("\n❌ Secciones CERRADAS (Falta de Profesores):")
            for mat, cant in self.secciones_cerradas.items():
                print(f"  - {mat}: {cant} sección(es)")
        else:
            print("\n✅ Ninguna sección fue cerrada por falta de profesores.")

        # 2. Materias sin salón
        if self.secciones_sin_salon:
            print("\n🏢 Secciones NO ASIGNADAS (Falta de Salones):")
            for mat, cant in self.secciones_sin_salon.items():
                print(f"  - {mat}: {cant} sección(es)")
        else:
            print("\n✅ Todas las secciones consiguieron salón.")

        # 3. Salones disponibles por bloque
        print("\n🕒 Disponibilidad de salones restante por horario:")
        for bloque in self.horarios:
            usados = self._salones_usados_en_bloque(bloque)
            libres = self.salones_disponibles - usados
            print(f"  - {bloque}: {libres} salones libres")

    def ver_horario_materia(self, codigo_materia):
        print(f"\n--- HORARIO DE MATERIA: {codigo_materia} ---")
        encontrado = False
        for sec in self.asignaciones:
            if sec.materia.codigo == codigo_materia:
                print(sec)
                encontrado = True
        if not encontrado:
            print("No hay secciones asignadas para esta materia.")

    def ver_horario_profesor(self, cedula):
        print(f"\n--- HORARIO DE PROFESOR: {cedula} ---")
        encontrado = False
        for sec in self.asignaciones:
            if sec.profesor.cedula == cedula:
                print(sec)
                encontrado = True
        if not encontrado:
            print("Este profesor no tiene carga asignada.")

    def ver_salones_hora(self, bloque):
        print(f"\n--- CLASES EN EL BLOQUE: {bloque} ---")
        encontrado = False
        for sec in self.asignaciones:
            if sec.bloque == bloque:
                print(sec)
                encontrado = True
        if not encontrado:
            print("No hay clases programadas a esta hora.")

    def guardar_csv(self, nombre_archivo="horarios.csv"):
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["ID Seccion", "Materia", "Profesor (Cedula)", "Bloque Horario"])
            for sec in self.asignaciones:
                writer.writerow([sec.id_seccion, sec.materia.nombre, f"{sec.profesor.nombre} ({sec.profesor.cedula})", sec.bloque])
        print(f"\nÉxito: Horario exportado correctamente a '{nombre_archivo}'.")

    def modificar_asignacion(self, id_seccion, nueva_cedula_profe, nuevo_bloque):
        # Buscamos la sección
        seccion_objetivo = None
        for sec in self.asignaciones:
            if sec.id_seccion == id_seccion:
                seccion_objetivo = sec
                break
                
        if not seccion_objetivo:
            print("Error: No se encontró la sección.")
            return

        # Validamos al nuevo profesor
        nuevo_profe = self.mod_profes._buscar_profesor(nueva_cedula_profe)
        if not nuevo_profe or seccion_objetivo.materia.nombre not in nuevo_profe.materias:
            print("Error: Profesor no encontrado o no dicta esta materia.")
            return

        # Validamos que el nuevo bloque exista y tenga capacidad
        if nuevo_bloque not in self.horarios:
            print("Error: Bloque horario inválido.")
            return
            
        if self._salones_usados_en_bloque(nuevo_bloque) >= self.salones_disponibles and nuevo_bloque != seccion_objetivo.bloque:
             print("Error: No hay salones disponibles en ese bloque.")
             return

        if self._profe_ocupado_en_bloque(nuevo_profe.cedula, nuevo_bloque) and (nuevo_profe.cedula != seccion_objetivo.profesor.cedula or nuevo_bloque != seccion_objetivo.bloque):
            print("Error: El profesor ya tiene una clase asignada a esa hora.")
            return

        # Actualizamos la carga si cambiamos de profesor
        if seccion_objetivo.profesor.cedula != nuevo_profe.cedula:
            self.cargas_profesores[seccion_objetivo.profesor.cedula] -= 1
            self.cargas_profesores[nuevo_profe.cedula] += 1

        # Aplicamos los cambios
        seccion_objetivo.profesor = nuevo_profe
        seccion_objetivo.bloque = nuevo_bloque
        print(f"Éxito: Sección {id_seccion} modificada correctamente.")
    def cargar_desde_csv(self, nombre_archivo="horarios.csv"):
        """Lee el CSV y reconstruye las asignaciones de forma sencilla."""
        import csv
        self.asignaciones = []
        try:
            with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
                reader = csv.reader(archivo)
                next(reader) # Saltamos la primera línea (los encabezados)
                
                for fila in reader:
                    id_seccion, nombre_materia, datos_profe, bloque = fila
                    
                    # Como es una carga directa, creamos "objetos temporales" 
                    # básicos solo con los datos que necesitamos para mostrarlos.
                    materia_temp = Materia(id_seccion.split("-")[0], nombre_materia, 1)
                    
                    # Extraemos el nombre y la cédula del string "Nombre (Cedula)"
                    nombre_p = datos_profe.split(" (")[0]
                    cedula_p = datos_profe.split("(")[1].replace(")", "")
                    profe_temp = Profesor(nombre_p, cedula_p, "", 1)
                    
                    nueva_seccion = SeccionAsignada(id_seccion, materia_temp, profe_temp, bloque)
                    self.asignaciones.append(nueva_seccion)
                    
            print(f"Éxito: Horario cargado desde '{nombre_archivo}'.")
            return True
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
            return False
