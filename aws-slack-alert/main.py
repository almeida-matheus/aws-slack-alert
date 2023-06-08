import json
import logging
import os
from provider.aws import AWS
from provider.slack import Slack

aws = AWS()

SLACK_WEBHOOK_URL = aws.get_parameter(os.getenv('SLACK_WEBHOOK_PARAMETER'))
SLACK_USERNAME = os.getenv('SLACK_USERNAME')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

def handler(event, context):

    logger = logging.getLogger('lambda_slack_notifier.log')
    logger.setLevel(logging.INFO)

    try:
        logger.info("Event: {}".format(event["Records"]))

        event_subject = event["Records"][0]["Sns"]["Subject"]
        event_message = event["Records"][0]["Sns"]["Message"]

        try:
            event_message = json.loads(event_message)
        except:
            pass

        slack = Slack(webhook_url=SLACK_WEBHOOK_URL, username=SLACK_USERNAME, channel=SLACK_CHANNEL)

        treated_message = slack.format_message(event_subject, str(event_message))

        return slack.send(event_subject, treated_message)

    except Exception as e:
        logger.error(str(e))
        raise