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
    user = graphene.Field(lambda: User)
    created_at = graphene.String()
    fidelity = graphene.Int()
    amount = graphene.Float()
    id = graphene.ID()

class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.ID(required=True))
    contracts = graphene.List(Contract)
    contract = graphene.Field(Contract, id=graphene.ID(required=True))
    get_contract = graphene.Field(GetContract, id=graphene.ID(required=True))
    getContractsByUser = graphene.List(GetContract, userId=graphene.ID(required=True))

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
            user = UserModel.query.get(contract.user_id)
            if user:
                return GetContract(
                    contract_id=contract.id,
                    description=contract.description,
                    user=user,
                    created_at=contract.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    fidelity=contract.fidelity,
                    amount=contract.amount,
                    id=contract.id
                )
        return None

    def resolve_getContractsByUser(self, info, userId):
        contracts = ContractModel.query.filter_by(user_id=userId).all()
        return [
            GetContract(
                contract_id=contract.id,
                description=contract.description,
                user=UserModel.query.get(contract.user_id),
                created_at=contract.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                fidelity=contract.fidelity,
                amount=contract.amount,
                id=contract.id
            ) for contract in contracts
        ]
