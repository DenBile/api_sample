import json
from dataclasses import asdict
from flask_restx import Resource, reqparse, Namespace, inputs

from src import service, log

sample_namespace = Namespace('sample', description='A sample API.')
# TODO: Load cache.

query_sample_parser = reqparse.RequestParser()
query_sample_parser.add_argument('strict_search', type=inputs.boolean, default=False, required=True, help='Strict search is a boolean, accepts only True/False. Wrong value passed.')
query_sample_parser.add_argument('first_name', type=inputs.regex(pattern=r'^[A-Z][a-z]'), trim=True, required=True, help='Wrong name passed.')

@sample_namespace.route('/query/')
class QuerySample(Resource):
    '''
        A query sample ...
    '''

    # TODO: auth, audit
    # @service.audit.write
    # @service.auth.restrict
    @service.api.expect(query_sample_parser)
    def get(self) -> tuple[dict[str, int|str], int]:
        '''
        '''

        pass

insert_sample_parser = reqparse.RequestParser()
insert_sample_parser.add_argument('strict_search', type=inputs.boolean, default=False, required=True, help='Strict search is a boolean, accepts only True/False. Wrong value passed.')
insert_sample_parser.add_argument('first_name', type=inputs.regex(pattern=r'^[A-Z][a-z]'), trim=True, required=True, help='Wrong name passed.')

@sample_namespace.route('/insert/')
class InsertSample(Resource):
    '''
        A insert sample ...
    '''

    # @service.audit.write
    # @service.auth.restrict
    @service.api.expect(insert_sample_parser)
    def post(self) -> tuple[dict[str, int|str], int]:
        '''
        '''

        pass

update_sample_parser = reqparse.RequestParser()
update_sample_parser.add_argument('strict_search', type=inputs.boolean, default=False, required=True, help='Strict search is a boolean, accepts only True/False. Wrong value passed.')
update_sample_parser.add_argument('first_name', type=inputs.regex(pattern=r'^[A-Z][a-z]'), trim=True, required=True, help='Wrong name passed.')

@sample_namespace.route('/update/')
class UpdateSample(Resource):
    '''
        A update sample ...
    '''

    # @service.audit.write
    # @service.auth.restrict
    @service.api.expect(update_sample_parser)
    def put(self) -> tuple[dict[str, int|str], int]:
        '''
        '''

        pass

delete_sample_parser = reqparse.RequestParser()
delete_sample_parser.add_argument('strict_search', type=inputs.boolean, default=False, required=True, help='Strict search is a boolean, accepts only True/False. Wrong value passed.')
delete_sample_parser.add_argument('first_name', type=inputs.regex(pattern=r'^[A-Z][a-z]'), trim=True, required=True, help='Wrong name passed.')

@sample_namespace.route('/delete/')
class DeleteSample(Resource):
    '''
        A delete sample ...
    '''

    # @service.audit.write
    # @service.auth.restrict
    @service.api.expect(delete_sample_parser)
    def delete(self) -> tuple[dict[str, int|str], int]:
        '''
        '''

        pass
