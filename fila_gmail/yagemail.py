import yagmail
from os import getenv

usuario = getenv('MAIL_USER')
senha = getenv('MAIL_PASS')
msg_from = getenv('MAIL_MESSAGE_FROM')

def send_email(to: str, subject: str, contents: str):
    yag = yagmail.SMTP(user=usuario, password=senha)
    yag.send(
        to=to, subject=[subject], contents=contents,headers={
        'From' : F'{msg_from} <{usuario}>'
        })
    yag.close()