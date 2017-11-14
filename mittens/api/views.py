from flask import Blueprint
from flask_restplus import Api, Resource


blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='Mittens API',
          description='API for handling error logs')
# api.model

logs = api.namespace('logs', description='Record or query error logs.')


@api.route('/hello', endpoint='hello-world')
class HelloWorld(Resource):
    def get(self):
        return {'hoi': "werld"}

#
# @logs.route('/', endpoint='log-list')
# class LogList(Resource):
#
