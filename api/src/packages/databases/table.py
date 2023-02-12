from dataclasses import dataclass
from abc import ABC, abstractclassmethod

from src.packages.logging.logger import Logger
from .supported_options import SupportedTableAmendmentOptions


@dataclass
class Table(ABC):

    sql: str
    _query_type: str

    _log = Logger()
    
    def execute(self, cursor: object) -> None:
        '''
            Identifies which query should be executed and executes it.
        '''
        
        getattr(self, SupportedTableAmendmentOptions[self._query_type])(cursor=cursor)


    @abstractclassmethod
    def create(self) -> None:
        '''
            Custom method to execute create tables in the database.
        '''
    
    @abstractclassmethod
    def drop(self) -> None:
        '''
            Custom method to execute drop tables in the database.
        '''
