# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def yo():
#     return 'WAZZZZZZZZZZZZZZZZZZAP'

from config.config import Directories
from packages.logging.logger import Logger
from packages.databases.my_sql_package.mysql_connector import MySqlConnection


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