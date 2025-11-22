from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import request
from datetime import datetime
from typing import Tuple
from zoneinfo import ZoneInfo

from api.models.user_perfil_model import UserPerfil
from api.models.log_api_model import LogApi

def auth_decorator(permitidos: Tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except:
                data = {
                    'ds_endpoint' : request.path,
                    'sg_metodo' : request.method,
                    'nu_user' : None,
                    'dh_request' : datetime.now(ZoneInfo("America/Sao_Paulo")),
                    'ds_status' : 'Não autenticado',
                    'ds_query_string' : request.query_string.decode('utf-8')
                }
                gravar_log_banco(data)
                return {"erro": True, "message": f"Token JWT ausente"}, 401
            id = get_jwt_identity()
            perfis = listar_perfis_por_usuario(id)
            if not any(item in permitidos for item in perfis):
                data = {
                    'ds_endpoint' : request.path,
                    'sg_metodo' : request.method,
                    'nu_user' : id,
                    'dh_request' : datetime.now(ZoneInfo("America/Sao_Paulo")),
                    'ds_status' : 'Não autorizado',
                    'ds_query_string' : request.query_string.decode('utf-8')
                }
                gravar_log_banco(data)
                return {"erro": True, "message": f"Usuário não autorizado"}, 403    
            data = {
                'ds_endpoint' : request.path,
                'sg_metodo' : request.method,
                'nu_user' : id,
                'dh_request' : datetime.now(ZoneInfo("America/Sao_Paulo")),
                'ds_status' : 'Autorizado',
                'ds_query_string' : request.query_string.decode('utf-8')
            }
            gravar_log_banco(data)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def listar_perfis_por_usuario(nu_user):
    perfis = UserPerfil.query.with_entities(UserPerfil.nu_perfil).filter_by(nu_user=nu_user).all()
    return [r.nu_perfil for r in perfis]

def gravar_log_banco(data):
    data['nu_log_api'] = 0
    from api import db
    log = LogApi(**data)
    try:
        db.session.add(log)
        db.session.commit()
    except:
        db.session.rollback()