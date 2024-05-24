from flask import Flask
from flask_graphql import GraphQLView
import graphene
from models import User as UserModel
from schema import schema  # Importar seu schema GraphQL

app = Flask(__name__)

# class AuthMiddleware:
#     def resolve(self, next, root, info, **kwargs):
#         token = request.headers.get('Authorization')
#         if token:
#             user_id = verify_token(token)
#             if user_id:
#                 info.context.user = UserModel.query.get(user_id)
#             else:
#                 info.context.user = None
#         else:
#             info.context.user = None
#         return next(root, info, **kwargs)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        # middleware=[AuthMiddleware()]  # Comentado para desabilitar a autenticação
    )
)

if __name__ == '__main__':
    app.run()
