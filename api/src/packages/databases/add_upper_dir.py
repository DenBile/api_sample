import sys
from pathlib import Path
from platform import system

database_module = Path(__file__).resolve().parent
print(database_module)
logging_module = database_module.parent.resolve('logging')
print(logging_module)
try:
    logging_module = fr'{logging_module}\logging' if 'windows'in system().strip().lower() else logging_module/'logging'
    
    # In perfect world this simply should be sys.path.append(str(database_module)), but in my case that's what I have to do for some reason ...
    sys.path.append('b'+str(database_module)[1:])
    sys.path.append('b'+logging_module[1:])
except Exception as exception_error:
    print('Unexpected error occured while importing module ...')
    print(exception_error)