from packages.databases.table import Table

class MySQLTable(Table):


    def create(self, cursor: object) -> None:
        '''
            Custom method to execute insert queries in the database.
        '''

        self._log.info('Query to insert new table will be executed ...')
        cursor.execute(self.sql)
        self._log.info('Insert SQL Executed successfully ...')
        
    def drop(self, cursor: object) -> None:
        '''
            Custom method to execute delete queries in the database.
        '''

        self._log.info('Query to delete table will be executed ...')
        cursor.execute(self.sql)
        self._log.info('Delete SQL Executed successfully ...')
