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

class CreateUserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)

class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)

    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    message = graphene.String()

    def mutate(self, info, input):
        try:
            existing_user = UserModel.query.filter_by(email=input.email).first()
            if existing_user:
                return CreateUser(
                    id=None,
                    name=None,
                    email=None,
                    message=f"User with this email already exists: {existing_user.name}"
                )
            
            user = UserModel(name=input.name, email=input.email)
            db_session.add(user)
            db_session.commit()

            db_session.refresh(user)

            return CreateUser(
                id=user.id,
                name=user.name,
                email=user.email,
                message="User created successfully"
            )
        except Exception as e:
            return CreateUser(
                id=None,
                name=None,
                email=None,
                message=f"An error occurred: {e}"
            )

class UpdateUserInput(graphene.InputObjectType):
    name = graphene.String()
    email = graphene.String()

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = UpdateUserInput(required=True)

    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    message = graphene.String()

    def mutate(self, info, id, input):
        try:
            user = UserModel.query.get(id)
            if not user:
                return UpdateUser(
                    id=None,
                    name=None,
                    email=None,
                    message='User not found.'
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
                message="User updated successfully"
            )
        except Exception as e:
            return UpdateUser(
                id=None,
                name=None,
                email=None,
                message=f"An error occurred: {e}"
            )

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            user = UserModel.query.get(id)
            if not user:
                return DeleteUser(success=False, message="User not found.")
            
            contracts = ContractModel.query.filter_by(user_id=id).all()
            if contracts:
                return DeleteUser(success=False, message="User has associated contracts and cannot be deleted.")

            db_session.delete(user)
            db_session.commit()
            
            return DeleteUser(success=True, message="User deleted successfully.")
        except Exception as e:
            return DeleteUser(success=False, message=f"An error occurred: {e}")

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
    message = graphene.String()

    def mutate(self, info, input):
        try:
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
                amount=contract.amount,
                message="Contract created successfully"
            )
        except Exception as e:
            return CreateContract(
                id=None,
                description=None,
                user_id=None,
                created_at=None,
                fidelity=None,
                amount=None,
                message=f"An error occurred: {e}"
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
    message = graphene.String()

    def mutate(self, info, id, input):
        try:
            contract = ContractModel.query.get(id)
            if not contract:
                return UpdateContract(contract=None, message="Contract not found.")

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
            return UpdateContract(contract=contract, message="Contract updated successfully")
        except Exception as e:
            return UpdateContract(contract=None, message=f"An error occurred: {e}")

class DeleteContract(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            contract = ContractModel.query.get(id)
            if not contract:
                return DeleteContract(success=False, message="Contract not found.")
            
            db_session.delete(contract)
            db_session.commit()
            return DeleteContract(success=True, message="Contract deleted successfully.")
        except Exception as e:
            return DeleteContract(success=False, message=f"An error occurred: {e}")

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
        try:
            return UserModel.query.all()
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def resolve_user(self, info, id):
        try:
            return UserModel.query.get(id)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def resolve_contracts(self, info):
        try:
            return ContractModel.query.all()
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def resolve_contract(self, info, id):
        try:
            return ContractModel.query.get(id)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def resolve_getContract(self, info, id):
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def resolve_getContractsByUser(self, info, user_id):
        try:
            contracts = ContractModel.query.filter_by(user_id=user_id).all()
            nextToken = None  # Implementação da lógica de paginação, se necessário
            return ContractsResult(Contracts=contracts, nextToken=nextToken)
        except Exception as e:
            print(f"An error occurred: {e}")
            return ContractsResult(Contracts=[], nextToken=None)
    
    def resolve_getUser(self, info, id):
        try:
            return UserModel.query.get(id)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()
    updateUser = UpdateUser.Field()
    deleteUser = DeleteUser.Field()
    createContract = CreateContract.Field()
    updateContract = UpdateContract.Field()
    deleteContract = DeleteContract.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
