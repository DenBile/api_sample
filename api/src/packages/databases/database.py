import pandas as pd
from dataclasses import dataclass
from abc import ABC, abstractclassmethod

from src.packages.logging.logger import Logger
from .supported_options import SupportedQueryOptions, SupportedTableAmendmentOptions
# from query import SupportedQueryOptions
# from table import SupportedTableAmendmentOptions


@dataclass(slots=True, frozen=True)
class DatabaseReturn:
    '''
        A custom class that will group in one format the output from the databases.
    '''

    rows: pd.DataFrame
    columns: tuple[str]
    database: str
    database_type: str

    _log = Logger()

    def __post_init__(self) -> None:
        '''
            Transforms the data into dataframe.
        '''

        self._log.info(f'Query returned data ... \n{self.rows}') if isinstance(self.rows, pd.DataFrame) or self.rows else self._log.info('No data was returned from the query')
            
        if not isinstance(self.rows, pd.DataFrame):
            try:
                self._log.info('Returned data from the database is not in DataFrame format, will convert it into a DataFrame ...')
                object.__setattr__(self, 'rows', pd.DataFrame(data=self.rows, columns=self.columns))
                self._log.info('Rows have been successfully changed into a DataFrame ...')
                self._log.info(self.rows)
            except Exception as dataframe_conversion_exception:
                self._log.error('Unexpected error occured while converting given data into a DataFrame ...')
                self._log.error(dataframe_conversion_exception)

    @property
    def is_empty(self) -> bool:
        '''
            Checks if the returned output is emapty list.
        '''

        self._log.info('Checking if the output is empty ...')
        self._log.debug(f'Rows: {self.rows}')
        return True if not self.rows.empty else False


class Database(ABC):
    '''
        An abstract database method.
    '''

    _log = Logger()

    def __enter__(self):
        '''
            Allows to use "with" keyword to establish connection against the db.

            Arguments:
                None

            Returns:
                self
        '''

        self._connect()
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        '''
            Closes the connection against the db.
        '''

        if any( (exception_type, exception_value, traceback) ):
            self._log.error(f'Disconnected from the database due to an unexpected exception ...')
            self._log.error(f'Exception type: {exception_type}')
            self._log.error(f'Exception value: {exception_value}')
            self._log.error(f'Traceback: {traceback}')
        self._disconnect()


    def execute_query(self, sql: str, properties: list[int|str|tuple[int|str]] = []) -> DatabaseReturn:
        '''
            Executes user's SQL.        
        '''

        self._log.info('Preparing to execute the query ...')
        self._log.info(f'SQL: {sql}')
        if properties:
            self._log.info(f'Properties: {properties}')

        if not self._is_connected or not self._valid_query_option(sql=sql):
            return DatabaseReturn(rows=pd.DataFrame(), columns=(), database=self.database, database_type=self.database_type)

        return self._execute(sql=sql, properties=properties)
        
    def amend_table(self, sql: str) -> None:
        '''
            Executes user's SQL table insert/drop.
        '''

        self._log.info('Preparing to amend table ...')
        self._log.info(f'SQL: {sql}')
        if not self._is_connected or not self._valid_table_amendment_option(sql=sql):
            return DatabaseReturn(rows=pd.DataFrame(), columns=(), database=self.database, database_type=self.database_type)
        
        return self._amend_table(sql=sql)
        

    def _valid_query_option(self, sql: str) -> bool:
        '''
            Identifyies whether the selected option is available or not.
        '''

        for query_option in SupportedQueryOptions:
            if sql.strip().upper().startswith(query_option):
                self._log.info('Query type is supported ...')
                self._query_type = query_option
                return True
        
        self._log.warning('Selected type is not supported, please check your query and try again.')
        return False

    def _valid_table_amendment_option(self, sql: str) -> bool:
        '''
            Validates whether the selected option by user is supported as a table amendment.
        '''

        for query_option in SupportedTableAmendmentOptions:
            if sql.strip().upper().startswith(query_option):
                self._log.info('Table amendment type is supported ...')
                self._query_type = query_option
                return True
        
        self._log.warning('Selected type is not supported, please check your query and try again.')
        return False


    @abstractclassmethod
    def _connect(self):
        '''
            An abstract to establish the connection.
        '''

    @abstractclassmethod
    def _disconnect(self) -> None:
        '''
            An abstract to close the connection.
        '''

    @abstractclassmethod
    def _is_connected(self) -> None:
        '''
            Checks if connection is present, in case it's not throw an exception.
        '''

    @abstractclassmethod
    def _execute(self) -> DatabaseReturn:
        '''
            Executes the query.
        '''

    @abstractclassmethod
    def _amend_table(self) -> None:
        '''

        '''
