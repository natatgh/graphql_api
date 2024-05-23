# app.py
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from database import init_db

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

@app.before_first_request
def setup():
    init_db()

if __name__ == '__main__':
    app.run()
