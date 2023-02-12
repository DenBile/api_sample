import json
import requests
from pathlib import Path
from dataclasses import dataclass, field
# import webauth_wsg

from redis import Redis
from flask import Flask
from flask_restx import Api
# from flask_cors import CORS
from flask_caching import Cache
# from requests_gssapi import HTTPSPNEGOAuth


from src.packages.mail.mail import Mail
from src.config.paths.paths import Paths
from src.packages.logging.logger import Logger
from src.packages.mail.templates.service_template import ServiceInitializationErrorEmail, ServiceNoFileErrorEmail

@dataclass
class Service:
    '''
        Custom service for Flask endpoints.
    '''

    name: None | str = None
    timeout: int = 300
    use_external_cache: bool = False
    load_remote_config: bool = False

    app: Flask = field(init=False)
    cache: Cache = field(init=False)
    # auth: Auth = field(init=False)
    # audit: Audit = field(init=False)
    api: Api = field(init=False)
    # zk: ZK

    log: Logger = Logger(console=True)

    def __post_init__(self) -> None:
        '''
            Default constructor.
        '''

        self.log.debug('Starting service ...')
        self._service_config = self._set_service_config()
        if not self.name:
            self.name = self._service_config['NAME']
        self._env = 'prod' if self._service_config['ENV'] == 'prod' else 'dev'
        self._cache_config = self._set_cache_config()
        self._init_app()


    def _set_service_config(self) ->  dict[str, str]:
        '''
            Load config file localy or from a remote server.
        '''

        if self.load_remote_config:
            self.log.debug('Loading service config from a remote server ...')
            remote_configs = requests.get('http://localhost/').json()
            if remote_configs:
                self.log.info('Remote cofigurations loaded successfully ...')
                return remote_configs
            
            self.log.error('Unable to load remote configurations, will continue with local ...')
            self.lof.error(remote_configs)

        try:
            with open(Paths.SERVICE_CONFIG) as service_config_file:
                service_config = json.load(service_config_file)
        except IOError as open_error:
            self.log.error('Unable to open a config file, therefore unable to start the service ...')
            self.log.critical(open_error)
            send_error_email(
                subject=ServiceNoFileErrorEmail.subject,
                sender=ServiceNoFileErrorEmail.sender,
                recipients=ServiceNoFileErrorEmail.recipients,
                copies=ServiceNoFileErrorEmail.copies,
                body=ServiceNoFileErrorEmail.body,
                attachments=ServiceNoFileErrorEmail.attachments
            )
        except Exception as exception_error:
            self.log.error('Unexpected error occured, therefore unable to start the service ...')
            self.log.critical(exception_error)
            send_error_email(
                subject=ServiceInitializationErrorEmail.subject,
                sender=ServiceInitializationErrorEmail.sender,
                recipients=ServiceInitializationErrorEmail.recipients,
                copies=ServiceInitializationErrorEmail.copies,
                body=ServiceInitializationErrorEmail.body,
                attachments=ServiceInitializationErrorEmail.attachments
            )
        else:
            self.log.info('Local config file loaded successfully ...')
            return service_config

    def _set_cache_config(self) -> dict[str, str]:
        '''
            Configurate the cache for the service.
        '''

        self.log.debug('Setting service cache config ...')
        return {
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_HOST': self._service_config['CACHE']['CACHE_REDIS_HOST'],
            'CACHE_REDIS_PORT': self._service_config['CACHE']['CACHE_REDIS_PORT'],
            'CACHE_REDIS_PASSWORD': '', # TODO: Add password authentication...
            'CACHE_DEFAULT_TIMEOUT': self.timeout
        } if self.use_external_cache else {
            'DEBUG': True,
            'CACHE_TYPE': 'SimpleCache',
            'CACHE_DEFAULT_TIMEOUT': self.timeout
        }

    def _init_app(self) -> None:
        '''
            Initializes service.
        '''

        self._set_app()
        self._set_api()

    def _set_app(self) -> None:
        '''
            Set's the Flask APP.
        '''

        self.log.debug('Setting service APP ...')
        self.app = Flask(self.name)
        self.app.config.from_mapping(self._cache_config)
        self.app.register_error_handler(Exception, Service.error_handler)

    def _set_api(self) -> None:
        '''
            Set's the Flask Rest-X API.
        '''

        self.log.debug('Setting Flast Rest-X API ...')
        try:
            api_version = self._service_config['BUILD_VERSION']
        except Exception as exception_message:
            self.log.warning('Unexpected error occured. Api version will be set to DEV ...')
            self.log.warning(exception_message)
            api_version = 'dev'
        
        self.api = Api(self.app, version=api_version, title=self._service_config['NAME'])

    def error_handler(error) -> tuple[dict[str, str], int]:
        '''
            Custom service error handler.
        '''

        log = Logger()
        log.error(f'Unexpected exception occured ... {str(error)}')
        return {
            'error_message': f'Unexpected exception occured ... {str(error)}',
            'notify_user': True
        }, 400


def send_error_email(subject: str, sender: str, recipients: str | list, copies: str | list, body: dict[str, dict[str, str]], attachments: list[str]) -> None:
    '''
        Send's error email to user, to notify in case of failure.
    '''

    error_mail = Mail(
        subject=subject,
        sender=sender,
        recipients=recipients,
        copies=copies,
        body=body,
        attachments=attachments
    )
    error_mail.send()
    exit(-1)
