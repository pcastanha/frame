from flask import Flask
from flask import jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api

from softframe.rest.endpoints import Endpoints

__version__ = "0.1.0"

# Flask configurations
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'pedro':
        return 'python'
    return None


@auth.error_handler
def unauthorized(self):
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


def create_app():
    app = Flask(__name__, static_url_path="")
    api = Api(app)
    register_endpoints(api)
    return app


def register_endpoints(api):
    # Endpoint declarations
    for endpoint in Endpoints:
        api.add_resource(endpoint.value['class'], endpoint.value['route'], endpoint=endpoint.value['endpoint'])

    return None


def main():
    app = create_app()
    app.run(host='0.0.0.0', debug=True)

if __name__ == '__main__':
    main()
