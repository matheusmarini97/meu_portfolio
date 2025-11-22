import os
import google.generativeai as genai

# configurar chave
genai.configure(api_key="AIzaSyBAqmb7kzIf5nSYo_O5R09ucPqUMRTGq3m")

# escolher modelo
model = genai.GenerativeModel("models/gemini-2.5-flash-lite") 

# gerar conteúdo
response = model.generate_content("meu_prompt_aqui")
print(response.text)