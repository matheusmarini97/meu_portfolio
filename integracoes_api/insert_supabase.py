import requests
from datetime import datetime

class InsertSupabase:
    def __init__(self):
        self.URL = 'https://mjjyogmavkwvlohutpuo.supabase.co/rest/v1/tb02_capturas'
        self.headers = {
            'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1qanlvZ21hdmt3dmxvaHV0cHVvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExNTI2NDYsImV4cCI6MjA3NjcyODY0Nn0.ggsAKMb8f7f2DsR7ZewfjA72xy_OlJ8Gg3zzVrfSA2s',
            'apiKey' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1qanlvZ21hdmt3dmxvaHV0cHVvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExNTI2NDYsImV4cCI6MjA3NjcyODY0Nn0.ggsAKMb8f7f2DsR7ZewfjA72xy_OlJ8Gg3zzVrfSA2s',
            'Content-Type' : 'application/json'
        }

    def insert(self, body: dict) -> requests:
        '''
        A função cria uma linha no banco e retorna o status, caso a gravação tenha sucesso, o status será 201
        Adicionar um dicionário com os seguintes campos
        {
            "no_placa" : string,
            "nu_velocidade" : float,
            "nu_temperatura" : float,
            "nu_umidade" : float,
            "dt_captura" : str(datetime.now()),
            "id_device" : int
        }
        '''
        response = requests.post(self.URL, json=body, headers=self.headers)
        
        return response.status_code

if __name__ == '__main__':
    body = {
        "no_placa" : "IOASDASD",
        "nu_velocidade" : 50.00,
        "nu_temperatura" : 24.00,
        "nu_umidade" : 55.00,
        "dt_captura" : str(datetime.now()),
        "id_device" : 1
    }
    insert = InsertSupabase()
    status = insert.insert(body)