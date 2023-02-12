from dataclasses import dataclass, field


ERROR_MESSAGES = {
    'NOT_SUPPORTED_MESSAGE': '[API] The message type you have selected is not supported, please select one of the following ones: '
}

@dataclass
class UserMessage:
    '''
        Custom user message class.
    '''

    notify_user: bool = True
    message: dict[str, str] = field(default_factory={lambda: 'message': 'Success'})
    payload: None | dict[str, str] = None
    return_code: int = field(init=False)

    def __post_init__(self) -> None:
        '''
            Initializes the return code.
        '''

        self._set_return_code()

    def _set_return_code(self) -> None:
        '''
        Checks the message and set's according message.
        '''

        message_options = {
            'message': 200,
            'success_message': 200,
            'warning_message': 400,
            'error_message': 400
        }

        for message_option in message_options:
            if message_option in self.message:
                self.return_code = message_options[message_option]
    

    def add_message(self, new_message: dict[str, bool|int|str]) -> None:
        '''
            Add's message to what will be sent to user.
        '''

        self.message = self.check_valid_message_type(new_message=new_message) if 'message' in self.message else new_message if not self.message else self._select_message_on_level(new_message=new_message)

    def check_valid_message_type(self, new_message: dict[str, bool|int|str]) -> str:
        '''
            Check's if user provided valid message type.
        '''

        message_options = {'success_message', 'warning_message', 'error_message'}

        return {'error_message': f'{"".join(list(new_message.values())[0])} {ERROR_MESSAGES["NOT_SUPPORTED_MESSAGE"]} {", ".join(message_options)}'} if list(new_message)[0] not in message_options else new_message

    def _select_message_on_level(self, new_message: dict[str, bool|int|str]) -> dict[str, bool|int|str]:
        '''
            Select's message type based on it's level.
        '''

        message_levels = {
            'message': 0,
            'success_message': 1,
            'warning_message': 2,
            'error_message': 3
        }

        existing_message_type = list(self.message)[0]
        new_message_type = list(new_message)[0]
        return {existing_message_type if message_levels[existing_message_type] > message_levels[new_message_type] else new_message_type: f'{"".join(list(self.message.values())[0])}' if message_levels[existing_message_type] < message_levels[new_message_type] else ''.join(list(new_message.values())[0])}

    def return_message(self) -> tuple[dict[str, bool|int|str], int]:
        '''
            Return's message from the endpoint.
        '''

        return self._check_payload(), self.return_code

    def _check_payload(self) -> dict[str, bool|int|str]:
        '''
            Check's if the message has a payload.
        '''

        return {
            'notify_user': self.notify_user,
            list(self.message)[0]: self.message[list(self.message)[0]],
            'payload': self.payload
        } if self.payload else {
            'notify_user': self.notify_user,
            list(self.message)[0]: self.message[list(self.message)[0]]
        }