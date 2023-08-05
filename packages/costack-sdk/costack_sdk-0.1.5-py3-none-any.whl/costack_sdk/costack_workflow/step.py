import traceback
import time
import config
from costack_sdk.costack_workflow.context.function_context import FunctionContext
from costack_sdk.costack_workflow.context.runtime_context import RuntimeContext

def step(function, *args, **kwargs):
    # global RUNTIME_CONTEXT
    if config.runtime.debug:
        return function(*args, **kwargs)
    
    start_time = time.time()
    try:
        function_return = function(*args, **kwargs)
        end_time = time.time()
        function_context = FunctionContext(start_time, end_time, list(args), dict(kwargs), function_return = function_return)
        config.runtime.add_step(function_context)
    except Exception as err:
        end_time = time.time()
        exec_traceback = traceback.format_exc()
        function_context = FunctionContext(start_time, end_time, list(args), dict(kwargs), exec_traceback = exec_traceback)
        config.runtime.add_step(function_context)
        raise err
    return function_return
