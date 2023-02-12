from src.endpoints.user.register import register_namespace
from src.endpoints.sample.sample_api import sample_namespace

namespaces: list = [
    register_namespace,
    sample_namespace
]