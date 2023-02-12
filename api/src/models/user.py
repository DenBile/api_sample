import re
from dataclasses import dataclass
from abc import ABC, abstractclassmethod

from src import log

@dataclass
class User(ABC):
    '''
        An abstract class of a user.
    '''

    _username: str
    _email: str
    _password: str


    @property
    def is_valid_username(self) -> bool:
        '''
            Checks if the user name is a valid username.
        '''

        if len(self._username) < 4:
            log.error(f'"{self._username}" is not a valid username. To short.')
            return False

        if len(self._username) > 48:
            log.error(f'"{self._username}" is not a valid username. To long.')
            return False

        if not re.match(pattern=r'^[0-9a-zA-Z_.]{4,48}', string=self._username):
            log.error(f'"{self._username}" is not a valid username. Doesn\'t match the regex pattern.')
            return False
        
        log.debug(f'"{self._username}" is valid username.')
        return True

    @property
    def is_valid_email(self) -> bool:
        '''
            Check if the email is valid.
        '''

        if not re.fullmatch(pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', string=self._email):
            log.error(f'"{self._email}" is not valid email address.')
            return False
        
        log.debug(f'"{self._email}" is valid email address.')
        return True


@dataclass
class AuthenticatedUser(User):
    '''
        A custom class for an authenticated user.
    '''

    _authenticated: bool = False


    @property
    def is_authenticated(self) -> bool:
        '''
            Check if user is authenticated.
        '''

        return self._authenticated == True