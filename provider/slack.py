import logging
import json
import urllib3
import certifi

logging.getLogger(__name__)
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
# http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)

class Slack:

    def __init__(self, webhook_url: str, username: str, channel: str, timeout: int = 15):
        """Class to send messages to a Slack webhook URL.

        You can read more about Slack's Incoming Webhooks here:
            https://api.slack.com/messaging/webhooks

        Args:
            webhook_url (str): The Slack webhook URL to send a message to.  Typically
                formatted like "https://hooks.slack.com/services/...".
            username (str): Name of the user who will send the message.
            channel (str): Slack channel where the message will be sent.

        Kwargs:
            timeout (int, optional): Number of seconds before the request will timeout.
                Default value is 15 seconds.
        """
        self.webhook_url = webhook_url
        self.username = username
        self.channel = channel
        self.timeout = timeout
        self.headers = {
            'Content-Type': 'application/json',
        }

    def format_message(self, subject: str, body: str or dict) -> dict:
        """Formats the subject and message body into Slack blocks.

        Args:
            subject (str): Subject that will appear on the notification popup.
            body (str): The full message body.

        Returns:
            A dictionary payload with Slack block formatting.
        """
        if isinstance(body, dict):

            if body.get('AlertType') == 'Error':
                color = '#D70040'
                emote = ':warning: '
            elif body.get('AlertType') == 'Success':
                color = '#50C878'
                emote = ':white_check_mark: '
            else:
                color = '#1F51FF'
                emote = ''

            formated_message = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*{} {}* ".format(emote,subject)
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*{}*:\n{}".format(body['AlertType'],body['AlertCode'])
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Resource:*\n{}".format('ResourceName')
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": body['AlertCause']
                    }
                }
            ]
        else:
            error_match_str = ['fail','error','exception','not authorized']
            if any(er_str in body.lower() for er_str in error_match_str):
                color = '#D70040'
                emote = ':warning: '
            else:
                color = '#50C878'
                emote = ':white_check_mark: '

            formated_message = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*{} {}* ".format(emote,subject)
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": body
                    }
                }
            ]

        return [{"blocks": formated_message, "color":color}]

    def send(self, subject: str, message: str) -> dict:
        """Sends a formatted message to the webhook URL.

        Args:
            subject (str): The subject of the message that will appear in the notification preview.
            message (str): Plain text string to send to Slack.

        Returns:
            A dictionary payload with Slack request response.
        """

        payload = {
            'username': self.username,
            'channel': self.channel,
            'attachments': message
        }
        
        try:
            encoded_payload = json.dumps(payload).encode("utf-8")
            response = http.request("POST", self.webhook_url, body=encoded_payload)
        except urllib3.exceptions.HTTPError as e:
            logging.error("Error occurred when communicating with Slack {} {}".format(e.code, e.reason))
        except (urllib3.exceptions.ConnectTimeoutError,urllib3.exceptions.TimeoutError) as e:
            logging.error("Timeout occurred when trying to send message to Slack: {}".format(e.reason))
        else:
            logging.info("Successfully sent message to Slack channel {}".format(self.channel))
            return {
                "message": subject,
                "status_code": response.status,
                "response": response.data,
            }