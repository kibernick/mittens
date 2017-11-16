from flask import Blueprint
from flask_login import login_required, current_user
from flask_restplus import Api, Resource, fields
from flask_restplus.errors import abort
from werkzeug.exceptions import NotFound

from mittens.db import db
from mittens.logs.forms import create_log
from mittens.logs.models import ErrorLog

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='Mittens API', description='API for handling error logs')

logs = api.namespace('logs', description='Record or query error logs.')
log_fields = {'id': fields.Integer(readOnly=True, description='Log unique identifier', example=1),
              'content': fields.String(description='Error message', required=True, min_length=1,
                                       example="Uncaught SyntaxError: Unexpected token <"),
              'meta': fields.Raw(description='Optional extra data',
                                 example={'browser': "Mozilla", 'url': "http://mylovelywebsite.com"})}
error_log_new = logs.model('ErrorLogNew', {x: log_fields[x] for x in ('content', 'meta')})
error_log_full = logs.model('ErrorLog', {x: log_fields[x] for x in ('id', 'content', 'meta')})


@logs.route('', endpoint='log-list')
class LogList(Resource):
    @logs.doc('list_logs')
    @logs.header("Authorization", description="Tenant API key")
    @logs.marshal_list_with(error_log_full)
    @login_required
    def get(self):
        """List all error logs for the current tenant."""
        return ErrorLog.query.filter_by(tenant=current_user).all()

    @logs.doc('create_log')
    @logs.expect(error_log_new)
    @logs.header("Authorization", description="Tenant API key")
    @logs.marshal_with(error_log_full, code=201)
    @login_required
    def post(self):
        """Create a new error log."""
        args = create_log.parse_args()
        if not args.get('content'):
            abort(400,
                  message="Input payload validation failed",
                  errors={'content': "Provide a non-empty string"})
        record = ErrorLog(**args)
        record.tenant = current_user
        db.session.add(record)
        db.session.commit()
        return record, 201


@logs.route('/<int:log_id>', endpoint='log-details')
@logs.doc(params={'log_id': "Id of the error log"})
class LogDetails(Resource):
    @logs.doc('get_log')
    @logs.header("Authorization", description="Tenant API key")
    @logs.marshal_with(error_log_full)
    @login_required
    def get(self, log_id):
        """Fetch an error log by id, for the current tenant."""
        record = ErrorLog.query.filter_by(tenant=current_user, id=log_id).first()
        if record:
            return record, 200
        abort(404,
              message="Log not found")
