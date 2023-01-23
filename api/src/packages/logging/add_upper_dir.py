import sys
from pathlib import Path
from platform import system


logging_module = Path(__file__).resolve().parent
database_module = logging_module.parent.resolve('logging')

try:
    database_module = fr'{database_module}\databases' if 'windows'in system().strip().lower() else database_module/'databases'
    # In perfect world this simply should be sys.path.append(str(logging_module)), but in my case that's what I have to do for some reason ...
    sys.path.append('b'+str(logging_module)[1:])
    sys.path.append('b'+database_module[1:])
except Exception as exception_error:
    print('Unexpected error occured while importing module ...')
    print(exception_error)