from api import ma
from marshmallow import fields, validate, EXCLUDE, validates, ValidationError
from .usuario_model import UsuarioModel
from password_validator import PasswordValidator

class UsuarioSchema(ma.Schema):
    id = fields.Integer(required=False)
    nome = fields.String(required=True)
    senha = fields.String(required=True)
    nova_senha = fields.String(required=False)
    email = fields.String(required=True, validate=validate.Email())
    idade = fields.Integer(required=True, strict=True)
    data_nascimento = fields.DateTime(required=True)

    @validates('senha')
    def validar_senha(self, value: str):
        schema = PasswordValidator()
        schema.min(8).max(100).has().uppercase().has().lowercase().has().digits()\
            .has().symbols().has().no().spaces()
        if not schema.validate(value):
            raise ValidationError("A senha precisa conter pelo menos 8 caracteres, uma letra minúscula, maiúscula, símbolo e um número")
   
    @validates('nova_senha')
    def validar_senha(self, value: str):
        schema = PasswordValidator()
        schema.min(8).max(100).has().uppercase().has().lowercase().has().digits()\
            .has().symbols().has().no().spaces()
        if not schema.validate(value):
            raise ValidationError("A senha precisa conter pelo menos 8 caracteres, uma letra minúscula, maiúscula, símbolo e um número")

    class Meta:
        model = UsuarioModel
        load_instance = False
        unknown = EXCLUDE
        ordered = True