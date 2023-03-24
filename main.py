from provider.slack import Slack
from provider.aws import AWS
import logging
import io
import os

log_stream = io.StringIO()
logging.basicConfig(stream=log_stream, level=logging.INFO, format='%(levelname)s: %(message)s')
logging.getLogger("botocore").setLevel(logging.WARNING)
aws = AWS()

SLACK_WEBHOOK_URL = aws.get_parameter(os.environ.get('PARAMETER_SLACK_WEBHOOK_URL'))
SLACK_USERNAME = os.environ.get('SLACK_USERNAME')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')

def handler(event, context):
    try:
        logging.info("Event: {}".format(event["Records"]))

        event_subject = event["Records"][0]["Sns"]["Subject"]
        event_message = event["Records"][0]["Sns"]["Message"]

        logging.info(f'Event subject: {event_subject}')
        logging.info(f'Event message: {event_message}')

        slack = Slack(webhook_url=SLACK_WEBHOOK_URL,username=SLACK_USERNAME,channel=SLACK_CHANNEL)

        required_fields_msg_body = ['AlertType','AlertCode','AlertCause']
        if not isinstance(event_message, dict):
            logging.warning('Message formatting was not applied because your values is not dict(object) type')
            treated_message = slack.format_message(event_subject,str(event_message))
        elif not (required_fields_msg_body == list(event_message.keys())):
            logging.warning('Message formatting was not applied because not all required fields were identified - {}'.format(required_fields_msg_body))
            treated_message = slack.format_message(event_subject,str(event_message))
        else:
            treated_message = slack.format_message(event_subject,event_message)

        return slack.send(event_subject,treated_message)

    except Exception as e:
        logging.error(str(e))
        raise

    finally:
        print(log_stream.getvalue())

