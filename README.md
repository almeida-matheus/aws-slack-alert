# aws-slack-alert

## About

The objective of the project is to notify actions of an AWS resource to a Slack channel through a message publication to an SNS topic that has as Subscribe a Lambda that is triggered from this event

Examples of use cases:

- Notification from AWS Budget threshold  directly to a Slack channel
- Notification of Success/Failure of an AWS Step Function workflow
- Notification of execution logs of a Lambda function

## Project structure

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- aws-slack-alert - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- template.yaml - A template that defines the application's AWS resources.

## How to configure

Edit `template.yaml` file to include your slack params:

- `SLACK_WEBHOOK_PARAMETER`: 'webhook-with-parameter-value'
- `SLACK_USERNAME`: 'your-slack-webhook-name'
- `SLACK_CHANNEL`: 'your-slack-channel'

## Deploy the application

To use the SAM CLI, you need the following tools.

* [Python 3](https://www.python.org/downloads/)
* [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Docker](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```