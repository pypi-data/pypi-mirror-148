import config
import os 
from costack_sdk.costack_workflow.constants import DEBUG_ENVIRON_KEY, LAMBDA_EVENT_KEY, LAMBDA_CONTEXT_KEY, LAMBDA_RETURN_KEY
from costack_sdk.costack_workflow.context.runtime_context import RuntimeContext

def lambda_runtime(handler):
    config.runtime = RuntimeContext(os.environ.get(DEBUG_ENVIRON_KEY) == "True")
    def wrapper_handler(event, context):
        config.runtime.add_entry_context(LAMBDA_EVENT_KEY, event)
        config.runtime.add_entry_context(LAMBDA_CONTEXT_KEY, context)
        lambda_return = handler(event, context)
        config.runtime.add_exit_context(LAMBDA_RETURN_KEY, lambda_return)
        return lambda_return
    return wrapper_handler
