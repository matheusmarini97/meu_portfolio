from api.exceptions import UserNotFound, ForeignKey, IntegrityError
from .usuario_model import UsuarioModel
from api import db

class UsuarioRepository:

    @staticmethod
    def criar_usuario(usuario: UsuarioModel) -> UsuarioModel:
        try:
            db.session.add(usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise IntegrityError('Usuário já cadastrado')
        return usuario
    
    @staticmethod
    def alterar_usuario(usuario: dict, id: int) -> UsuarioModel:
        usuario_db = UsuarioModel.query.filter_by(id=id).first()
        if not usuario_db:
            raise UserNotFound('Usuário não encontrado')
        for key, value in usuario.items():
            setattr(usuario_db, key, value)
        try:
            db.session.add(usuario_db)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception('Erro desconhecido')
        return usuario_db

    @staticmethod
    def listar_usuarios() -> list[UsuarioModel]:
        usuarios = UsuarioModel.query.all()
        if not usuarios:
            raise UserNotFound('Nenhum usuário encontrado')
        return usuarios
        
    @staticmethod
    def listar_usuario(id: int) -> UsuarioModel:
        usuario = UsuarioModel.query.filter_by(id=id).first()
        if not usuario:
            raise UserNotFound('Usuário não encontrado')
        return usuario

    @staticmethod
    def remover_usuario(id: int) -> None:
        usuario = UsuarioModel.query.filter_by(id=id).first()
        if not usuario:
            raise UserNotFound('Usuário não encontrado')
        try:
            db.session.delete(usuario)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise ForeignKey('Existem registros para esse usuário e por isso ele não pode ser removido')
        return