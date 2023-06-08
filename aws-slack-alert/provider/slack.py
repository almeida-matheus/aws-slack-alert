import json
import logging
import urllib3

logger = logging.getLogger('lambda_slack_notifier.log')
http = urllib3.PoolManager()

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

    def format_message(self, subject: str, body: str) -> dict:
        """Formats the subject and message body into Slack blocks.

        Args:
            subject (str): Subject that will appear on the notification popup.
            body (str): The full message body.

        Returns:
            A dictionary payload with Slack block formatting.
        """
        color = '#D70040'
        formated_message = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{}* ".format(subject)
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
            logger.error("Error occurred when communicating with Slack {} {}".format(e.code, e.reason))
        except (urllib3.exceptions.ConnectTimeoutError,urllib3.exceptions.TimeoutError) as e:
            logger.error("Timeout occurred when trying to send message to Slack: {}".format(e.reason))
        else:
            logger.info("Successfully sent message to Slack channel {}".format(self.channel))
            return {
                "message": subject,
                "status_code": response.status,
                "response": response.data,
            }