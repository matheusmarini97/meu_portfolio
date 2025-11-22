from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from database import Base
from os import getenv

class FilaEmail(Base):
    __tablename__ = f"{getenv('TABLENAME')}"

    nu_mail = Column(Integer, primary_key=True, autoincrement=True)
    nu_user = Column(Integer, nullable=False)
    no_email = Column(String(100), nullable=False)
    no_assunto = Column(String(200), nullable=False)
    no_conteudo = Column(String(4000), nullable=False)
    ic_enviado = Column(Integer, nullable=False, default=False)
    dh_create_at = Column(DateTime, server_default=func.now())
    dh_envio = Column(DateTime, nullable=True)
    dh_enviado = Column(DateTime, nullable=True)