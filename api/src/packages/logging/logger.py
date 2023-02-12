import uuid
import time
import logging
from pathlib import Path
from flask import request, g, has_request_context

from src.config.paths.paths import Paths


class Logger:


    _logger = logging.getLogger(__name__)

    def __init__(self, level: str = 'DEBUG', format: None | str = None, console: bool = False) -> None:
        '''
            Default constructor.
        '''

        self._level = level.strip().upper()
        self._format = format
        self._enable_console = console

        if self._logger.hasHandlers():
            self._logger.handlers.clear()
            
        self._initialize_logging()


    def _initialize_logging(self) -> None:
        '''
            Initializes logger level, log file and adds a console logging if the console is enabled.
        '''

        self._logger.setLevel(self._set_level())
        self._create_file_handler()
        if self._enable_console:
            self._create_console_handler()


    def _set_level(self) -> logging.Logger:
        '''
            Set's the logging level, based on what user has provided.
        '''

        logging_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        return logging_levels[self._level] if self._level in logging_levels else logging.DEBUG

    def _set_format(self) -> logging.Formatter:
        '''
            Set's the logging format. If not provided by user will used the default one.
        '''
        
        # '[%(asctime)s.%(msecs)03d UTC] (PROCESS: %(process)d) (%(request_id)s) %(levelname)s in %(module)s: MESSAGE: %(message)s'
        logging.Formatter.converter = time.gmtime
        return logging.Formatter(
            fmt=f'[%(asctime)s.%(msecs)03d UTC] | [PROCESS: %(process)d]\t| %(levelname)s\tin %(module)s: MESSAGE: %(message)s',
            datefmt='%d/%m/%Y at %H:%M:%S') if not self._format else logging.Formatter(self._format)

    def _create_file_handler(self) -> None:
        '''
            Creates a file handler.
        '''

        logging_dir = Path(Paths.LOGGING_DIR).resolve()
        if not logging_dir.exists():
            try:
                logging_dir.mkdir()
            except Exception as exception_message:
                # TODO: Find a way to alert user that something is wrong, and logging directery is unable to be generated.
                print('Unexpected execption occured while creating logging direcory ...')
                print(exception_message)
                exit(code=-1)

        
        self._add_handler(handler_type=logging.FileHandler(Paths.LOGGING_FILE))

    def _create_console_handler(self) -> None:
        '''
            Creates a console handler.
        '''

        self._add_handler(handler_type=logging.StreamHandler())

    def _add_handler(self, handler_type: logging.FileHandler | logging.StreamHandler) -> None:
        '''
            Groups the handlers.
        '''
        
        handler_type.setLevel(self._set_level())
        handler_type.setFormatter(self._set_format())
        self._logger.addHandler(handler_type)

    def debug(self, message: str) -> None:
        '''
            Custom debug level of logging.
        '''

        self._logger.debug(message)

    def info(self, message: str) -> None:
        '''
            Custom info level of logging.
        '''

        self._logger.info(message)

    def warning(self, message: str) -> None:
        '''
            Custom warning level of logging.
        '''

        self._logger.warning(message)

    def critical(self, message: str) -> None:
        '''
            Custom critical level of logging.
        '''

        self._logger.critical(message)

    def error(self, message: str) -> None:
        '''
            Custom error level of logging.
        '''

        self._logger.error(message)


def setup_flask_logging(application):
    '''
        Set's up the Flask logging.
    '''

    @application.after_request
    def afters(response):
        response.headers['X-Request-ID'] = _request_id()
        return response

    return Logger(console=True)

def _request_id():
    '''
    
    '''

    if hasattr(g, 'request_id'):
    # if getattr(g, 'request_id', None):
        return g.request_id

    existing_uuid = request.headers.get('X-Request-ID')
    new_uuid = uuid.uuid4()
    
    request_id = existing_uuid or new_uuid
    g.request_id = request_id

    return request_id
    