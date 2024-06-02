import requests

# URL do seu servidor GraphQL
url = 'http://localhost:5000/graphql'

# Sua API Key
api_key = 'j2w9UHvP4bQz9g9V7vQ4tM6z2eK5tYx3'

# Headers para indicar que estamos enviando uma consulta GraphQL
headers = {'Content-Type': 'application/json'}

# Consultas e variáveis para criação, atualização, exclusão e obtenção de usuários e contratos
create_user_gql = """
mutation createUser($input: CreateUserInput!, $api_key: String!) {
  createUser(input: $input, api_key: $api_key) {
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
    },
    "api_key": api_key
}

get_user_gql = """
query getUser($id: ID!, $api_key: String!) {
  getUser(id: $id, api_key: $api_key) {
    id
    name
    email
  }
}
"""

get_user_variables = {
    "id": "1",
    "api_key": api_key
}

update_user_gql = """
mutation updateUser($id: ID!, $input: UpdateUserInput!, $api_key: String!) {
  updateUser(id: $id, input: $input, api_key: $api_key) {
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
    },
    "api_key": api_key
}

delete_user_gql = """
mutation deleteUser($id: ID!, $api_key: String!) {
  deleteUser(id: $id, api_key: $api_key) {
    success
    message
  }
}
"""

delete_user_variables = {
    "id": "1",
    "api_key": api_key
}

create_contract_gql = """
mutation createContract($input: CreateContractInput!, $api_key: String!) {
  createContract(input: $input, api_key: $api_key) {
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
    },
    "api_key": api_key
}

update_contract_gql = """
mutation updateContract($id: ID!, $input: UpdateContractInput!, $api_key: String!) {
  updateContract(id: $id, input: $input, api_key: $api_key) {
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
    },
    "api_key": api_key
}

get_contract_gql = """
query getContract($id: ID!, $api_key: String!) {
  getContract(id: $id, api_key: $api_key) {
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
    "id": "1",
    "api_key": api_key
}

get_contract_withoutnested_gql = """
query getContract($id: ID!, $api_key: String!) {
  getContract(id: $id, api_key: $api_key) {
    description
    user_id
    created_at
    fidelity
    amount
  }
}
"""

get_contracts_by_user_gql = """
query getContractsByUser($user_id: ID!, $api_key: String!) {
  getContractsByUser(user_id: $user_id, api_key: $api_key) {
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
    "user_id": "1",
    "api_key": api_key
}

delete_contract_gql = """
mutation deleteContract($id: ID!, $api_key: String!) {
  deleteContract(id: $id, api_key: $api_key) {
    success
    message
  }
}
"""

delete_contract_variables = {
    "id": "1",
    "api_key": api_key
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
