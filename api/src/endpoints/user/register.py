import json
from dataclasses import asdict
from flask_restx import Resource, reqparse, Namespace, inputs

from src import service, log
from src.models.user import User
from src.packages.response.user_message import UserMessage
from src.validators.user.register import RegistrationValidator
from src.packages.authentication.authenticator import Authentication


register_namespace = Namespace('register', description='Registration.')

register_parser = reqparse.RequestParser()
register_parser.add_argument('email', type=inputs.regex(pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'), required=True, help='Wrong email format.')
register_parser.add_argument('user_name', type=inputs.regex(pattern=r'[0-9a-zA-Z_.]{4,48}'), required=True, help='Username contains unsupported characters. Tip: Min characters: 4, Max cahracters: 48, Unsupported characters: !@#$%^&*()-=+')
register_parser.add_argument('password', type=str, required=True, help='Wrong password passed.')
register_parser.add_argument('repeat_password', type=str, required=True, help='Wrong password passed.')


@register_namespace.route('/')
class Registration(Resource):
    '''
        A registration class, that is used for during the registration form.
    '''

    @service.api.expect(register_parser)
    def post(self) -> tuple[dict[str, int|str], int]:
        '''
            Registrates new user.
        '''

        arguments = register_parser.parse_args()
        user = User(
            _email=arguments.get('email', None),
            _username=arguments.get('user_name', None),
            _password=arguments.get('password', None)
        )
        user_message = UserMessage()

        if user._password != arguments.get('repeat_password', None):
            log.warning('The passwords does not match ...')
            user_message.add_message(new_message={'warning_message': 'The passwords does not match'})
            return user_message.return_message()

        if not RegistrationValidator().insert(user=user, user_message=user_message):
            return user_message.return_message()

        if not Authentication().create_user(username=user._username, password=user._password):
            log.error(f'Authentication failed for username "{user._username}" ...')
            return 'Unfortunately registration failed. Please try again later or contact our support team.', 400

        log.info(f'New user with username "{user._username}" registered ...')
        return 'You have completed the registration successfully', 200