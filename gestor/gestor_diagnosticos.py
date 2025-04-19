import json
import os
import sys
sys.path.append('C:\\Users\\srodriguez\\Desktop\\papila_diagnosticos 2\\papila_diagnosticos 2\\papila_diagnosticos\\modelos')

from modelos.diagnostico import Diagnostico


class GestorDiagnosticos:
    """
    Clase encargada de gestionar diagnósticos oftalmológicos, incluyendo
    registro, eliminación, listado y persistencia en archivos JSON.
    """

    def __init__(self, ruta_db: str, db_pacientes: str):
        self.ruta_db = ruta_db
        self.ruta_db_pacientes = db_pacientes
        self.db = self._cargar_db()
        self.ultimo_id = self._obtener_ultimo_id()

    def _cargar_db(self):
        if not os.path.exists(self.ruta_db):
            return {}
        with open(self.ruta_db, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def _guardar_db(self):
        with open(self.ruta_db, "w", encoding="utf-8") as f:
            json.dump(self.db, f, indent=4)

    def _obtener_ultimo_id(self):
        if not self.db:
            return 0
        return max(int(did) for did in self.db.keys())

    def _generar_id(self):
        self.ultimo_id += 1
        return str(self.ultimo_id).zfill(3)

    def _paciente_existe(self, id_paciente: str) -> bool:
        if not os.path.exists(self.ruta_db_pacientes):
            return False
        with open(self.ruta_db_pacientes, "r", encoding="utf-8") as f:
            try:
                db_pacientes = json.load(f)
                return id_paciente in db_pacientes
            except json.JSONDecodeError:
                return False

    def registrar_diagnostico(self, id_paciente: str, fecha: str, d1: float, d2: float, astigmatismo: float, tipo: str):
        """
        Registra un nuevo diagnóstico asociado a un paciente.

        Args:
            id_paciente (str): ID del paciente relacionado.
            fecha (str): Fecha del diagnóstico.
            d1 (float): Dioptría 1.
            d2 (float): Dioptría 2.
            astigmatismo (float): Valor del astigmatismo.
            tipo (str): Tipo de ojo ("OD" o "OS").
        """
        if not self._paciente_existe(id_paciente):
            print("❌ El paciente no existe.")
            return

        if tipo not in ("OD", "OS"):
            print("❌ Tipo inválido. Debe ser 'OD' (ojo derecho) o 'OS' (ojo izquierdo).")
            return

        nuevo_id = self._generar_id()
        diagnostico = Diagnostico(
            id_=nuevo_id,
            id_paciente=id_paciente,
            fecha=fecha,
            dioptria_1=d1,
            dioptria_2=d2,
            astigmatismo=astigmatismo,
            tipo=tipo
        )
        self.db[nuevo_id] = diagnostico.to_dict()
        self._guardar_db()
        print(f"✅ Diagnóstico registrado con ID {nuevo_id}")

    def eliminar_diagnostico(self, id_diagnostico: str):
        if id_diagnostico not in self.db:
            print("❌ El diagnóstico no existe.")
            return
        del self.db[id_diagnostico]
        self._guardar_db()
        print(f"🗑️ Diagnóstico {id_diagnostico} eliminado.")

    def listar_diagnosticos(self, id_paciente: str = None):
        if not self.db:
            print("📭 No hay diagnósticos registrados.")
            return

        print("\n📋 Lista de diagnósticos:")
        for did, datos in self.db.items():
            if id_paciente and datos["id_paciente"] != id_paciente:
                continue
            print(
                f"ID: {did} | Paciente: {datos['id_paciente']} | Fecha: {datos['fecha']} | "
                f"D1: {datos['dioptria_1']} | D2: {datos['dioptria_2']} | "
                f"Astigmatismo: {datos['astigmatismo']} | Tipo: {datos['tipo']}"
            )
