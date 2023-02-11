import requests
# import webauth_wsg

from dataclasses import dataclass, field

from redis import Redis
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_caching import Cache
# from requests_gssapi import HTTPSPNEGOAuth

from src.packages.logging.logger import Logger

@dataclass
class Service:
    '''
        Custom service for Flask endpoints.
    '''

    name: str
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
        self._service_config = _set_service_config()
        self._env = 'prod' if self._service_config['ENV'] == 'prod' else 'dev'
        self._cache_config = self._set_cache_config()

    def _set_cache_config(self) -> dict[str, str]:
        '''
            Configurate the cache for the service.
        '''

        pass

    def _set_service_config(self) ->  dict[str, str]:
        '''
            Load config file localy or from a remote server.
        '''

        if load_remote_config:
            
            return requests.get('http://localhost/').json()

        try:
            pass
        except IOError as open_error:
            self.log.error('Unable to open a config file, therefore unable to start the service ...')
            self.log.critical(open_error)
        except Exception as exception_error:
            self.log.error('Unexpected error occured, therefore unable to start the service ...')
            self.log.critical(exception_error)
        else:
            pass