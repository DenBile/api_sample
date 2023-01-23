import requests
# import webauth_wsg

from redis import Redis
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_caching import Cache
# from requests_gssapi import HTTPSPNEGOAuth

class Service:
    '''
        Custom service for Flask endpoints.
    '''

    