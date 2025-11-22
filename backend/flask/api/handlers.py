from flask import Flask, jsonify
from api.exceptions import UserNotFound, IntegrityError, FieldNotFound, InvalidPassword
from marshmallow import ValidationError

def handle_raise(error, status):
    return jsonify(error = True, message = error), status

def registrar_error_handle(app: Flask):
    @app.errorhandler(UserNotFound)
    def user_not_found(e):
        return handle_raise(str(e), 404)
    
    @app.errorhandler(Exception)
    def exception(e):
        return handle_raise(str(e), 400)
    
    @app.errorhandler(IntegrityError)
    def integrity_error(e):
        return handle_raise(str(e), 409)
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return handle_raise(e.messages, 400)

    @app.errorhandler(FieldNotFound)
    def handle_validation_error(e: FieldNotFound):
        return handle_raise(str(e), 400)

    @app.errorhandler(InvalidPassword)
    def handle_validation_error(e: InvalidPassword):
        return handle_raise(str(e), 400)