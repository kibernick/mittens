from flask import Blueprint
from flask_restplus import Api, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound

from mittens.logs.forms import create_log
from mittens.logs.models import ErrorLog
from mittens.db import db

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='Mittens API', description='API for handling error logs')

logs = api.namespace('logs', description='Record or query error logs.')
log_fields = {
    'id': fields.Integer(
        readOnly=True,
        description='The task unique identifier',
        example=1),
    'content': fields.String(
        description='Error message',
        required=True,
        min_length=1,
        example="Uncaught SyntaxError: Unexpected token <"),
    'meta': fields.Raw(
        description='Optional extra data',
        example={'browser': "Mozilla", 'url': "http://mylovelywebsite.com"})
}
error_log_new = logs.model('ErrorLogNew', {x: log_fields[x] for x in ('content', 'meta')})
error_log_full = logs.model('ErrorLog', {x: log_fields[x] for x in ('id', 'content', 'meta')})


@logs.route('/', endpoint='log-list')
class LogList(Resource):
    @logs.doc('list_logs')
    @logs.marshal_list_with(error_log_full)
    def get(self):
        """List all error logs."""
        # todo: list only the logs of the logged in user
        return ErrorLog.query.all()

    @logs.doc('create_log')
    @logs.expect(error_log_new)
    @logs.marshal_with(error_log_full, code=201)
    def post(self):
        """Create a new error log."""
        args = create_log.parse_args()
        if not args.get('content'):
            raise BadRequest("Input payload validation failed")

        record = ErrorLog(**args)
        db.session.add(record)
        db.session.commit()
        return record, 201


@logs.route('/<int:log_id>', endpoint='log-details')
class LogDetails(Resource):
    @logs.doc('get_log')
    @logs.marshal_with(error_log_full)
    def get(self, log_id):
        """Fetch a given resource."""
        record = ErrorLog.query.get(log_id)
        if record:
            return record, 200
        raise NotFound('Log not found')
