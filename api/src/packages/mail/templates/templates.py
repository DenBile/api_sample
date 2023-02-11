import subprocess
from abc import ABC

from src.config.paths.paths import Paths

class EmailSettings(ABC):

    sender: str                 = subprocess.getoutput('whoami')
    recipients: str | list[str] = [subprocess.getoutput('whoami')]
    copies: str | list[str]     = [subprocess.getoutput('whoami')]

class ErrorMail(EmailSettings):

    subject: str        = '[ERROR] Unexpectedly stopped'
    attachments: str    = Paths.LOGGING_FILE
