from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class SendMail:
    def __init__(self):
        self.SMTP_SERVER = ""
        self.SMTP_PORT = 0 
        self.EMAIL_USUARIO = ""
        self.EMAIL_SENHA = ""
        self.servidor = self.__iniciarConexao()

    # FUNÇÃO PARA INICIAR CONEXÃO COM SMTP
    def __iniciarConexao(self):
        try:
            servidor = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            servidor.starttls()
            servidor.login(self.EMAIL_USUARIO, self.EMAIL_SENHA)
        except Exception as e:
            print(f"Erro ao iniciar conexão: {e}")
            raise e
        return servidor
            
    def __enviarEmail(self, mail, nome, path_certificado):
        # Configuração do e-mail
        msg = MIMEMultipart()
        msg["From"] = f'SevenPass {self.EMAIL_USUARIO}'
        msg["To"] = mail
        msg["Subject"] = 'Certificado do Simpósio sobre Sexualidade'

        # Corpo do e-mail (usa uma mensagem padrão se nenhum conteúdo for fornecido)
        mensagem = self.__html_mail(nome)
        msg.attach(MIMEText(mensagem, "html"))

        # Anexar o certificado em PDF, se fornecido
        if path_certificado:
            try:
                print(f"Tentando abrir: {path_certificado}")
                with open(path_certificado, "rb") as f:
                    pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
                    pdf_attachment.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename="certificado_simpósio_sexualidade.pdf"
                    )
                    msg.attach(pdf_attachment)
            except Exception as e:
                print(f"Erro ao anexar o certificado PDF: {e}")
                raise e
        else:
            print("Aviso: Nenhum certificado PDF foi fornecido para anexar.")

        # Enviar o e-mail
        try:
            self.servidor.sendmail(f'SevenPass {self.EMAIL_USUARIO}', msg["To"], msg.as_string())
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            raise e

        return

    def __html_mail(self, nome):
        content = f'''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
            body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            }}
            .container {{
            background-color: #ffffff;
            max-width: 600px;
            margin: 40px auto;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }}
            p {{
            color: #444444;
            font-size: 15px;
            line-height: 1.6;
            }}
            .footer {{
            margin-top: 30px;
            font-size: 12px;
            color: #999999;
            text-align: center;
            }}
        </style>
        </head>
        <body>
        <div class="container">
            <h2>Olá, {nome.split()[0]}!</h2>
            <p>Seu certificado de participação no simpósio <strong>Sem Tabus: Sexualidade & Jovem Adventista</strong> está em anexo.</p>
            <p>Atenciosamente,<br>Equipe SevenPass</p>

            <div class="footer">
            Este é um e-mail automático. Por favor, não responda.
            </div>
        </div>
        </body>
        </html>

    '''
        return content

    def run(self):
        import pandas as pd
        import shutil
        df = pd.read_csv('processados/dados.csv', delimiter=';', encoding='utf-8')

        for index, row in df.iterrows():

            data = {
                'email' : row['email'],
                'nome' : row['user'],
                'caminho_arquivo' : f'certificados/{row['nome_arquivo']}_certificado.pdf'
            }
            
            print(f'Iniciando o preparo e envio do certificado para o email: {data['email']}')
            try:
                email = data['email']
                caminho_arquivo = data['caminho_arquivo']
                nome = data['nome']

            except Exception as e:
                print(f'Erro: {e}')

            origem = f'certificados/{row['nome_arquivo']}_certificado.pdf'
            destino = f'enviados/{row['nome_arquivo']}_certificado.pdf'

            try:
                self.__enviarEmail(mail=email, nome=nome, path_certificado=caminho_arquivo)
                print(f'Email enviado com sucesso para o email: {data['email']}')
                shutil.move(origem, destino)
            except Exception as e:
                print(f'Erro: {e}')
            

            

            

if __name__ == '__main__':
    mailer = SendMail()
    mailer.run()