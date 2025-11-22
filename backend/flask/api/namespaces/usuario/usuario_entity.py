from dataclasses import dataclass
from datetime import date

@dataclass
class UsuarioEntity:
    id: int = None
    nome:str = None
    senha: str = None
    email: str = None
    idade: int = None
    data_nascimento: date = None