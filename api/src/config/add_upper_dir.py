import sys
from pathlib import Path
from platform import system

config = Path(__file__).resolve().parent
print(config)
logging_module = config.parent.resolve('packages\logging') # if 'windows'in system().strip().lower() else logging_module/packages/'logging'.as_posix
print(logging_module)

try:
    # In perfect world this simply should be sys.path.append(str(config)), but in my case that's what I have to do for some reason ...
    
    sys.path.append("B:\Projects\git_repos\flask_api\api\src\packages")
except Exception as exception_error:
    print('Unexpected error occured while importing module ...')
    print(exception_error)