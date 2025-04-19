from typing import Dict

class Diagnostico:
    """
    Clase que representa un diagnóstico oftalmológico realizado a un paciente.

    Atributos:
        id (str): Identificador único del diagnóstico.
        id_paciente (str): Identificador del paciente al que corresponde el diagnóstico.
        fecha (str): Fecha en que se realizó el diagnóstico (formato YYYY-MM-DD).
        dioptria_1 (float): Valor de la primera dioptría.
        dioptria_2 (float): Valor de la segunda dioptría.
        astigmatismo (float): Valor del astigmatismo.
        tipo (str): Tipo de ojo ('OD' = Ojo Derecho, 'OS' = Ojo Izquierdo).
    """

    def __init__(
        self,
        id_: str,
        id_paciente: str,
        fecha: str,
        dioptria_1: float,
        dioptria_2: float,
        astigmatismo: float,
        tipo: str
    ):
        if tipo not in ("OD", "OS"):
            raise ValueError("El tipo debe ser 'OD' o 'OS'.")

        self.id = id_
        self.id_paciente = id_paciente
        self.fecha = fecha
        self.dioptria_1 = dioptria_1
        self.dioptria_2 = dioptria_2
        self.astigmatismo = astigmatismo
        self.tipo = tipo

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "id_paciente": self.id_paciente,
            "fecha": self.fecha,
            "dioptria_1": self.dioptria_1,
            "dioptria_2": self.dioptria_2,
            "astigmatismo": self.astigmatismo,
            "tipo": self.tipo
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            id_=data["id"],
            id_paciente=data["id_paciente"],
            fecha=data["fecha"],
            dioptria_1=data["dioptria_1"],
            dioptria_2=data["dioptria_2"],
            astigmatismo=data["astigmatismo"],
            tipo=data["tipo"]
        )
