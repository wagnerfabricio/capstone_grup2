# API e-comerce Won-Sushi

Api com rotas para controle de um sushi/restaurante com banco de dados em PosgreSQL.

# Url base

Url base dessa API é:
desenvolvimento: 

- **localhost:5000/**

produção: 

- **link do heroku em breve !!!!!!**

# Rotas que não precisam de autorização

Sem fazer o login, o usuário poderá se cadastrar, logar e ver a lista de produtos disponíveis. 

Todas as demais rotas precisam de autenticação do tipo Bearer com Token de acesso.

As rotas administrativas também só poderão ser acessadas por usuários que possuam a classe “admin”.

# Endpoints

O projeto consiste em 'X’ endPoints pricipais:

- **`POST /register`:**  para registro de usuários
- **`POST /login`:**  para login de usuário
- **`admin`:**  funções de administrador (necessário o usuário ser da classe admin)*
    - **`GET /admin/users` :** retorna uma lista dos usuários
    - **`GET /admin/users/<user_id>` :** retorna um usuário em específico
    - **`PATCH /admin/users/<user_id>` :** update de um usuário em específico
    - **`DELETE /admin/users/<user_id>` : deleta** um usuário em específico

*rotas que requerem autorização via token

---

# Rotas que não exigem autenticação

As seguintes rotas não exigem autenticação

## Usuário

Os usuários poderão se logar ou se cadastrar sem a necessidade de autenticação.

### Cadastro

```python
POST /register
```

Para o cadastro do usuário, obrigatoriamente os seguintes campos deverão ser informados: name, email e password, sendo possível também informar 'birthday’ no formato MM/DD/AAAA. 

A requisição deverá seguir o seguinte formato:

```json
{
    "name": "John Wick",
    "email": "johnwick@gmail.com",
    "password": "BabaYaga"
}
```

Exemplos de respostas:

- 201 CREATED: em caso de sucesso com a seguinte mensagem contendo os dados do usuário:
    
    ```json
    {
        "name": "John Wick",
        "email": "johnwick@gmail.com"
    }
    ```
    
- 409 CONFLICT:
    - caso o usuário já exista:
        
        ```json
        {
        	"error": "email = jaum@mail.com  already exists."
        }
        ```
        
- 400 BAD REQUEST:
    - Caso não tenha sido fornecido algumas das chaves obrigatórias (indicando qual chave está faltando):
        
        ```json
        {
        	"error": "missing keys",
        	"expected": [
        		"email",
        		"password",
        		"name"
        	],
        	"received": [
        		"password",
        		"birthday",
        		"name"
        	],
        	"missing": [
        		"email"
        	]
        }
        ```
        
    - Caso a senha tenha menos que 8 caracteres:
        
        ```json
        {
        	"error": "Field password must be at least 8 characters long"
        }
        ```
        
    - Caso o email seja inválido:
        
        ```json
        {
        	"error": "Invalid email address"
        }
        ```
        
    

### Login

```python
POST /login
```

Endpoint a ser utilizado para realizar login por usuários já cadastrados, obrigatoriamente as seguintes chaves deverão ser informadas: email e password.

A requisição deverá seguir o seguinte formato:

```json
{
    "email": "johnwick@gmail.com",
    "password": "BabaYaga"
}
```

Exemplos de respostas:

- 200 OK: em caso de sucesso retornando um access_token para ser utilizado nas rotas que exigem autenticação.
    
    ```json
    {
    	"data": {
    		"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MTAwMzMwMSwianRpIjoiODA0MmY4MTktMDFhZC00ZTA5LThkZWEtN2NmZTFiNzEwYzc4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJlbWFpbCI6ImpvaG53aWNrQGdtYWlsLmNvbSIsIm5hbWUiOiJKb2huIFdpY2sifSwibmJmIjoxNjUxMDAzMzAxLCJleHAiOjE2NTM1OTUzMDF9.fBtJ9MqQDgcNnbF5pCnfSAuRGCI0G3xZlKeVEFho-ls",
    		"user": {
    			"email": "johnwick@gmail.com",
    			"name": "John Wick",
    			"id": "cd61d8d4-7f3e-47da-8f1f-642b323655aa",
    			"admin": false
    		}
    	}
    }
    ```
    
- 401 UNAUTHORIZED: caso o email ou senha sejam inválidos.
    
    ```json
    {
    	"error": "Invalid email or password"
    }
    ```
    

---

# Rotas que EXIGEM autenticação

Todas as rotas seguintes exigem que o usuário esteja autenticado/logado através do método Bearer com o token do usuário.
A validade do token de autenticação é de 30 (trinta) dias.

**Caso o token/jwt esteja expirado, ou não seja informado as seguintes respostas serão retornadas:**

- **401 UNAUTHORIZED**: caso o token tenha expirado.
    
    ```json
    {
      "msg": "Token has expired"
    }
    ```
    

- **422 UNPROCESSABLE ENTITY:** caso o token não seja informado.
    
    ```json
    {
      "msg": "Not enough segments"
    }
    ```
    

## Rotas de usuário classe **administrador**:

Para ter acesso as rotas administrativas o usuário deverá estar logado e ser da classe administrador.

### **Listar todos os usuários**

Usuários de classe administrador poderão listar todos os usuários cadastrados através do endpoint:

```python
GET /admin/users
```

Exemplo de resposta:

- 200 OK: com a lista de usuários cadastrados
    
    ```json
    [
    	{
    		"id": "445e4bcc-0a18-44ff-b2a1-365586e20ac0",
    		"name": "Jaum San",
    		"email": "jaum@mail.com",
    		"birthday": "Tue, 02 Mar 1982 00:00:00 GMT"
    	},
    	{
    		"id": "cd61d8d4-7f3e-47da-8f1f-642b323655aa",
    		"name": "John Wick",
    		"email": "johnwick@gmail.com",
    		"birthday": null
    	}
    ]
    ```
    
- 200 OK: caso a tabela esteja em branco
    
    ```json
    []
    ```
    

### Listar um usuário específico

Administradores poderão verificar um usuário específico pelo seu id através do endpoint:

```python
GET /admin/users/<user_id>
```

Exemplo de respostas:

- 200 OK
    
    ```json
    {
    		"id": "cd61d8d4-7f3e-47da-8f1f-642b323655aa",
    		"name": "John Wick",
    		"email": "johnwick@gmail.com",
    		"birthday": null
    	}
    ```
    

- 400 NOT FOUND: caso o usuário/id não exista.
    
    ```json
    {
    	"error": "user id not found"
    }
    ```
    

- **401 UNAUTHORIZED**: Caso o usuário não seja da classe admin:
    
    ```json
    {
    	"error": "you are not authorized to access this page"
    }
    ```
    

### **Alteração de usuários**

Altereções dos dados do usuário por um admisntrador como name, email, password ou birthday, se dará através do seguinte end point:

```python
PATCH /admin/users/<user_id>
```

Um ou mais valores podem ser passados através da requisição.
ex.:

```json
{
	"name": "Kenzo Jr",
  "birthday": "12/03/2000"
}
```

Exemplo de resposta:

- 200 OK: caso tudo tenha sido enviado corretamente, sem corpo de resposta.

- 400 NOT FOUND: caso o usuário/id não exista.
    
    ```json
    {
    	"error": "user id not found"
    }
    ```
    

- **401 UNAUTHORIZED**:  Caso o usuário não seja da classe admin:
    
    ```json
    {
    	"error": "you are not authorized to access this page"
    }
    ```
    

### Deletar um usuário:

Administradores poderão apagar contas de usuários através do endpoint:

```python
DELETE /admin/users/<user_id>
```

Exemplo de respostas:

- 200 OK: caso o usuário tenha sido deletado, sem corpo de mensagem.

- 400 NOT FOUND: caso o usuário/id não exista.
    
    ```json
    {
    	"error": "user id not found"
    }
    ```
    
- **401 UNAUTHORIZED**: caso o usuário não seja da classe admin.