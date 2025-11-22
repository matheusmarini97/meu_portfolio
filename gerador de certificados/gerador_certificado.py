from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

class GerarCertificado:
    def __init__(self, template_path):
        self.template = template_path
        self.__cria_pasta_certificados()
        self.draw = self.__importa_template()
        self.certificado = self.draw

    def __importa_template(self):
        self.img = Image.open(self.template)
        return ImageDraw.Draw(self.img)
        
    def __cria_pasta_certificados(self):
        os.makedirs('certificados', exist_ok=True)
        return
    
    def __insere_nome(self, nome: str) -> None:
        # INSERE O NOME NO CERTIFICADO
        fonte = ImageFont.truetype('arial.ttf', 80)
        texto = nome
        cx, cy = 1358, 900
        bbox = self.certificado.textbbox((0, 0), texto, font=fonte)
        largura_texto = bbox[2] - bbox[0]
        altura_texto = bbox[3] - bbox[1]
        x = cx - largura_texto // 2
        y = cy - altura_texto // 2
        self.certificado.text((x, y), texto, font=fonte, fill=(255, 255, 255))
        return

    def __insere_horas(self, horas: str) -> None:
        # INSERE O NUMERO DE HORAS NO CERTIFICADO
        fonte = ImageFont.truetype('arial.ttf', 45)
        texto = str(horas)
        cx, cy = 2323, 1142
        bbox = self.certificado.textbbox((0, 0), texto, font=fonte)
        largura_texto = bbox[2] - bbox[0]
        altura_texto = bbox[3] - bbox[1]
        x = cx - largura_texto // 2
        y = cy - altura_texto // 2
        self.certificado.text((x, y), texto, font=fonte, fill=(255, 255, 255))
        return

    def __insere_data(self):
        # INSERE A DATA NO CERTIFICADO
        agora = datetime.now()
        fonte = ImageFont.truetype('arial.ttf', 45)
        texto = agora.date().strftime('Ivatuba-PR, %d/%m/%Y')
        cx, cy = 1358, 1300
        bbox = self.certificado.textbbox((0, 0), texto, font=fonte)
        largura_texto = bbox[2] - bbox[0]
        altura_texto = bbox[3] - bbox[1]
        x = cx - largura_texto // 2
        y = cy - altura_texto // 2
        self.certificado.text((x, y), texto, font=fonte, fill=(255, 255, 255))       
        return

    def __salva_certificado(self, nome_arquivo: str) -> None:
        self.img.save(f'certificados/{nome_arquivo}_certificado.pdf')
        return
    
    def run(self, nome, horas, nome_arquivo):
        self.certificado = self.draw
        self.__cria_pasta_certificados()
        self.__insere_nome(nome=nome)
        self.__insere_horas(horas=horas)
        self.__insere_data()
        self.__salva_certificado(nome_arquivo=nome_arquivo)

if __name__ == '__main__':
    certificado = GerarCertificado('templates/simposio_sexualidade.png')
    certificado.run(nome='Matheus Marini De Oliveira', horas=24, nome_arquivo='MatheusMariniDeOliveira')