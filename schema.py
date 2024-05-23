import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User as UserModel, Contract as ContractModel
from database import db_session
import datetime

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
    id = graphene.ID()
    description = graphene.String()
    user = graphene.Field(GetUser)  # Usuário aninhado
    createdAt = graphene.String()
    fidelity = graphene.Int()
    amount = graphene.Float()

class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.ID(required=True))
    contracts = graphene.List(Contract)
    contract = graphene.Field(Contract, id=graphene.ID(required=True))
    get_contract = graphene.Field(GetContract, id=graphene.ID(required=True))  # Novo método para obter contrato com detalhes do usuário

    def resolve_users(self, info):
        return UserModel.query.all()

    def resolve_user(self, info, id):
        return UserModel.query.get(id)

    def resolve_contracts(self, info):
        return ContractModel.query.all()

    def resolve_contract(self, info, id):
        return ContractModel.query.get(id)

    def resolve_get_contract(self, info, id):  # Método para obter contrato com detalhes do usuário
        contract = ContractModel.query.get(id)
        if contract:
            return GetContract(
                id=contract.id,
                description=contract.description,
                user_id=contract.user_id,
                user=UserModel.query.get(contract.user_id),
                created_at=contract.created_at,
                fidelity=contract.fidelity,
                amount=contract.amount
            )
        return None 

class CreateUserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)

class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, input):
        existing_user = UserModel.query.filter_by(email=input.email).first()
        if existing_user:
            return CreateUser(user=None)
        user = UserModel(name=input.name, email=input.email)
        db_session.add(user)
        db_session.commit()
        return CreateUser(user=user)

class UpdateUserInput(graphene.InputObjectType):
    name = graphene.String()
    email = graphene.String()

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateUserInput()  # Mantendo o nome como "input" para corresponder ao esperado pelo servidor GraphQL

    user = graphene.Field(User)

    def mutate(self, info, id, input=None):
        user = UserModel.query.get(id)
        if not user:
            return UpdateUser(user=None)

        if input:
            if input.name:
                user.name = input.name
            if input.email:
                user.email = input.email

        db_session.commit()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        user = UserModel.query.get(id)
        if user:
            db_session.delete(user)
            db_session.commit()
            return DeleteUser(success=True, message="User deleted successfully.")
        else:
            return DeleteUser(success=False, message="User not found.")

class CreateContractInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    userId = graphene.ID(required=True)
    createdAt = graphene.String(required=True)
    fidelity = graphene.Int(required=True)
    amount = graphene.Float(required=True)

class CreateContract(graphene.Mutation):
    class Arguments:
        input = CreateContractInput(required=True)

    contract = graphene.Field(Contract)

    def mutate(self, info, input):
        created_at = datetime.datetime.strptime(input.createdAt, "%Y-%m-%dT%H:%M:%S")
        contract = ContractModel(
            description=input.description,
            user_id=input.userId,
            created_at=created_at,
            fidelity=input.fidelity,
            amount=input.amount
        )
        db_session.add(contract)
        db_session.commit()
        return CreateContract(contract=contract)

class UpdateContractInput(graphene.InputObjectType):
    description = graphene.String()
    userId = graphene.ID()
    createdAt = graphene.String()
    fidelity = graphene.Int()
    amount = graphene.Float()

class UpdateContract(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateContractInput(required=True)

    contract = graphene.Field(Contract)

    def mutate(self, info, id, input):
        contract = ContractModel.query.get(id)
        if not contract:
            return UpdateContract(contract=None)

        if input:
            if input.description:
                contract.description = input.description
            if input.userId:
                contract.user_id = input.userId
            if input.createdAt:
                contract.created_at = datetime.datetime.strptime(input.createdAt, "%Y-%m-%dT%H:%M:%S")
            if input.fidelity:
                contract.fidelity = input.fidelity
            if input.amount:
                contract.amount = input.amount

        db_session.commit()
        return UpdateContract(contract=contract)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()  # Renomeando para update_user
    delete_user = DeleteUser.Field()
    create_contract = CreateContract.Field()
    update_contract = UpdateContract.Field()  # Adicionando a atualização de contrato

schema = graphene.Schema(query=Query, mutation=Mutation)
