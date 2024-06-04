import requests
import jwt
import datetime

# URL do seu servidor GraphQL
url = 'http://localhost:5000/graphql'

# Chave secreta usada para gerar o token JWT
SECRET_KEY = 'j2w9UHvP4bQz9g9V7vQ4tM6z2eK5tYx3'

# Função para gerar um token JWT
def generate_api_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Gera um token para o usuário com ID 1 (ou outro ID de teste)
api_token = generate_api_token(1)

# Headers para incluir o token de API
headers = {
    'Content-Type': 'application/json',
    'Authorization': api_token
}

# Consultas e variáveis para criação, atualização, exclusão e obtenção de usuários e contratos
create_user_gql = """
mutation createUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
"""

create_user_variables = {
    "input": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "password"
    }
}

get_user_gql = """
query getUser($id: ID!) {
  getUser(id: $id) {
    id
    name
    email
  }
}
"""

get_user_variables = {
    "id": "1"
}

update_user_gql = """
mutation updateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    email
    error {
      message
    }
  }
}
"""

update_user_variables = {
    "id": "1",
    "input": {
        "name": "John Doe Updated",
        "email": "john.doe.updated@example.com",
        "password": "newpassword"
    }
}

delete_user_gql = """
mutation deleteUser($id: ID!) {
  deleteUser(id: $id) {
    success
    message
  }
}
"""

delete_user_variables = {
    "id": "1"
}

create_contract_gql = """
mutation createContract($input: CreateContractInput!) {
  createContract(input: $input) {
    id
    description
    user_id
    created_at
    fidelity
    amount
  }
}
"""

create_contract_variables = {
    "input": {
        "description": "New Contract",
        "user_id": "1",
        "created_at": "2024-05-22T00:00:00",
        "fidelity": 5,
        "amount": 1000.00
    }
}

update_contract_gql = """
mutation updateContract($id: ID!, $input: UpdateContractInput!) {
  updateContract(id: $id, input: $input) {
    id
    description
    user_id
    created_at
    fidelity
    amount
  }
}
"""

update_contract_variables = {
    "id": "1",
    "input": {
        "description": "Updated Contract",
        "user_id": "1",
        "created_at": "2024-05-22T00:00:00",
        "fidelity": 10,
        "amount": 2000.00
    }
}

get_contract_gql = """
query getContract($id: ID!) {
  getContract(id: $id) {
    description
    user_id
    user {
      id
      name
      email
    }
    created_at
    fidelity
    amount
  }
}
"""

get_contract_variables = {
    "id": "1"
}

get_contract_withoutnested_gql = """
query getContract($id: ID!) {
  getContract(id: $id) {
    description
    user_id
    created_at
    fidelity
    amount
  }
}
"""

get_contracts_by_user_gql = """
query getContractsByUser($user_id: ID!) {
  getContractsByUser(user_id: $user_id) {
    Contracts {
      id
      description
      user_id
      created_at
      fidelity
      amount
    }
    nextToken
  }
}
"""

get_contracts_by_user_variables = {
    "user_id": "1"
}

delete_contract_gql = """
mutation deleteContract($id: ID!) {
  deleteContract(id: $id) {
    success
    message
  }
}
"""

delete_contract_variables = {
    "id": "1"
}

def execute_gql(query, variables):
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    return response.json()

# Executando as consultas
print("Response for creating user:", execute_gql(create_user_gql, create_user_variables), "\n")
print("Response for getting user:", execute_gql(get_user_gql, get_user_variables), "\n")
print("Response for updating user:", execute_gql(update_user_gql, update_user_variables), "\n")
print("Response for creating contract:", execute_gql(create_contract_gql, create_contract_variables), "\n")
print("Response for getting contract:", execute_gql(get_contract_gql, get_contract_variables), "\n")
print("Response for getting contract without:", execute_gql(get_contract_withoutnested_gql, get_contract_variables), "\n")
print("Response for getting contracts by user:", execute_gql(get_contracts_by_user_gql, get_contracts_by_user_variables), "\n")
print("Response for deleting user:", execute_gql(delete_user_gql, delete_user_variables), "\n")
print("Response for deleting contract:", execute_gql(delete_contract_gql, delete_contract_variables), "\n")
