# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def yo():
#     return 'WAZZZZZZZZZZZZZZZZZZAP'

from packages.logging.logger import Logger
from config.config import Directories

def main():
    log = Logger()
    log.info('...')
    d = Directories()

if __name__ == '__main__':
    main()