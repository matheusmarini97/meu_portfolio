from flask_restx import Resource, Namespace
from .usuario_service import UsuarioService
from .usuario_schema import UsuarioSchema
from api.exceptions import FieldNotFound
from flask import request

usuario_namespace = Namespace('usuario', description='Recursos do usuário')

@usuario_namespace.route('')
class UsuarioList(Resource):
    def get(self):
        usuarios = UsuarioService.service_get_usuarios()
        return UsuarioSchema(many=isinstance(usuarios, list), exclude=['senha']).dump(usuarios)
    
    def post(self):
        usuario = UsuarioSchema().load(request.json)
        usuario = UsuarioService.service_post_usuario(usuario)
        return UsuarioSchema(exclude=['senha']).dump(usuario)

@usuario_namespace.route('/<int:id>')
class Usuario(Resource):
    def get(self, id):
        usuario = UsuarioService.service_get_usuario(id)
        return UsuarioSchema(many=isinstance(usuario, list), exclude=['senha']).dump(usuario)
    
    def delete(self, id):
        UsuarioService.service_delete_usuario(id)
        return {}, 204
    
    def patch(self, id):
        usuario = UsuarioSchema(partial=True).load(request.json)
        if 'nova_senha' not in usuario:
            raise FieldNotFound('Campo nova_senha inválido')
        usuario = UsuarioService.service_patch_usuario(usuario, id)
        return UsuarioSchema(many=isinstance(usuario, list), exclude=['senha', 'nova_senha']).dump(usuario), 200
    