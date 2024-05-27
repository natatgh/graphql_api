import graphene
from models import User as UserModel, Contract as ContractModel
from database import db_session
import datetime
from queries import User, Contract  # Certifique-se de importar as definições corretas

class UserExistsError(graphene.ObjectType):
    message = graphene.String()

class CreateUserInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)

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
        
        return CreateUser(user=user, error=None)

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
            return UpdateUser(user=None)

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
    message = graphene.String()

    def mutate(self, info, id):
        contract = ContractModel.query.get(id)
        if contract:
            db_session.delete(contract)
            db_session.commit()
            return DeleteContract(success=True, message="Contract deleted successfully.")
        return DeleteContract(success=False, message="Contract not found.")

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_contract = CreateContract.Field()
    update_contract = UpdateContract.Field()
    delete_contract = DeleteContract.Field()
