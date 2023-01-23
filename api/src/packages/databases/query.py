from dataclasses import dataclass
from abc import ABC, abstractclassmethod

from packages.logging.logger import Logger
from .supported_options import SupportedQueryOptions

@dataclass
class Query(ABC):

    sql: str
    properties: list[int|str|tuple[int|str]]
    _query_type: str

    _log = Logger()
    
    def execute(self, cursor: object, bulk: bool) -> tuple:
        '''
            Identifies which query should be executed and executes it.
        '''
        
        return getattr(self, SupportedQueryOptions[self._query_type])(cursor=cursor, bulk=bulk) if self._query_type != 'SELECT' else getattr(self, SupportedQueryOptions[self._query_type])(cursor=cursor)


    @abstractclassmethod
    def select(self) -> tuple:
        '''
            Custom method to execute select queries in the database.
        '''

    @abstractclassmethod
    def insert(self) -> None:
        '''
            Custom method to execute insert queries in the database.
        '''

    @abstractclassmethod 
    def update(self) -> None:
        '''
            Custom method to execute update queries in the database.
        '''

    @abstractclassmethod
    def delete(self) -> None:
        '''
            Custom method to execute delete queries in the database.
        '''

# SupportedQueryOptions = {
#     'SELECT': 'select',
#     'INSERT': 'insert',
#     'UPDATE': 'update',
#     'DELETE': 'delete'
# }
