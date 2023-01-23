import sqlite3
import pandas as pd

from packages.databases.sql_lite_package.sql_lite_tables import SQLiteTable
from packages.databases.sql_lite_package.sql_lite_queries import SQLiteQuery
from packages.databases.database import Database, DatabaseReturn

class SQLiteConnection(Database):
    '''
        Custom SQLite connection class.
    '''

    def __init__(self, database: str) -> None:
        '''
            Default constructor.
        '''

        self.database = database
        self.database_type = 'SQLite'

        self._database_connection = None
    
    def _connect(self):
        '''
            Establish connection against SQLite database.
        '''

        try:
            print(self.database)
            self._log.info(f'Establishing connection ... Database: {self.database}')
            self._database_connection = sqlite3.connect(database=self.database)
        except sqlite3.Error as sql_db_exception:
            self._log.error(f'Exception occured while establishing SQLite connection agains {self.database} database.')
            self._log.error(sql_db_exception)
            raise Exception(sql_db_exception)
    
    def _disconnect(self) -> None:
        '''
            Closing the connection against SQLite database.
        '''

        self._log.info(f'Disconnecting from {self.database}')
        self._database_connection.close()
        self._database_connection = None

    def _is_not_bulk_insert(self, properties: list[int|str|tuple[str|int]]) -> bool:
        '''
            Checks whether any of the passed parameters is string.
        '''

        return any( [ isinstance(value, str) for value in properties ] )

    def _execute(self, sql: str, properties: list[int|str|tuple[int|str]]) -> tuple[pd.DataFrame, str]:
        '''
            Execute SQLite query.
        '''

        bulk = not self._is_not_bulk_insert(properties=properties)
        query = SQLiteQuery(
            sql=sql, properties=properties, _query_type = self._query_type
        )

        try:
            self._log.info('Opening cursor against the Database ...')
            _cursor = self._database_connection.cursor()

            if bulk and self._query_type != 'SELECT':
                self._database_connection.start_transaction()
                self._log.info('Transaction started ...')
            
            db_data = query.execute(cursor=_cursor, bulk=bulk)
            if self._query_type == 'SELECT':
                return DatabaseReturn(rows=db_data[0], columns=db_data[1], database=self.database, database_type=self.database_type)
            
            db_data = DatabaseReturn(rows=pd.DataFrame(), columns=(), database=self.database, database_type=self.database_type)
            self._database_connection.commit()
            self._log.info('Transaction has been commited ...')
        except sqlite3.Error as mysql_exception:
            self._log.error('Unexpected exception occured while executing user\'s query ...')
            self._log.error(mysql_exception)

            db_data = DatabaseReturn(rows=pd.DataFrame(), columns=(), database=self.database, database_type=self.database_type)
            if bulk and self._query_type != 'SELECT':
                self._log.warning('Rolling back ...')
                self._database_connection.rollback()
        finally:
            self._log.info('Closing cursor ...')
            _cursor.close()

        return db_data

    def _amend_table(self, sql: str) -> None:
        '''
            Execute SQLite query to insert/drop table
        '''

        pass

    @property
    def _is_connected(self) -> bool:
        '''
            Checks if connection is established.
        '''

        if self._database_connection:
            return True

        self._log.warning(f'No connection established against {self.database}.')
        return False