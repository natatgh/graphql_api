from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from schema import schema
from database import db_session, init_db
from auth import validate_api_token, authenticate_user, validate_api_key

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
        token = request.headers.get('Authorization')
        api_key = request.headers.get('X-API-KEY')
        
        if not token and not api_key:
            return jsonify({"message": "Missing Authentication Token or API Key"}), 401
        
        if token:
            user_id = validate_api_token(token)
            if not user_id:
                return jsonify({"message": "Invalid Authentication Token"}), 401
        
        if api_key:
            if not validate_api_key(api_key):
                return jsonify({"message": "Invalid API Key"}), 401
        
        return super().dispatch_request()

app.add_url_rule('/graphql', view_func=AuthGraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
