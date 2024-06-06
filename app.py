import os
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from schema import schema
from database import db_session, init_db
from auth import authenticate_user, validate_api_key

# Certifique-se de que o diretório /tmp exista
if not os.path.exists("/tmp"):
    os.makedirs("/tmp")

app = Flask(__name__)

@app.before_first_request
def setup():
    init_db()  # Inicializa o banco de dados e cria as tabelas

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.errorhandler(Exception)
def handle_error(e):
    response = jsonify({"message": str(e)})
    response.status_code = 500
    return response

class AuthGraphQLView(GraphQLView):
    def dispatch_request(self):
        api_key = request.headers.get('X-API-KEY')
        
        if not api_key or not validate_api_key(api_key):
            return jsonify({"message": "Invalid API Key"}), 403
        
        return super().dispatch_request()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if authenticate_user(email, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

app.add_url_rule(
    '/graphql',
    view_func=AuthGraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run(debug=True)
