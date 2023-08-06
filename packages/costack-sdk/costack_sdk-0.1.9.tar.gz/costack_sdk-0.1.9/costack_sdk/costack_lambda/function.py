"""
sdk for calling the lambda functions 
seamless experience for using remote lambda functions in your space 
"""
import boto3 
import json 

class CostackFunction:
    def __init__(self, function_name, boto3_session=None):
        self.function_name = function_name 
        # call lambda 
        # use the default boto3 profile: assume everything is in the same account 
        if boto3_session:
            self.client = boto3_session.client('lambda')
        else:
            # user default profile 
            self.client = boto3.client('lambda')

    def call(self, args={},  context=None):
        kwargs = {
            "FunctionName":self.function_name,
            # InvocationType='Event'|'RequestResponse'|'DryRun',
            # LogType='None'|'Tail',
            # ClientContext='string',
            "Payload":json.dumps(args).encode("utf-8")
        }
        if context: 
            # context is a string 
            kwargs['ClientContext'] = str(context)
        response = self.client.invoke(**kwargs)
        response_payload = json.loads(response['Payload'].read().decode("utf-8"))
        return response_payload 

