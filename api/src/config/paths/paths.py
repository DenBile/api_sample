from pathlib import Path
from dataclasses import dataclass

from .files_names import FileName
from .directories import Directories
from helpers.date_time import DateTime

utc_time_now = DateTime().convert_for_path()

class Paths:

    LOGGING_DIR     = Path(Directories.LOGGING).resolve().as_posix()
    LOGGING_FILE    = Path(f'{LOGGING_DIR}/{utc_time_now}_{FileName.LOG}').resolve().as_posix()
    CONFIG          = Path(Directories.CONFIG).resolve().as_posix()
    MAIL_CONFIG     = Path({f'{CONFIG}/{FileName.MAIL}'}).resolve().as_posix()
    HTML_TEMPLATE   = Path(Directories.HTML_TEMPLATE).resolve().as_posix()