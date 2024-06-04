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

# Parâmetros para a consulta de criação de usuario
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

# Atualização de Usuário
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
    id
    description
    user_id
    created_at
    fidelity
    amount
  }
}
"""

# Parâmetros para a consulta de criação de contrato
create_contract_variables = {
  "input": {
      "description": "New Contract",
      "user_id": "1",  # ID do usuário associado ao contrato
      "created_at": "2024-05-22T00:00:00",  # Formato ISO 8601
      "fidelity": 5,
      "amount": 1000.00
  }
}

# Consulta para atualizar um contrato por ID
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

# Parâmetros para a consulta de atualização de contrato
update_contract_variables = {
    "id": "1",  # ID do contrato que você deseja atualizar
    "input": {
        "description": "Updated Contract",
        "user_id": "1",  # ID do usuário associado ao contrato
        "created_at": "2024-05-22T00:00:00",  # Formato ISO 8601
        "fidelity": 10,
        "amount": 2000.00
    }
}

# Consulta para obter um contrato por ID
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

# Parâmetros para a consulta de obtenção de contrato por ID
get_contract_variables = {
    "id": "1"  # ID do contrato que você deseja obter
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

# Consulta para obter contratos por ID de usuário
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

# Parâmetros para a consulta de obtenção de contratos por ID de usuário
get_contracts_by_user_variables = {
    "user_id": "1"  # ID do usuário que você deseja obter os contratos
}

# Consulta para excluir um contrato
delete_contract_gql = """
mutation deleteContract($id: ID!) {
  deleteContract(id: $id) {
    success
    message
  }
}
"""

# Parâmetros para a consulta de exclusão de contrato
delete_contract_variables = {
    "id": "1"  # ID do contrato que você deseja excluir
}

# Função para executar as consultas usando requests
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
