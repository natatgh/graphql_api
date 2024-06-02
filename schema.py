import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User as UserModel, Contract as ContractModel
from database import db_session
import datetime

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class ContractType(SQLAlchemyObjectType):
    class Meta:
        model = ContractModel

class UserExistsError(graphene.ObjectType):
    message = graphene.String()
    user_name = graphene.String()

class CreateUserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)

class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)

    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    error = graphene.Field(UserExistsError)

    def mutate(self, info, input):
        existing_user = UserModel.query.filter_by(email=input.email).first()
        if existing_user:
            print("User with email already exists:", input.email)
            return CreateUser(
                id=None,
                name=None,
                email=None,
                error=UserExistsError(
                    message='User with this email already exists.',
                    user_name=existing_user.name
                )
            )
        
        print("Creating new user:", input.name)
        user = UserModel(name=input.name, email=input.email)
        db_session.add(user)
        db_session.commit()
        
        return CreateUser(
            id=user.id,
            name=user.name,
            email=user.email,
            error=None
        )

class UpdateUserInput(graphene.InputObjectType):
    name = graphene.String()
    email = graphene.String()

class UserUpdateError(graphene.ObjectType):
    message = graphene.String()

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateUserInput(required=True)

    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    error = graphene.Field(UserUpdateError)

    def mutate(self, info, id, input):
        user = UserModel.query.get(id)
        if not user:
            return UpdateUser(
                id=None,
                name=None,
                email=None,
                error=UserUpdateError(
                    message='User not found.'
                )
            )
        
        if input.name:
            user.name = input.name
        if input.email:
            user.email = input.email
        
        db_session.commit()
        
        return UpdateUser(
            id=user.id,
            name=user.name,
            email=user.email,
            error=None
        )
    
class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        user = UserModel.query.get(id)
        if not user:
            return DeleteUser(success=False, message="User not found.")

        contracts = ContractModel.query.filter_by(user_id=id).all()
        for contract in contracts:
            db_session.delete(contract)

        db_session.delete(user)
        db_session.commit()
        
        return DeleteUser(success=True, message="User and associated contracts deleted successfully.")

class CreateContractInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    user_id = graphene.ID(required=True)
    created_at = graphene.String(required=True)
    fidelity = graphene.Int(required=True)
    amount = graphene.Float(required=True)

class CreateContract(graphene.Mutation):
    class Arguments:
        input = CreateContractInput(required=True)

    id = graphene.ID()
    description = graphene.String()
    user_id = graphene.ID()
    created_at = graphene.String()
    fidelity = graphene.Int()
    amount = graphene.Float()

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
        return CreateContract(
            id=contract.id,
            description=contract.description,
            user_id=contract.user_id,
            created_at=contract.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            fidelity=contract.fidelity,
            amount=contract.amount
        )

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

    contract = graphene.Field(ContractType)

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
    message = graphene.String()

    def mutate(self, info, id):
        contract = ContractModel.query.get(id)
        if contract:
            db_session.delete(contract)
            db_session.commit()
            return DeleteContract(success=True, message="Contract deleted successfully.")
        return DeleteContract(success=False, message="Contract not found.")

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

class Contract(graphene.ObjectType):
    id = graphene.ID()
    description = graphene.String()
    user_id = graphene.ID()
    created_at = graphene.String()
    fidelity = graphene.Int()
    amount = graphene.Float()

class ContractsResult(graphene.ObjectType):
    Contracts = graphene.List(Contract)
    nextToken = graphene.String()

class GetContract(graphene.ObjectType):
    contract_id = graphene.ID()
    description = graphene.String()
    user_id = graphene.ID()
    created_at = graphene.String()
    fidelity = graphene.Int()
    amount = graphene.Float()
    user = graphene.Field(User)

    def resolve_user(parent, info):
        return UserModel.query.get(parent.user_id)

class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.ID(required=True))
    contracts = graphene.List(Contract)
    contract = graphene.Field(Contract, id=graphene.ID(required=True))
    getContract = graphene.Field(GetContract, id=graphene.ID(required=True))
    getContractsByUser = graphene.Field(ContractsResult, user_id=graphene.ID(required=True))
    getUser = graphene.Field(User, id=graphene.ID(required=True))

    def resolve_users(self, info):
        return UserModel.query.all()

    def resolve_user(self, info, id):
        return UserModel.query.get(id)

    def resolve_contracts(self, info):
        return ContractModel.query.all()

    def resolve_contract(self, info, id):
        return ContractModel.query.get(id)

    def resolve_getContract(self, info, id):
        contract = ContractModel.query.get(id)
        if contract:
            return GetContract(
                contract_id=contract.id,
                description=contract.description,
                user_id=contract.user_id,
                created_at=contract.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                fidelity=contract.fidelity,
                amount=contract.amount
            )
        return None

    def resolve_getContractsByUser(self, info, user_id):
        Contracts = ContractModel.query.filter_by(user_id=user_id).all()
        nextToken = None  # You can implement your pagination token logic here
        return ContractsResult(Contracts=Contracts, nextToken=nextToken)
    
    def resolve_getUser(self, info, id):
        return UserModel.query.get(id)

class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()
    updateUser = UpdateUser.Field()
    deleteUser = DeleteUser.Field()
    createContract = CreateContract.Field()
    updateContract = UpdateContract.Field()
    deleteContract = DeleteContract.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
