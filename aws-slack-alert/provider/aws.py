import boto3

class AWS:

    def __init__(self, region='us-east-1'):
        """Class to connect to AWS API

        Args:
            region (str, optional): AWS region name. Defaults to 'us-east-1'.
        """
        self.ssm_client = boto3.client('ssm', region_name=region)

    def get_parameter(self, parameter_name, with_decryption=True):
        """Get AWS SSM Parameter

        Args:
            parameter_name (str): Parameter Name
            with_decryption (bool, optional): AWS System Manager Parameter Store name. Defaults to True.

        Returns:
            str: Parameter value
        """
        return self.ssm_client.get_parameter(Name=parameter_name, WithDecryption=with_decryption)['Parameter']['Value']