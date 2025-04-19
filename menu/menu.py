import os
from gestor.gestor_pacientes import GestorPacientes
from gestor.gestor_diagnosticos import GestorDiagnosticos
from gestor.gestor_imagenes import GestorImagenes


class MenuSistema:
    """
    Clase que implementa el menú del sistema de gestión de pacientes, diagnósticos e imágenes.
    """

    def __init__(self):
        """
        Inicializa las rutas de los archivos y las instancias de los gestores de pacientes, diagnósticos e imágenes.
        """
        self.db_pacientes_path = os.path.join("data", "db_pacientes.json")
        self.db_diagnosticos_path = os.path.join("data", "db_diagnostico.json")
        self.db_imagenes_path = os.path.join("data", "db_imagen.json")
        self.carpeta_imagenes = os.path.join("imagenes")

        # Inicialización de los gestores
        self.gestor_pacientes = GestorPacientes(self.db_pacientes_path)
        self.gestor_diagnosticos = GestorDiagnosticos(
            self.db_diagnosticos_path, self.db_pacientes_path
        )
        self.gestor_imagenes = GestorImagenes(
            self.db_imagenes_path, self.carpeta_imagenes,
            self.db_diagnosticos_path, self.db_pacientes_path
        )

    def menu_pacientes(self):
        """
        Muestra las opciones del menú de gestión de pacientes.
        """
        while True:
            print("\n--- MENÚ PACIENTES ---")
            print("1. Registrar paciente")
            print("2. Modificar paciente")
            print("3. Eliminar paciente")
            print("4. Listar pacientes")
            print("5. Volver al menú principal")

            # Captura de la opción seleccionada
            opcion = input("Seleccione una opción: ")

            # Acción según la opción seleccionada
            if opcion == "1":
                nombre = input("Nombre: ")
                edad = int(input("Edad: "))
                genero = input("Género (M/F/Otro): ")
                self.gestor_pacientes.registrar_paciente(nombre, edad, genero)

            elif opcion == "2":
                pid = input("ID del paciente: ")
                nombre = input("Nuevo nombre (Enter para no cambiar): ")
                edad = input("Nueva edad (Enter para no cambiar): ")
                genero = input("Nuevo género (Enter para no cambiar): ")
                self.gestor_pacientes.modificar_paciente(
                    pid,
                    nuevo_nombre=nombre if nombre else None,
                    nueva_edad=int(edad) if edad else None,
                    nuevo_genero=genero if genero else None
                )

            elif opcion == "3":
                pid = input("ID del paciente a eliminar: ")
                self.gestor_pacientes.eliminar_paciente(pid)

            elif opcion == "4":
                self.gestor_pacientes.listar_pacientes()

            elif opcion == "5":
                break
            else:
                print("Opción inválida.")

    def menu_diagnosticos(self):
        """
        Muestra las opciones del menú de gestión de diagnósticos.
        """
        while True:
            print("\n--- MENÚ DIAGNÓSTICOS ---")
            print("1. Registrar diagnóstico")
            print("2. Eliminar diagnóstico")
            print("3. Listar todos los diagnósticos")
            print("4. Listar por ID de paciente")
            print("5. Volver al menú principal")

            # Captura de la opción seleccionada
            opcion = input("Seleccione una opción: ")

            # Acción según la opción seleccionada
            if opcion == "1":
                id_paciente = input("ID del paciente: ")
                tipo = input("Tipo de ojo (OD = derecho / OS = izquierdo): ").upper()
                if tipo not in ("OD", "OS"):
                    print("Tipo inválido. Debe ser 'OD' o 'OS'.")
                    continue
                fecha = input("Fecha del diagnóstico (YYYY-MM-DD): ")
                d1 = float(input("Dioptría 1: "))
                d2 = float(input("Dioptría 2: "))
                astig = float(input("Astigmatismo: "))
                self.gestor_diagnosticos.registrar_diagnostico(id_paciente, fecha, d1, d2, astig, tipo)

            elif opcion == "2":
                id_diag = input("ID del diagnóstico a eliminar: ")
                self.gestor_diagnosticos.eliminar_diagnostico(id_diag)

            elif opcion == "3":
                self.gestor_diagnosticos.listar_diagnosticos()

            elif opcion == "4":
                pid = input("ID del paciente: ")
                self.gestor_diagnosticos.listar_diagnosticos(pid)

            elif opcion == "5":
                break
            else:
                print("Opción inválida.")

    def menu_imagenes(self):
        """
        Muestra las opciones del menú de gestión de imágenes de papilas.
        """
        while True:
            print("\n--- MENÚ IMÁGENES DE PAPILAS ---")
            print("1. Registrar imagen")
            print("2. Eliminar imagen")
            print("3. Listar todas las imágenes")
            print("4. Listar imágenes por diagnóstico")
            print("5. Volver al menú principal")

            # Captura de la opción seleccionada
            opcion = input("Seleccione una opción: ")

            # Acción según la opción seleccionada
            if opcion == "1":
                id_diag = input("ID del diagnóstico: ")
                tipo_ojo = input("Tipo de ojo (OD/OS): ").upper()
                while tipo_ojo not in ["OD", "OS"]:
                    print("Opción inválida. Debe ser 'OD' o 'OS'.")
                    tipo_ojo = input("Tipo de ojo (OD/OS): ").upper()
                fecha_captura = input("Fecha de captura (YYYY-MM-DD): ")
                ruta = input("Ruta completa de la imagen. Ej (C:\FundusImages\IMG2025.jpg) : ")
                desc = input("Descripción (opcional): ")
                self.gestor_imagenes.registrar_imagen(id_diag, ruta, desc, tipo_ojo, fecha_captura)

            elif opcion == "2":
                id_img = input("ID de la imagen a eliminar: ")
                self.gestor_imagenes.eliminar_imagen(id_img)

            elif opcion == "3":
                self.gestor_imagenes.listar_imagenes()

            elif opcion == "4":
                id_diag = input("ID del diagnóstico: ")
                self.gestor_imagenes.listar_imagenes(id_diag)

            elif opcion == "5":
                break
            else:
                print("Opción inválida.")

    def menu_principal(self):
        """
        Muestra las opciones del menú principal y maneja la selección de las subopciones.
        """
        while True:
            print("\n=== SISTEMA DE DIAGNÓSTICOS DE PAPILAS ===")
            print("1. Gestión de Pacientes")
            print("2. Gestión de Diagnósticos")
            print("3. Gestión de Imágenes")
            print("4. Salir")

            # Captura de la opción seleccionada
            opcion = input("Elige una opción: ")

            # Acción según la opción seleccionada
            if opcion == "1":
                self.menu_pacientes()
            elif opcion == "2":
                self.menu_diagnosticos()
            elif opcion == "3":
                self.menu_imagenes()
            elif opcion == "4":
                print("Saliendo del sistema...")
                break
