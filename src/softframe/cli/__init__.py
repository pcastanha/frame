'''from flask import Flask
from flask_restful import Api
from ml_api.api import TaskAPI, TaskListAPI

__version__ = "0.1.0"

# Flask configurations
app = Flask(__name__, static_url_path="")
api = Api(app)

# Endpoint declarations
api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint='task')'''

from .cli import main

__all__ = ['main']
