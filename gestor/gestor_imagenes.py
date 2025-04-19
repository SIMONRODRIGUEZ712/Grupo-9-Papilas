import json
import os
import shutil
from modelos.imagen import ImagenPapila


class GestorImagenes:
    """
    Clase encargada de gestionar imágenes de papilas, incluyendo su registro,
    eliminación, listado y persistencia en disco.
    """

    def __init__(self, ruta_db: str, carpeta_imagenes: str, db_diagnosticos: str, db_pacientes: str):
        """
        Inicializa el gestor de imágenes.

        Args:
            ruta_db (str): Ruta al archivo JSON de la base de datos de imágenes.
            carpeta_imagenes (str): Carpeta donde se guardarán las imágenes físicamente.
            db_diagnosticos (str): Ruta a la base de datos de diagnósticos.
            db_pacientes (str): Ruta a la base de datos de pacientes.
        """
        self.ruta_db = ruta_db
        self.ruta_db_diagnosticos = db_diagnosticos
        self.ruta_db_pacientes = db_pacientes
        self.carpeta_imagenes = carpeta_imagenes
        self.db = self._cargar_db()
        self.ultimo_id = self._obtener_ultimo_id()

        os.makedirs(carpeta_imagenes, exist_ok=True)

    def _cargar_db(self):
        """
        Carga la base de datos desde el archivo JSON.

        Returns:
            dict: Base de datos de imágenes.
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
        Guarda la base de datos de imágenes en el archivo JSON.
        """
        with open(self.ruta_db, "w", encoding="utf-8") as f:
            json.dump(self.db, f, indent=4)

    def _obtener_ultimo_id(self):
        """
        Obtiene el último ID usado para las imágenes.

        Returns:
            int: Último ID numérico usado.
        """
        if not self.db:
            return 0
        return max(int(iid) for iid in self.db.keys())

    def _generar_id(self):
        """
        Genera un nuevo ID autoincremental con formato de tres dígitos.

        Returns:
            str: Nuevo ID como cadena, con ceros a la izquierda.
        """
        self.ultimo_id += 1
        return str(self.ultimo_id).zfill(3)

    def _diagnostico_valido(self, id_diagnostico):
        """
        Verifica si un diagnóstico existe en la base de datos.

        Args:
            id_diagnostico (str): ID del diagnóstico a verificar.

        Returns:
            bool: True si el diagnóstico existe, False en caso contrario.
        """
        if not os.path.exists(self.ruta_db_diagnosticos):
            return False
        with open(self.ruta_db_diagnosticos, "r", encoding="utf-8") as f:
            try:
                db_diag = json.load(f)
                return id_diagnostico in db_diag
            except json.JSONDecodeError:
                return False

    def _get_paciente_id(self, id_diagnostico):
        """
        Obtiene el ID del paciente asociado a un diagnóstico.

        Args:
            id_diagnostico (str): ID del diagnóstico.

        Returns:
            str or None: ID del paciente si se encuentra, None si no.
        """
        if not os.path.exists(self.ruta_db_diagnosticos):
            return None
        with open(self.ruta_db_diagnosticos, "r", encoding="utf-8") as f:
            db_diag = json.load(f)
            if id_diagnostico in db_diag:
                return db_diag[id_diagnostico]["id_paciente"]
        return None

    def registrar_imagen(self, id_diagnostico: str, ruta_origen: str, descripcion: str = "", tipo_ojo: str = "OD", fecha_captura: str = ""):
        """
        Registra una nueva imagen asociada a un diagnóstico.

        Args:
            id_diagnostico (str): ID del diagnóstico relacionado.
            ruta_origen (str): Ruta del archivo de imagen. Ej: C:\FundusImages\ImgPaciente2025.jpg.
            descripcion (str): Descripción opcional de la imagen.
            tipo_ojo (str): Tipo de ojo ("OD" o "OS").
            fecha_captura (str): Fecha de captura de la imagen en formato "YYYY-MM-DD".
        """
        if not self._diagnostico_valido(id_diagnostico):
            print("❌ Diagnóstico no encontrado.")
            return

        if not os.path.exists(ruta_origen):
            print("❌ La imagen no existe en la ruta especificada.")
            return

        id_imagen = self._generar_id()
        id_paciente = self._get_paciente_id(id_diagnostico)
        nombre_archivo = f"RET{id_paciente}{tipo_ojo}.jpg"
        ruta_destino = os.path.join(self.carpeta_imagenes, nombre_archivo)

        shutil.copy2(ruta_origen, ruta_destino)

        imagen = ImagenPapila(
            id_=id_imagen,
            id_diagnostico=id_diagnostico,
            archivo=nombre_archivo,
            descripcion=descripcion,
            tipo_ojo=tipo_ojo,
            fecha_captura=fecha_captura
        )
        self.db[id_imagen] = imagen.to_dict()
        self._guardar_db()
        print(f"✅ Imagen registrada con ID {id_imagen} y guardada como {nombre_archivo}")

    def eliminar_imagen(self, id_imagen: str):
        """
        Elimina una imagen tanto de la base de datos como del disco.

        Args:
            id_imagen (str): ID de la imagen a eliminar.
        """
        if id_imagen not in self.db:
            print("❌ Imagen no encontrada.")
            return

        nombre_archivo = self.db[id_imagen]["archivo"]
        ruta_fisica = os.path.join(self.carpeta_imagenes, nombre_archivo)

        if os.path.exists(ruta_fisica):
            os.remove(ruta_fisica)

        del self.db[id_imagen]
        self._guardar_db()
        print(f"🗑️ Imagen {id_imagen} eliminada correctamente.")

    def listar_imagenes(self, id_diagnostico: str = None):
        """
        Lista todas las imágenes registradas, o solo las de un diagnóstico específico.

        Args:
            id_diagnostico (str, opcional): Si se especifica, filtra las imágenes por este diagnóstico.
        """
        if not self.db:
            print("📭 No hay imágenes registradas.")
            return

        print("\n📸 Lista de imágenes:")
        for iid, datos in self.db.items():
            if id_diagnostico and datos["id_diagnostico"] != id_diagnostico:
                continue
            print(
                f"ID: {iid} | Diagnóstico: {datos['id_diagnostico']} | "
                f"Archivo: {datos['archivo']} | Descripción: {datos.get('descripcion', '')} | "
                f"Tipo Ojo: {datos['tipo_ojo']} | Fecha Captura: {datos['fecha_captura']}"
            )
