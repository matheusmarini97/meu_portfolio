from .usuario_repository import UsuarioRepository
from api.exceptions import UserNotFound, InvalidPassword
from .usuario_model import UsuarioModel
from .usuario_entity import UsuarioEntity
from passlib.hash import pbkdf2_sha256

class UsuarioService:
    @staticmethod
    def service_get_usuarios():
        usuarios = UsuarioRepository.listar_usuarios()
        return usuarios
    
    @staticmethod
    def service_get_usuario(id: int) -> UsuarioModel:
        usuario = UsuarioRepository.listar_usuario(id)
        return usuario
    
    @staticmethod
    def service_delete_usuario(id: int) -> None:
        UsuarioRepository.remover_usuario(id)
        return
    
    @staticmethod
    def service_post_usuario(usuario: dict) -> UsuarioModel:
        usuario = UsuarioEntity(**usuario)
        usuario.senha = pbkdf2_sha256.hash(usuario.senha)
        usuario = UsuarioModel(**usuario.__dict__)
        return UsuarioRepository.criar_usuario(usuario)
    
    @staticmethod
    def service_patch_usuario(usuario: dict, id: int) -> UsuarioModel:
        usuario_db = UsuarioRepository.listar_usuario(id)
        if 'nova_senha' in usuario:
            if not pbkdf2_sha256.verify(usuario['nova_senha'], usuario_db.senha):
                raise InvalidPassword('Credenciais inválidas')
            usuario['senha'] = pbkdf2_sha256.hash(usuario['senha'])
        return UsuarioRepository.alterar_usuario(usuario, id)