from flask import Flask
from flask_graphql import GraphQLView
from .schemas import schema

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )


    return app