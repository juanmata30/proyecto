"""MODULOS PRINCIPALES"""

import csv
import json

class Profesor:
    def __init__(self, nombre, cedula, correo, max_materias):
        self.nombre = nombre
        self.cedula = cedula
        self.correo = correo
        self.max_materias = max_materias
        self.materias = [] 

    def __str__(self):
        materias_str = ", ".join(self.materias) if self.materias else "Ninguna"
        return f"Cédula: {self.cedula} | Nombre: {self.nombre} | Correo: {self.correo} | Materias: {materias_str}"


class ModuloProfesores:
    def __init__(self):
        self.profesores = [] 

    # --- NUEVO MÉTODO: CARGAR DATOS ---
    def cargar_datos_api(self, datos_api):
        """
        Recibe una lista de diccionarios (como los que llegarían de la API) 
        y los convierte en objetos Profesor.
        """
        self.profesores = [] # Limpiamos la lista por si ya tenía datos
        for dato in datos_api:
            # Creamos el objeto con los datos básicos
            nuevo_profe = Profesor(dato['nombre'], dato['cedula'], dato['correo'], dato['max_materias'])
            
            # Si la API nos envió materias ya asignadas, las agregamos
            if 'materias' in dato:
                nuevo_profe.materias = dato['materias']
                
            self.profesores.append(nuevo_profe)
            
        print(f"Sistema: Se cargaron {len(self.profesores)} profesores desde la base de datos (API).")

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

class Materia:
    def __init__(self, codigo, nombre, num_secciones):
        self.codigo = codigo
        self.nombre = nombre
        self.num_secciones = num_secciones

    def __str__(self):
        estado = "No se oferta este trimestre" if self.num_secciones == 0 else f"{self.num_secciones} secciones"
        return f"Código: {self.codigo} | Nombre: {self.nombre} | Estado: {estado}"


class ModuloMaterias:
    # Fíjate que al iniciar, le pasamos el módulo de profesores para que puedan interactuar
    def __init__(self, modulo_profesores):
        self.materias = []
        self.modulo_profesores = modulo_profesores 

    # --- MÉTODO PARA CARGAR DATOS DE LA API ---
    def cargar_datos_api(self, datos_api):
        self.materias = [] 
        for dato in datos_api:
            nueva_materia = Materia(dato['codigo'], dato['nombre'], dato['num_secciones'])
            self.materias.append(nueva_materia)
        print(f"Sistema: Se cargaron {len(self.materias)} materias desde la base de datos (API).")

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


class ModuloControlEstudios:
    def __init__(self, modulo_profesores, modulo_materias):
        # Recibimos los módulos anteriores para poder leer sus datos
        self.mod_profes = modulo_profesores
        self.mod_materias = modulo_materias
        
        self.salones_disponibles = 0
        self.asignaciones = [] # Aquí guardaremos los objetos SeccionAsignada
        self.cargas_profesores = {} # Diccionario: {cedula: cantidad_de_secciones_asignadas}
        
        # Reportes de errores
        self.secciones_cerradas = {} # Por falta de profesores
        self.secciones_sin_salon = {} # Por falta de espacio
        
        # Generamos la lista de los 14 bloques horarios de la imagen
        self.horarios = []
        dias = ["Lunes y Miércoles", "Martes y Jueves"]
        horas = ["7:00 - 8:30", "8:45 - 10:15", "10:30 - 12:00", 
                 "12:15 - 1:45", "2:00 - 3:30", "3:45 - 5:15", "5:30 - 7:00"]
        for dia in dias:
            for hora in horas:
                self.horarios.append(f"{dia} | {hora}")

    # --- MÉTODOS AUXILIARES LÓGICOS ---
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

# ==========================================
# MENÚS DE NAVEGACIÓN DEL SISTEMA
# ==========================================

def menu_control_estudios(sis_control, sis_modificacion):
    """Submenú de la fase final: Ver y modificar horarios."""
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