

import socket
from abc import ABC, abstractclassmethod
from dataclasses import dataclass, field

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from config.paths.paths import Paths
from packages.logging.logger import Logger

import json
from bs4 import BeautifulSoup

class EmailService:

    _log = Logger(console=True)

    def __init__(self) -> None:
        '''
            Default constructor.
        '''

        self._connection = None
        self._get_config_file()

    def __enter__(self):
        '''
            Gives the ability to connect to the mailbox using "with" keyword.
        '''

        self._connect()
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        '''
            Closes safely the connection.
        '''

        if any((exception_type, exception_value, traceback)):
            self._log.critical('Disconnected from the mail service was triggered due to an unexpected exception.')
            self._log.critical(exception_type)
            self._log.critical(exception_value)
            self._log.critical(traceback)
        self._disconnect()
    
    def _get_config_file(self) -> None:
        '''
            Gets the configurations from the config file.
        '''

        try:
            with open(Paths.MAIL_CONFIG) as mail_config_file:
                self._config = json.load(mail_config_file)
        except Exception as exception_message:
            self._log.critical('Unexpected error occured while fetching mail configurations ...')
            self._log.critical(exception_message)


    def _connect(self) -> None:
        '''
            Establishes the connection.
        '''

        try:
            self._connection = smtplib.SMTP()
            self._connection.connect(self._config['connection'])
        except socket.error as smtplib_error:
            self._log.critical('Unexpected error occured, could not connect to the mail service ...')
            self._log.critical(smtplib_error)
        except Exception as exception_message:
            self._log.critical('Unexpected error occured, could not connect to the mail service ...')
            self._log.critical(exception_message)

    def _disconnect(self) -> None:
        '''
            Closes the connection.
        '''

        self._connection.quit()
        self._log.info('Disconnecting from the mail service ...')

    def send_mail(self, sender: str, recipients: str, message: str) -> None:
        '''
            Sends the emial to user.
        '''

        self._connection.sendmail(from_addr=sender, to_addrs=recipients, msg=message)

@dataclass
class Mail:
    '''
        Mail class.

        Arguments:
            subject: str
            sender: str
            recipients: list[str]
            body: dict[str, dict[str, str]]
            attachments: list[str]
    '''

    subject: str
    sender: str
    recipients: str | list[str]
    copies: str | list[str]
    body: dict[str, dict[str, str]] = field(default_factory=dict)
    attachments: list[str] = field(default_factory=list)

    _log = Logger(console=True)

    def __post_init__(self) -> None:
        '''
            Sets all necessary process after the object is created.
        '''


        self._message = MIMEMultipart()
        self._generate_mail()
    
    def _generate_mail(self) -> None: 
        '''
            Generates the email.
        '''

        self._set_subject()
        self._set_sender()
        self._set_recipients()
        self._set_body()
        if self.attachments:
            self._set_attachments()
        
    def _set_subject(self) -> None:
        '''
            Sets the subject of the email.
        '''

        self._log.info(f'Adding subject "{self.subject}" to the email ...')
        self._message['Subject'] = self.subject
    
    def _set_sender(self) -> None:
        '''
            Sets the sender of the email.
        '''

        self._log.info(f'Adding sender "{self.sender}" to the email ...')
        self._message['From'] = self.sender
    
    def _set_recipients(self) -> None:
        '''
            Sets the recipients of the email.
        '''

        self._message['To'] = ', '.join(self.recipients) if isinstance(self.recipients, list) else self.recipients
        self._log.info(f'Adding recipients "{self._message["To"]}" to the email ...')
        self._message['Cc'] = ', '.join(self.copies) if isinstance(self.copies, list) else self.copies
        self._log.info(f'Adding CC "{self._message["Cc"]}" to the email ...')
    
    def _set_body(self) -> None:
        '''
            Sets the body of the email.
        '''

        self._log.info(f'Adding body of the email ...')
        try:
            with open(Paths.HTML_TEMPLATE) as template_file:
                default_template = template_file.read()
        except Exception as exception_message:
            self._log.critical('Unexpected error occured while opening default HTML email template ...')
            self._log.critical(exception_message)
            exit(-1)
        
        if self.body == '':
            self._log.warning('Body was not specified by user, will use default template ...')
            self.body = default_template
        else:
            if not isinstance(self.body, dict):
                self._log.warning('Given body:')
                self._log.warning(self.body)
                self._log.warning('Is not the correct format will use default template ...')
                self.body = default_template
            else:
                # TODO: add recursive function to loop through the elements and store them in the dict
                # then add users option in place of old ones
                # in case user would like to add new element that is not present in default template
                # add it in that order.
                # self._adjust_default_template(default_template=default_template)
                pass
    
        self._message.attach(MIMEText(self.body, 'html', _charset='utf-8'))

    def _adjust_default_template(self, default_template: str) -> None:
        '''
            Adjust default template to the one that user provided.
        '''

        soup = BeautifulSoup(default_template, 'html.parser')

        # TODO
    
    def _set_attachments(self) -> None:
        '''
            Sets the attachments of the email.
        '''

        self._log.info(f'Adding attachments to the email ...')
        if not isinstance(self.attachments, list):
            self._log.warning('Given attachments were not in format of list, will convert them into list ...')
            self.attachments = self.attachments.split() if ',' in self.attachments else [self.attachments]
    
        for attachment in self.attachments:
            try:
                with open(file=attachment, mode='rb') as file_to_attach:
                    self._message.attach(MIMEApplication(
                        file_to_attach.read(),
                        Name=attachment.split('/')[-1]
                    ))
            except Exception as exception_message:
                self._log.error('Unexpected error occured while adding attachment to the email ...')
                self._log.error(exception_message)

    def send(self) -> None:
        '''
            Sends email.
        '''

        with EmailService() as message_service:
            message_service.send_mail(
                sender=self.sender,
                recipients=self.recipients,
                message=self._message.as_string()
            )