from enum import Enum, unique

from flask import abort
from flask_restful import Resource, reqparse, fields, marshal

from softframe.misc.routines import classify_paragraphs

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}


class TaskAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task[0], task_fields)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, task_fields)}

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}


class TaskListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return {'tasks': [marshal(task, task_fields) for task in tasks]}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        return {'task': marshal(task, task_fields)}, 201


class ClassifierAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('document', type=str, required=True, help="No document provided.", location='json')
        self.reqparse.add_argument('convert', type=bool, required=False, default=False, location='json')
        self.reqparse.add_argument('paragraph', type=bool, required=False, default=True, location='json')
        super(ClassifierAPI, self).__init__()

    def post(self):  # TODO: paragraph bool flag not working properly.
        args = self.reqparse.parse_args()
        if args['convert'] is False:
            if args['paragraph'] is True:
                response = classify_paragraphs(args['document'])
            else:
                response = classify_paragraphs(args['document'], use_paragraph=True)
        else:
            raise NotImplementedError

        return response


@unique
class Endpoints(Enum):
    TASK = {"class": TaskAPI, "route": "/todo/api/v1.0/tasks/<int:id>", "endpoint": "task"}
    TASKLIST = {"class": TaskListAPI, "route": "/todo/api/v1.0/tasks", "endpoint": "tasks"}
    CLASSIFIER = {"class": ClassifierAPI, "route": "/ml/api/v1.0/classify", "endpoint": "classify"}
