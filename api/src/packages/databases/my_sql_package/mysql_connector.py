import os
import pandas as pd
import mysql.connector as mysql

try:
    from mysql_tables import MySQLTable
    from mysql_queries import MySQLQuery
    from database import Database, DatabaseReturn
except Exception as exception_message:
    print('Unexpected error occured while loading modules ...')
    import add_upper_dir
    print('Loaded modules ... retrying to import ...')
    from mysql_tables import MySQLTable
    from mysql_queries import MySQLQuery
    from database import Database, DatabaseReturn
    

class MySqlConnection(Database):
    '''
        Custom mysql connection class.
    '''


    def __init__(self, host: str, password: str, database: str, user: str = os.system('whoami'),) -> None:
        '''
            Default constructor.
        '''

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.database_type = 'MySQL'

        self._database_connection = None
    
    def _connect(self):
        '''
            Establish connection against MySQL database.
        '''

        try:
            self._log.info(f'Establishing connection ... Host: {self.host}\tUser: {self.user}\tPassword: {self.password}\tDatabase: {self.database}')
            self._database_connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        except mysql.Error as sql_db_exception:
            self._log.error(f'Exception occured while establishing MySQL connection agains {self.database} database on {self.host} host.')
            self._log.error(sql_db_exception)
            raise Exception(sql_db_exception)
    
    def _disconnect(self) -> None:
        '''
            Closing the connection against MySQL database.
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
            Execute MySQL query.
        '''

        bulk = not self._is_not_bulk_insert(properties=properties)
        query = MySQLQuery(
            sql=sql, properties=properties, _query_type = self._query_type
        )
        
        try:
            self._log.info('Opening cursor against the Database ...')
            _cursor = self._database_connection.cursor(prepared=True)

            if bulk and self._query_type != 'SELECT':
                self._database_connection.start_transaction()
                self._log.info('Transaction started ...')
            
            db_data = query.execute(cursor=_cursor, bulk=bulk)
            if self._query_type == 'SELECT':
                return DatabaseReturn(rows=db_data[0], columns=db_data[1], database=self.database, database_type=self.database_type)
            
            db_data = DatabaseReturn(rows=pd.DataFrame(), columns=(), database=self.database, database_type=self.database_type)
            self._database_connection.commit()
            self._log.info('Transaction has been commited ...')
        except mysql.Error as mysql_exception:
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
            Execute MySQL query to insert/drop table
        '''

        table = MySQLTable(
            sql=sql, _query_type = self._query_type
        )

        try:
            self._log.info('Opening cursor against the Database ...')
            _cursor = self._database_connection.cursor(prepared=True)

            table.execute(cursor=_cursor)
            self._database_connection.commit()
            self._log.info('Transaction has been commited ...')
        except mysql.Error as mysql_exception:
            self._log.error('Unexpected exception occured while executing user\'s query ...')
            self._log.error(mysql_exception)

        finally:
            self._log.info('Closing cursor ...')
            _cursor.close()

        return
        
    @property
    def _is_connected(self) -> bool:
        '''
            Checks if connection is established.
        '''

        if self._database_connection:
            return True

        self._log.warning(f'No connection established against {self.database}.')
        return False


def main():
    '''
        Main function.
    '''

    # log = Logger(console=True)
    # Connection data
    HOST = 'localhost'
    USER = '***'
    PASSWORD = '***'
    DATABASE = 'photovoltaic'

    # Queries
    SELECT_QUERY_EXAMPLE = 'SELECT * FROM actor'
    SELECT_QUERY_WITH_PARAMS_EXAMPLE = 'SELECT * FROM actor WHERE first_name LIKE ?'
    SELECT_QUERY_PARAMS_EXAMPLE = [
        'Denys'# ,
        # 'Nefeli'
        ]
    # INSERT_QUERY_EXAMPLE = 'INSERT INTO hello (a, b, c) VALUES (?, ?, ?)'
    INSERT_QUERY_EXAMPLE = 'INSERT INTO actor (first_name, last_name) VALUES (?, ?)'
    # INSERT_QUERY_PARAMS_EXAMPLE = ['Denys', 'Biletskyy']
    INSERT_QUERY_PARAMS_EXAMPLE = [
        ('Denys', 'Biletskyy'),
        ('Nefeli', 'Konstantinou')
        ]
    UPDATE_QUERY_EXAMPLE = 'UPDATE actor SET actor_id = ? WHERE actor_id LIKE ?'
    UPDATE_QUERY_PARAMS_EXAMPLE = [
        (201, 202),
        # (202, 20044),
        # (203, 20043),
        # (204, 20045),
        ]
    DELETE_QUERY_EXAMPLE = 'DELETE FROM actor WHERE first_name LIKE ?'
    DELETE_QUERY_PARAMS_EXAMPLE = [
        ('Denys',),
        ('Nefeli',)
        ]
    # Tables
    CREATE_TABLE_EXAMPLE = '''
    CREATE TABLE IF NOT EXISTS hello (
        id SERIAL PRIMARY KEY,
        a VARCHAR(16),
        b VARCHAR(16),
        c VARCHAR(16)
    )
    '''
    DROP_TABLE_EXAMPLE = 'DROP TABLE hello'
    
    # print('*****\t****\t***\t**\t*\t**\t***\t****\t*****')
    # log.info('Opening connection')
    with MySqlConnection(
        host=HOST, user=USER, password=PASSWORD, database=DATABASE
    ) as db:
    #     log.info('Connection established')
        db_data = db.execute_query(sql=SELECT_QUERY_WITH_PARAMS_EXAMPLE, properties=SELECT_QUERY_PARAMS_EXAMPLE)
        print(db_data)
        # db_data = db.execute_query(sql=SELECT_QUERY_EXAMPLE)
        # db.execute_query(sql=INSERT_QUERY_EXAMPLE, properties=INSERT_QUERY_PARAMS_EXAMPLE)
        # db.execute_query(sql=UPDATE_QUERY_EXAMPLE, properties=UPDATE_QUERY_PARAMS_EXAMPLE)
        # db.execute_query(sql=DELETE_QUERY_EXAMPLE, properties=DELETE_QUERY_PARAMS_EXAMPLE)
        # print('=====\t====\t===\t==\t=\t==\t===\t====\t=====')
        # db.execute_query(sql=UPDATE_QUERY_EXAMPLE, properties=UPDATE_QUERY_PARAMS_EXAMPLE)
        # db_data = db.execute_query(sql=SELECT_QUERY_WITH_PARAMS_EXAMPLE, properties=SELECT_QUERY_PARAMS_EXAMPLE)
        # print(db_data.rows)
        # db.amend_table(sql=CREATE_TABLE_EXAMPLE)
        # db.amend_table(sql=DROP_TABLE_EXAMPLE)
    # print('*****\t****\t***\t**\t*\t**\t***\t****\t*****')
    # log.debug('Connection closed')


if __name__ == '__main__':
    main()
    