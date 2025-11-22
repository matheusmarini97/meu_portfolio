from multiprocessing import Process
from database import SessionLocal
from yagemail import send_email
from datetime import datetime
from zoneinfo import ZoneInfo
from model import FilaEmail
from time import sleep
import logging
import sys
from dotenv import load_dotenv

load_dotenv()

def log_instance():
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s [%(levelname)s] %(message)s", 
        handlers=[ logging.StreamHandler(sys.stdout)])
    logger = logging.getLogger(__name__)
    return logger

def envios_imediatos():
    logger = log_instance()
    nao_enviar = False 
    while True:
        with SessionLocal() as session:
            email = session.query(FilaEmail).filter(FilaEmail.ic_enviado != 1, FilaEmail.dh_envio == None).first()
            if not email:
                sleep(2)
                if not nao_enviar:
                    logger.info('Sem emails na fila de envios imediatos')
                    nao_enviar = True
                continue
            send_email(email.no_email,email.no_assunto, email.no_conteudo)
            logger.info(f'Email não agendado enviado para {email.no_email}')
            email.ic_enviado = 1
            email.dh_enviado = datetime.now(ZoneInfo("America/Sao_Paulo"))
            try:
                session.add(email)
                session.commit()
                nao_enviar = False
            except:
                session.rollback()

def envios_agendados():
    logger = log_instance()
    nao_enviar = False 
    while True:
        with SessionLocal() as session:
            email = session.query(FilaEmail).filter(
                FilaEmail.ic_enviado != 1, 
                FilaEmail.dh_envio < datetime.now(ZoneInfo("America/Sao_Paulo"))
                ).order_by(FilaEmail.dh_envio.asc()).first()
            if not email:
                sleep(2)
                if not nao_enviar:
                    logger.info('Sem emails na fila de envios agendados')
                    nao_enviar = True
                continue
            send_email(email.no_email, email.no_assunto, email.no_conteudo)
            logger.info(f'Email agendado enviado para {email.no_email}')
            email.ic_enviado = 1
            email.dh_enviado = datetime.now(ZoneInfo("America/Sao_Paulo"))
            try:
                session.add(email)
                session.commit()
                nao_enviar = False
            except:
                session.rollback()



if __name__ == "__main__":
    p1 = Process(target=envios_imediatos)
    p2 = Process(target=envios_agendados)
    p1.start()
    p2.start()