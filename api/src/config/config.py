import subprocess
from abc import ABC
from pathlib import Path
from dataclasses import dataclass, field

from .paths.paths import Paths
from packages.logging.logger import Logger
from packages.mail.mail import Mail


class EmailSettings(ABC):

    sender: str                 = subprocess.getoutput('whoami')
    recipients: str | list[str] = [subprocess.getoutput('whoami')]
    copies: str | list[str]     = [subprocess.getoutput('whoami')]

class ErrorMail(EmailSettings):

    subject: str        = '[ERROR] Unexpectedly stopped'
    attachments: str    = Paths.LOGGING_FILE

class ConfigDirectoryErrorEmail(ErrorMail):

    body = ''

@dataclass(frozen=True)
class Directories:


    log = Logger(console=True)
    path_map: dict[str, list[str]] = field(default_factory=lambda: (
        Paths.CONFIG,
        Paths.LOGGING_DIR,
        Paths.REPORTS,
        Paths.CURRENT_REPORT,
    ))

    def __post_init__(self) -> None:
        '''
            Executes exactly after the object has been created.
        '''

        self._check_dircectories()

    def _check_dircectories(self) -> None:
        '''
            Checks if the directory exsts - if not, creates it.
        '''

        for directory in self.path_map:
            _dir = Path(directory).resolve()
            if _dir.exists():
                self.log.debug(f'{directory} exists ... no action required ...')
                continue

            self.log.warning(f'{directory} directory does not exists ... will create a new one ...')
            try:
                _dir.mkdir()
                self.log.info('Directory created successfully ...')
            except Exception as exception_message:
                self.log.critical('Unable to create the directory ...')
                self.log.critical(exception_message)
                error_mail = Mail(
                    subject=ConfigDirectoryErrorEmail.subject,
                    sender=ConfigDirectoryErrorEmail.sender,
                    recipients=ConfigDirectoryErrorEmail.recipients,
                    copies=ConfigDirectoryErrorEmail.copies,
                    body=ConfigDirectoryErrorEmail.body,
                    attachments=ConfigDirectoryErrorEmail.attachments
                )
                error_mail.send()
                exit(-1)