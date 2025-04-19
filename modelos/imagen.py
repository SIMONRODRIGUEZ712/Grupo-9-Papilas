from typing import Dict

class ImagenPapila:
    """
    Clase que representa una imagen de papila ocular asociada a un diagnóstico.

    Atributos:
        id (str): Identificador único de la imagen de la papila.
        id_diagnostico (str): Identificador del diagnóstico relacionado con la imagen.
        archivo (str): Ruta o nombre del archivo de la imagen.
        descripcion (str): Descripción opcional de la imagen.
        tipo_ojo (str): Indica si la imagen corresponde al ojo derecho (OD) o izquierdo (OS).
        fecha_captura (str): Fecha en que se capturó la imagen (formato YYYY-MM-DD).
    """

    def __init__(self, id_: str, id_diagnostico: str, archivo: str, descripcion: str = "",
                 tipo_ojo: str = "OD", fecha_captura: str = ""):
        self.id = id_
        self.id_diagnostico = id_diagnostico
        self.archivo = archivo
        self.descripcion = descripcion
        self.tipo_ojo = tipo_ojo
        self.fecha_captura = fecha_captura

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "id_diagnostico": self.id_diagnostico,
            "archivo": self.archivo,
            "descripcion": self.descripcion,
            "tipo_ojo": self.tipo_ojo,
            "fecha_captura": self.fecha_captura
        }

    @staticmethod
    def from_dict(data: Dict):
        return ImagenPapila(
            id_=data["id"],
            id_diagnostico=data["id_diagnostico"],
            archivo=data["archivo"],
            descripcion=data.get("descripcion", ""),
            tipo_ojo=data.get("tipo_ojo", "OD"),
            fecha_captura=data.get("fecha_captura", "")
        )
