from datetime import datetime
class DateTime:
    '''
        Custom datetime class.
    '''

    def __init__(self) -> None:
        '''
            Default constructor.
        '''

        self.utc_time_now = datetime.utcnow()
    
    def convert_for_path(self) -> str:
        '''
            Converts the datetime to the format that will be used in paths.
        '''

        return self.utc_time_now.strftime('%Y%m%d_%H%M%S')