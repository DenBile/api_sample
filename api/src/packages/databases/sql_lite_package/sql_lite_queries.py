import pandas as pd
from query import Query

class SQLiteQuery(Query):


    def select(self, cursor: object) -> tuple[pd.DataFrame, str]:
        '''
            Custom method to execute select queries in the database.
        '''

        self._log.info('Select query will be executed.')
        cursor.execute(self.sql) if not self.properties else cursor.execute(self.sql, self.properties)
        
        self._log.info('Fetching results ...')
        rows = cursor.fetchall()
        column_names = zip(*cursor.description)

        return (pd.DataFrame(data=rows, columns=column_names), column_names)

    def insert(self, cursor: object, bulk: bool) -> None:
        '''
            Custom method to execute insert queries in the database.
        '''

        self._log.info('Insert query will be executed ...')
        cursor.executemany(self.sql, self.properties) if bulk else cursor.execute(self.sql, self.properties)
        self._log.info('Insert SQL Executed successfully ...')
        self._log.info(f'Inserted {cursor.rowcount} new row(s) ...')

    def update(self, cursor: object, bulk: bool) -> None:
        '''
            Custom method to execute update queries in the database.
        '''

        self._log.info('Update query will be executed ...')
        cursor.executemany(self.sql, self.properties) if bulk else cursor.execute(self.sql, self.properties)
        self._log.info('Update SQL Executed successfully ...')
        self._log.info(f'Updated {cursor.rowcount} row(s) ...')
        
    def delete(self, cursor: object, bulk: bool) -> None:
        '''
            Custom method to execute delete queries in the database.
        '''

        self._log.info('Delete query will be executed ...')
        cursor.executemany(self.sql, self.properties) if bulk else cursor.execute(self.sql, self.properties)
        self._log.info('Delete SQL Executed successfully ...')
        self._log.info(f'Deleted {cursor.rowcount} row(s) ...')
