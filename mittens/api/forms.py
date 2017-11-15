from flask_restplus import reqparse


create_log = reqparse.RequestParser()
create_log.add_argument('content', required=True, help='Provide a non-empty string')
create_log.add_argument('meta', type=dict)
