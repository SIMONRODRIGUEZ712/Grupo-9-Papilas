import json
import os
from modelos.paciente import Paciente


class GestorPacientes:
    """
    Clase encargada de gestionar los datos de pacientes, permitiendo
    registrar, modificar, eliminar, listar y persistir la información
    en archivos JSON.
    """

    def __init__(self, ruta_db: str):
        """
        Inicializa el gestor de pacientes.

        Args:
            ruta_db (str): Ruta al archivo JSON de la base de datos de pacientes.
        """
        self.ruta_db = ruta_db
        self.db = self._cargar_db()
        self.ultimo_id = self._obtener_ultimo_id()

    def _cargar_db(self):
        """
        Carga la base de datos de pacientes desde el archivo JSON.

        Returns:
            dict: Diccionario con los datos cargados o vacío si no existe o hay error.
        """
        if not os.path.exists(self.ruta_db):
            return {}
        with open(self.ruta_db, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def _guardar_db(self):
        """
        Guarda la base de datos de pacientes en el archivo JSON.
        """
        with open(self.ruta_db, "w", encoding="utf-8") as f:
            json.dump(self.db, f, indent=4)

    def _obtener_ultimo_id(self):
        """
        Obtiene el último ID numérico usado para generar nuevos pacientes.

        Returns:
            int: Último ID usado, 0 si no hay pacientes.
        """
        if not self.db:
            return 0
        return max(int(pid) for pid in self.db.keys())

    def _generar_id(self):
        """
        Genera un nuevo ID de paciente con formato de tres dígitos.

        Returns:
            str: ID generado (ej. "001").
        """
        self.ultimo_id += 1
        return str(self.ultimo_id).zfill(3)

    def registrar_paciente(self, nombre: str, edad: int, genero: str):
        """
        Registra un nuevo paciente en la base de datos.

        Args:
            nombre (str): Nombre del paciente.
            edad (int): Edad del paciente.
            genero (str): Género del paciente.
        """
        nuevo_id = self._generar_id()
        paciente = Paciente(id_=nuevo_id, nombre=nombre, edad=edad, genero=genero)
        self.db[nuevo_id] = paciente.to_dict()
        self._guardar_db()
        print(f"✅ Paciente registrado con ID {nuevo_id}")

    def modificar_paciente(self, id_paciente: str, nuevo_nombre=None, nueva_edad=None, nuevo_genero=None):
        """
        Modifica los datos de un paciente existente.

        Args:
            id_paciente (str): ID del paciente a modificar.
            nuevo_nombre (str, opcional): Nuevo nombre (si aplica).
            nueva_edad (int, opcional): Nueva edad (si aplica).
            nuevo_genero (str, opcional): Nuevo género (si aplica).
        """
        if id_paciente not in self.db:
            print("❌ El paciente no existe.")
            return

        paciente = Paciente.from_dict(self.db[id_paciente])

        if nuevo_nombre:
            paciente.nombre = nuevo_nombre
        if nueva_edad is not None:
            paciente.edad = nueva_edad
        if nuevo_genero:
            paciente.genero = nuevo_genero

        self.db[id_paciente] = paciente.to_dict()
        self._guardar_db()
        print(f"✅ Paciente {id_paciente} modificado.")

    def eliminar_paciente(self, id_paciente: str):
        """
        Elimina un paciente de la base de datos.

        Args:
            id_paciente (str): ID del paciente a eliminar.
        """
        if id_paciente not in self.db:
            print("❌ El paciente no existe.")
            return

        del self.db[id_paciente]
        self._guardar_db()
        print(f"🗑️ Paciente {id_paciente} eliminado.")

    def listar_pacientes(self):
        """
        Lista todos los pacientes registrados.
        """
        if not self.db:
            print("📭 No hay pacientes registrados.")
            return

        print("\n📋 Lista de pacientes:")
        for pid, datos in self.db.items():
            print(f"ID: {pid} | Nombre: {datos['nombre']} | Edad: {datos['edad']} | Género: {datos['genero']}")
