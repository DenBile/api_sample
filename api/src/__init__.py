from src.packages.service.service import Service
from src.packages.logging.logger import setup_flask_logging

service = Service()
log = setup_flask_logging(service.app)
