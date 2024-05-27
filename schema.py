import graphene
from mutations import Mutation
from queries import Query
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User as UserModel, Contract as ContractModel

schema = graphene.Schema(query=Query, mutation=Mutation)
