import uuid
import pprint

class FunctionContext:
    TYPE = "function_context"

    def __init__(self, start_time, end_time, arguments, keyword_arguments, function_return=None, exec_traceback=None):
        self._start_time = start_time
        self._end_time = end_time
        self._arguments = arguments
        self._keyword_arguments = keyword_arguments
        self._function_return = function_return
        self._exec_traceback = exec_traceback
        self._step_id = uuid.uuid4().hex
    
    def __repr__(self):
        return pprint.pformat({
            "start_time": self._start_time,
            "end_time": self._end_time,
            "arguments": self._arguments,
            "keyword_arguments": self._keyword_arguments,
            "function_return": self._function_return,
            "exec_traceback": self._exec_traceback,
            "step_id": self._step_id
        })
