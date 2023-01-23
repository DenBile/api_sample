import bcrypt
import sqlite3
import json


from .pepper import PEPPER
from config.paths.paths import Paths
from packages.logging.logger import Logger
from packages.databases.sql_lite_package.sql_lite_connector import SQLiteConnection


class Authentication:

    _log = Logger(console=True)

    def __init__(self):
        '''
            Default constructor.
        '''

        self._pepepr = PEPPER
        self._get_auth_database()


    def _get_auth_database(self) -> None:
        '''
            Gets the corresponding database for the authentication users.
        '''

        try:
            with open(Paths.DATABASES_CONFIG) as database_config_file:
                self._auth_database = json.load(database_config_file)
            self._auth_database = self._auth_database['MySQLite']['auth']
            self._log.info('User authentication config file opened successfully ...')
        except Exception as exception_message:
            self._log.critical(f'Unexpected error occured while openning the config file for the user authentication  ...')
            self._log.critical(exception_message)
            exit(-1)

    def _generate_password(self, password: str) -> str:
        '''
            Generates password.
        '''

        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def create_user(self, username: str, password: str) -> bool:
        '''
            Creates new user.        
        '''

        # TODO: Move the queries itself out of here
        _insert_salt_query: str = 'INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?, ?)'
        _insert_pepper_query: str = 'INSERT INTO PEPPER (USERNAME, PEPPER) VALUES (?, ?)'
        password = self._generate_password(password=password)
        
        with SQLiteConnection(database=f'../{self._auth_database}') as sqlite_db:
            sqlite_db.execute_query(sql=_insert_salt_query, properties=[username, password])
            sqlite_db.execute_query(sql=_insert_pepper_query, properties=[username, password])

        return self.authenticate(username=username, password=password)

    def authenticate(self, username: str, password: str) -> bool:
        '''
            Authenticates user.
        '''

        # TODO: Move the query itself out of here
        _select_user_query: str = 'SELECT PASSWORD, PEPPER FROM USERS, PEPPER WHERE USERS.USERNAME = PEPPER.USERNAME AND USERS.USERNAME = ?'
        with SQLiteConnection(database=f'{Paths.DATABASES_CONFIG}/{self._auth_database}') as sqlite_db:
            db_data = sqlite_db.execute_query(sql=_select_user_query, properties=[username])

        if not db_data:
            return False

        password = password.encode('utf-8')
        password = bcrypt.hashpw(password, self._pepepr)
        password = bcrypt.hashpw(password, db_data[1])
        return password == db_data[0]

    def update_password(self, username: str, password: str) -> bool:
        '''
            Update the password for a given user.
        '''

        _update_user_pass_query: str = 'UPDATE USERS SET PASSWORD = ? WHERE USERNAME = ?'
        with SQLiteConnection(database=f'{Paths.DATABASES_CONFIG}/{self._auth_database}') as sqlite_db:
            sqlite_db.execute_query(sql=_update_user_pass_query, properties=[self._generate_password(password=password), username])

        return self.authenticate(username=username, password=password)
