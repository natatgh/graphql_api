import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User as UserModel, Contract as ContractModel
from database import db_session

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Contract(SQLAlchemyObjectType):
    class Meta:
        model = ContractModel

class GetUser(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

class GetContract(graphene.ObjectType):
    contract_id = graphene.ID()
    description = graphene.String()
    user_id = graphene.ID()  # Alterado de 'user' para 'user_id'
    created_at = graphene.String()  # Alterado de 'created_at' para 'created_at'
    fidelity = graphene.Int()
    amount = graphene.Float()
    id = graphene.ID()

    def resolve_user_id(self, info):
        # Aqui você pode adicionar a lógica para resolver o ID do usuário, se necessário
        return self.user_id

    def resolve_created_at(self, info):
        # Aqui você pode adicionar a lógica para resolver a data de criação, se necessário
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None

class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.ID(required=True))
    contracts = graphene.List(Contract)
    contract = graphene.Field(Contract, id=graphene.ID(required=True))
    get_contract = graphene.Field(GetContract, id=graphene.ID(required=True))
    getContractsByUser = graphene.List(GetContract, user_id=graphene.ID(required=True))
    getUser = graphene.Field(User, id=graphene.ID(required=True))  # Adicionado

    def resolve_users(self, info):
        return UserModel.query.all()

    def resolve_user(self, info, id):
        return UserModel.query.get(id)

    def resolve_contracts(self, info):
        return ContractModel.query.all()

    def resolve_contract(self, info, id):
        return ContractModel.query.get(id)

    def resolve_get_contract(self, info, id):
        contract = ContractModel.query.get(id)
        if contract:
            return GetContract(
                contract_id=contract.id,
                description=contract.description,
                user_id=contract.user_id,  # Alterado de 'user' para 'user_id'
                created_at=contract.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Alterado de 'created_at' para 'created_at'
                fidelity=contract.fidelity,
                amount=contract.amount,
                id=contract.id
            )
        return None

    def resolve_getContractsByUser(self, info, user_id):
        contracts = ContractModel.query.filter_by(user_id=user_id).all()
        return [
            GetContract(
                contract_id=contract.id,
                description=contract.description,
                user_id=contract.user_id,
                created_at=contract.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                fidelity=contract.fidelity,
                amount=contract.amount,
                id=contract.id
            ) for contract in contracts
        ]
    
    # Método para obter um usuário por ID
    def resolve_getUser(self, info, id):
        return UserModel.query.get(id)
