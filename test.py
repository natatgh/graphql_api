import requests

# URL do seu servidor GraphQL
url = 'http://localhost:5000/graphql'

# Headers para indicar que estamos enviando uma consulta GraphQL
headers = {'Content-Type': 'application/json'}

# Consulta para criar um usuário
create_user_gql = """
mutation createUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
"""

# Parâmetros para a consulta de criação de usuário
create_user_variables = {
    "input": {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
}

# Consulta para obter um usuário por ID
get_user_gql = """
query getUser($id: ID!) {
  getUser(id: $id) {
    id
    name
    email
  }
}
"""

# Parâmetros para a consulta de obtenção de usuário por ID
get_user_variables = {
    "id": "1"  # ID do usuário que você deseja obter
}

# Consulta para atualizar um usuário
update_user_gql = """
mutation updateUser($id: ID!, $input: CreateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    email
  }
}
"""

# Parâmetros para a consulta de atualização de usuário
update_user_variables = {
    "id": "1",  # ID do usuário que você deseja atualizar
    "input": {
        "name": "John Doe Updated",
        "email": "john.doe.updated@example.com"
    }
}

# Consulta para excluir um usuário
delete_user_gql = """
mutation deleteUser($id: ID!) {
  deleteUser(id: $id) {
    success
    message
  }
}
"""

# Parâmetros para a consulta de exclusão de usuário
delete_user_variables = {
    "id": "1"  # ID do usuário que você deseja excluir
}

# Consulta para criar um contrato
create_contract_gql = """
mutation createContract($input: CreateContractInput!) {
  createContract(input: $input) {
    contract {
      id
      description
      userId
      createdAt
      fidelity
      amount
    }
  }
}
"""

# Parâmetros para a consulta de criação de contrato
create_contract_variables = {
    "input": {
        "description": "New Contract",
        "userId": "1",  # ID do usuário associado ao contrato
        "createdAt": "2024-05-22T00:00:00",  # Formato ISO 8601
        "fidelity": 5,
        "amount": 1000.00
    }
}

# Consulta para obter um contrato por ID
get_contract_gql = """
query getContract($id: ID!) {
  getContract(id: $id) {
    id
    description
    user {
      id
      name
      email
    }
    createdAt
    fidelity
    amount
  }
}
"""

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

delete_contract_gql = """
mutation deleteContract($id: ID!) {
  deleteContract(id: $id) {
    success
    message
  }
}
"""

# Parâmetros para a consulta de obtenção de contrato por ID
get_contract_variables = {
    "id": "1"  # ID do contrato que você deseja obter
}

# Executando as consultas usando requests
response = requests.post(url, json={'query': create_user_gql, 'variables': create_user_variables}, headers=headers)
print("Response for creating user:", response.json())

response = requests.post(url, json={'query': get_user_gql, 'variables': get_user_variables}, headers=headers)
print("Response for getting user:", response.json())

response = requests.post(url, json={'query': update_user_gql, 'variables': update_user_variables}, headers=headers)
print("Response for updating user:", response.json())

response = requests.post(url, json={'query': delete_user_gql, 'variables': delete_user_variables}, headers=headers)
print("Response for deleting user:", response.json())

response = requests.post(url, json={'query': create_contract_gql, 'variables': create_contract_variables}, headers=headers)
print("Response for creating contract:", response.json())

response = requests.post(url, json={'query': get_contract_gql, 'variables': get_contract_variables}, headers=headers)
print("Response for getting contract:", response.json())

response = requests.post(url, json={'query': get_contract_withoutnested_gql, 'variables': get_contract_variables}, headers=headers)
print("Response for getting contract without nested fields:", response.json())

response = requests.post(url, json={'query': get_contracts_by_user_gql, 'variables': {"user_id": "1"}}, headers=headers)
print("Response for getting contracts by user:", response.json())

response = requests.post(url, json={'query': delete_contract_gql, 'variables': {"id": "1"}}, headers=headers)
print("Response for deleting contract:", response.json())
