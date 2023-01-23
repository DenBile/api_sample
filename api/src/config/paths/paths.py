from pathlib import Path
from dataclasses import dataclass

from .files_names import FileName
from .directories import Directories
from helpers.date_time import DateTime

utc_time_now = DateTime().convert_for_path()

class Paths:

    LOGGING_DIR: str        = Path(Directories.LOGGING).resolve().as_posix()
    LOGGING_FILE: str       = Path(f'{LOGGING_DIR}/{utc_time_now}_{FileName.LOG}').resolve().as_posix()
    CONFIG: str             = Path(Directories.CONFIG).resolve().as_posix()
    DATABASES_CONFIG: str   = Path(f'{Directories.CONFIG}/{FileName.DATABASES_CONFIG}').resolve().as_posix()
    MAIL_CONFIG: str        = Path(f'{CONFIG}/{FileName.MAIL}').resolve().as_posix()
    REPORTS: str            = Path(Directories.REPORTS).resolve().as_posix()
    CURRENT_REPORT: str     = Path(f'{Directories.REPORTS}/{utc_time_now}/').resolve().as_posix()
    HTML_TEMPLATE: str      = Path(f'{Directories.HTML_TEMPLATE}/{FileName.HTML_TEMPLATE}').resolve().as_posix()