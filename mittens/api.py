from flask_restplus import Api

from mittens.logs.views import logs
from mittens.health.views import health

api = Api(
    title='Mittens API',
    version='1.0',
    description='API for handling error logs',
    prefix='/api/v1',
)

api.add_namespace(logs)
api.add_namespace(health)
