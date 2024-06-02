from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from schema import schema
from database import db_session
from auth import generate_api_token, validate_api_token

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.errorhandler(Exception)
def handle_error(e):
    response = jsonify({"message": str(e)})
    response.status_code = 500
    return response

@app.route('/generate_token', methods=['POST'])
def generate_token():
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    token = generate_api_token(user_id)
    return jsonify({"token": token})

class AuthGraphQLView(GraphQLView):
    def dispatch_request(self):
        api_key = request.headers.get('Authorization')
        if not api_key or not validate_api_token(api_key):
            return jsonify({"message": "Invalid API Key"}), 403
        return super().dispatch_request()

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
