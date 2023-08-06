import boto3 
import os 
# import dotenv 

# storage opetions 
# load storage options 
# maybe should setup the credentials during run time 
# we need a context configuration 
# maybe a table to store the credential for initialization 
# by default can store in the native s3 bucket 

# get the envrionment --> how to connect to our dynamo class we cannot allow you 
# two steps: 1.create a dynamo db for the context  2.save the db name to env 
class CostackContext:
    def __init__(self):
        # load the datasource 
        self.dynamo_table_name = os.getenv("COSTACK_DYNAMO_CONTEXT_TABLE_NAME")
        self.function_id = os.getenv("COSTACK_FUNCTION_ID")
        self.dynamo_client = boto3.resource("dynamodb")
        self._table_exists = False
    
    def load_context(self):
        response = self.dynamo_client.Table(self.dynamo_table_name).get_item(Key={"function_id": self.function_id})
        try:
            context = response['Item']
        except Exception as e:
            print(f"failed to load the context {e}")
        return context 
    
    def save_context(self, context): 
        response = self.dynamo_client.Table(self.dynamo_table_name).update_item(
            Key={
                'function_id': self.function_id
            },
            UpdateExpression="set costack_context = :r",
            ExpressionAttributeValues={
                ':r': context,
            },
            ReturnValues="UPDATED_NEW"
        )
        return response 





if __name__ == "__main__":
    # pass 
    os.environ["COSTACK_DYNAMO_CONTEXT_TABLE_NAME"] = "costack_context_ae3978e0-fa28-468a-8770-29bfd37f9281"
    os.environ["COSTACK_FUNCTION_ID"] = "test-func1"
    cc = CostackContext()
    # cc.save_context({"name":1})
    print(cc.load_context())
