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
    contract_id = graphene.ID()  # Rename to contract_id to avoid conflict with the 'id' field
    description = graphene.String()
    user = graphene.Field(GetUser)
    created_at = graphene.String()
    fidelity = graphene.Int()
    amount = graphene.Float()
    id = graphene.ID()  # Include the 'id' field

class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.ID(required=True))
    contracts = graphene.List(Contract)
    contract = graphene.Field(Contract, id=graphene.ID(required=True))
    get_contract = graphene.Field(GetContract, id=graphene.ID(required=True))  # Novo método para obter contrato com detalhes do usuário
    getContractsByUser = graphene.List(GetContract, userId=graphene.ID(required=True))  # Use 'userId' instead of 'user_id'

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
                    created_at=datetime.strftime(contract.created_at, "%Y-%m-%d %H:%M:%S"),
                    fidelity=contract.fidelity,
                    amount=contract.amount
                )
        return None

    def resolve_getContractsByUser(self, info, userId):  # Use 'userId' instead of 'user_id'
        contracts = ContractModel.query.filter_by(user_id=userId).all()
        return [GetContract(
                    contract_id=contract.id,
                    description=contract.description,
                    user=UserModel.query.get(contract.user_id),
                    created_at=datetime.strftime(contract.created_at, "%Y-%m-%d %H:%M:%S"),
                    fidelity=contract.fidelity,
                    amount=contract.amount,
                    id=contract.id  # Include the 'id' field
                ) for contract in contracts]

class CreateUserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)

class UserExistsError(graphene.ObjectType):
    message = graphene.String()

class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)

    user = graphene.Field(User)
    error = graphene.Field(UserExistsError)

    def mutate(self, info, input):
        existing_user = UserModel.query.filter_by(email=input.email).first()
        if existing_user:
            return CreateUser(error=UserExistsError(message='User with this email already exists.'))
        
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
        input = UpdateUserInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, id, input):
        user = UserModel.query.get(id)
        if not user:
            return UpdateUser(user=None)  # Return without raising an exception, indicating the user was not found.

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
    user_id = graphene.ID(required=True)
    created_at = graphene.String(required=True)
    fidelity = graphene.Int(required=True)
    amount = graphene.Float(required=True)

class CreateContract(graphene.Mutation):
    class Arguments:
        input = CreateContractInput(required=True)

    contract = graphene.Field(Contract)

    def mutate(self, info, input):
        created_at = datetime.datetime.strptime(input.created_at, "%Y-%m-%dT%H:%M:%S")
        contract = ContractModel(
            description=input.description,
            user_id=input.user_id,
            created_at=created_at,
            fidelity=input.fidelity,
            amount=input.amount
        )
        db_session.add(contract)
        db_session.commit()
        return CreateContract(contract=contract)

class UpdateContractInput(graphene.InputObjectType):
    description = graphene.String()
    user_id = graphene.ID()
    created_at = graphene.String()
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
            if input.user_id:
                contract.user_id = input.user_id
            if input.created_at:
                contract.created_at = datetime.datetime.strptime(input.created_at, "%Y-%m-%dT%H:%M:%S")
            if input.fidelity:
                contract.fidelity = input.fidelity
            if input.amount:
                contract.amount = input.amount

        db_session.commit()
        return UpdateContract(contract=contract)

class DeleteContract(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()  # Adicionando o campo message

    def mutate(self, info, id):
        contract = ContractModel.query.get(id)
        if contract:
            db_session.delete(contract)
            db_session.commit()
            return DeleteContract(success=True, message="Contract deleted successfully.")  # Retornando uma mensagem descritiva
        return DeleteContract(success=False, message="Contract not found.")  # Retornando uma mensagem descritiva

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_contract = CreateContract.Field()
    update_contract = UpdateContract.Field()
    delete_contract = DeleteContract.Field()  # Adicione a mutação de exclusão de contrato

schema = graphene.Schema(query=Query, mutation=Mutation)
