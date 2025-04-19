from typing import Dict

class Paciente:
    """
    Clase que representa a un paciente.

    Atributos:
        id (str): Identificador único del paciente.
        nombre (str): Nombre completo del paciente.
        edad (int): Edad del paciente.
        genero (str): Género del paciente.
    """

    def __init__(self, id_: str, nombre: str, edad: int, genero: str):
        """
        Inicializa una nueva instancia de la clase Paciente.

        Args:
            id_ (str): Identificador único del paciente.
            nombre (str): Nombre completo del paciente.
            edad (int): Edad del paciente.
            genero (str): Género del paciente.
        """
        self.id = id_
        self.nombre = nombre
        self.edad = edad
        self.genero = genero

    def to_dict(self) -> Dict:
        """
        Convierte la instancia de Paciente a un diccionario.

        Returns:
            Dict: Un diccionario que representa la instancia de Paciente.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "genero": self.genero
        }

    @staticmethod
    def from_dict(data: Dict):
        """
        Crea una instancia de Paciente a partir de un diccionario.

        Args:
            data (Dict): Un diccionario con los datos del paciente.

        Returns:
            Paciente: Una nueva instancia de Paciente creada a partir del diccionario.
        """
        return Paciente(
            id_=data["id"],
            nombre=data["nombre"],
            edad=data["edad"],
            genero=data["genero"]
        )
