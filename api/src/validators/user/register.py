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

        pass