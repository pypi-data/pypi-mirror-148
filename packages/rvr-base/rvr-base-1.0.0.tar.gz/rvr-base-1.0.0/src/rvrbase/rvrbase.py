import logging
from platform import node
import json
import sys
from dbus import ValidationException

from rvrbase.__about__ import __version__ as version
from rvrbase.api import New_notification_api
from rvrbase.api import Azure_logger_api
from rvrbase.api import Rvrconfig
from rvrbase.constants import LOG_TYPE_APPLICATION_EVENT, MST_STARTING, NOTIFY_APPLICATION_EVENT,\
    VALID_MESSAGE_TYPES


class Rvrbase():

    def __init__(self, path):

        self.config_api = Rvrconfig(path)
        self.notifcation_api = New_notification_api()
        self.azure_logger_api = Azure_logger_api()
        self.workspace_id = self.q1('workspace_id')
        self.workspace_prim_key = self.q1('primary_key')

        self.send_az_app_event(type='info', message=MST_STARTING.format(
            url=self.notifcation_api.notify.endpoint))

    def send_browser_notification(self, message, type):
        if type not in VALID_MESSAGE_TYPES:
            raise ValidationException(
                f'{type} is not in {VALID_MESSAGE_TYPES}.')

        self.notifcation_api.send_browser_notification(
            NOTIFY_APPLICATION_EVENT.format(type=type, node=node(), message=message))

    def log_app_event(self, type, message, notify_message=False):
        if type not in VALID_MESSAGE_TYPES:
            raise ValidationException(
                f'{type} is not in {VALID_MESSAGE_TYPES}.')

        if type == 'debug':
            logging.debug(message)
        elif type == 'info':
            logging.info(message)
        elif type == 'warning':
            logging.warning(message)
        elif type == 'error':
            logging.error(message)

        self.send_az_app_event(type, message)

        if notify_message:
            self.notifcation_api.send_browser_notification(message=message)

    def send_az_app_event(self, type, message):
        if type not in VALID_MESSAGE_TYPES:
            raise ValidationException(
                f'{type} is not in {VALID_MESSAGE_TYPES}.')

        body = {
            "hostname": node(),
            "script_path": sys.argv[0],
            "arguments": sys.argv[1:],
            "type": type,
            "message": message,
            "rvrbase_version": version
        }

        body_json = json.dumps(body)

        try:
            self.azure_logger_api.post_data(
                body_json, LOG_TYPE_APPLICATION_EVENT, self.workspace_id, self.workspace_prim_key)

        except Exception as error:
            message = 'Failed to log message to azure on {node}. With error {error}.'.format(
                node=node(), error=error)
            logging.error(message)
            self.notifcation_api.send_browser_notification(message=message)

    def send_az_metric(self, log_type, metric_name, value):
        body = {
            "hostname": node(),
            "script_path": sys.argv[0],
            "metric_name": metric_name,
            "value": value,
            "rvrbase_version": version
        }

        body_json = json.dumps(body)
        self.azure_logger_api.post_data(
            body_json, log_type, self.workspace_id, self.workspace_prim_key)

    def q1(self, key):
        return self.config_api.q1(key=key)
