
# 📄 Auth Decorator – Flask JWT

Este módulo contém o **`auth_decorator`**, desenvolvido para proteger endpoints em aplicações **Flask** utilizando **JWT (JSON Web Token)**.  
Ele também registra logs de todas as requisições em um banco de dados, permitindo auditoria de acessos autorizados, não autorizados ou não autenticados.

---

## 🔹 Funcionalidade

O `auth_decorator` realiza três ações principais:

1. **Verificação do JWT**  
   - Confirma se a requisição possui um token JWT válido.
   - Se o token estiver ausente ou inválido, retorna erro `401` e grava um log com status `"Não autenticado"`.

2. **Autorização por perfil de usuário**  
   - Consulta os perfis do usuário (`UserPerfil`) no banco de dados.
   - Permite acesso apenas se o usuário possuir algum dos perfis listados no parâmetro `permitidos`.
   - Caso o usuário não tenha permissão, retorna erro `403` e grava um log com status `"Não autorizado"`.

3. **Gravação de logs de API**  
   - Todos os acessos são registrados na tabela `LogApi` com informações como endpoint, método HTTP, usuário, query string e status da requisição.
   - Logs são gravados mesmo em caso de falha na autenticação ou autorização.

---

## 🔹 Parâmetros

```python
auth_decorator(permitidos: Tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7))
```

- permitidos: tupla de IDs de perfis que têm acesso ao endpoint.

- Valor padrão: (1, 2, 3, 4, 5, 6, 7)

---
## 🔹 Exemplo de Uso

```python
from flask import Flask, jsonify
from api.auth_decorator import auth_decorator

app = Flask(__name__)

@app.route('/meu-endpoint')
@auth_decorator(permitidos=(1, 3, 5))
def meu_endpoint():
    return jsonify({"mensagem": "Acesso permitido"})
```

- Apenas usuários com perfis 1, 3 ou 5 poderão acessar o endpoint /meu-endpoint.

- Todas as requisições são registradas na tabela LogApi.

---
## 🔹 Observações Técnicas

- Utiliza **flask_jwt_extended** para autenticação JWT.
- A função `listar_perfis_por_usuario` consulta os perfis associados ao usuário no banco.
- A função `gravar_log_banco` adiciona entradas de log na tabela `LogApi`, com rollback em caso de falha.
- Fuso horário utilizado para logs: `America/Sao_Paulo`.

---

## 🔹 Benefícios

- Centraliza **autenticação e autorização** em um único decorator.
- Permite **auditoria completa** de acessos à API.
- Fácil integração com múltiplos endpoints Flask.
