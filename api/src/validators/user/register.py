from dataclasses import dataclass

from src import service, log
from src.models.user import User
from src.packages.response.user_message import UserMessage

@dataclass
class RegistrationValidator:
    '''
        A registration validator class.
    '''

    def insert(self, user: User, user_message: UserMessage) -> bool:
        '''
            ...
        '''

        if not user.is_valid_email:
            user_message.add_message(new_message={'error_message': 'Invalid email address.'})
            return False
        
        if not user.is_valid_username:
            user_message.add_message(new_message={'error_message': 'Invalid username address.'})
            return False
        
        if not user.unique_username():
            user_message.add_message(new_message={'error_message': 'This username is already ocupated, please select a different one ...'})
            return False

        return True