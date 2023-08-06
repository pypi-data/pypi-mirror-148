from typing import List
from costack_sdk.costack_workflow.context.function_context import FunctionContext
import pprint

class RuntimeContext:
    def __init__(self, debug):
        self._debug = debug
        self._entry_context = dict()
        self._exit_context = dict()
        self._steps: List[FunctionContext] = []
    
    def __repr__(self):
        return pprint.pformat({
            "debug": self.debug,
            "entry_context": self.entry_context,
            "exit_context": self.exit_context,
            "steps": self.steps
        })

    @property
    def debug(self):
        return self._debug
    @property
    def steps(self):
        return self._steps
    @property
    def entry_context(self):
        return self._entry_context
    @property
    def exit_context(self):
        return self._exit_context
    
    def add_step(self, step):
        self._steps.append(step)
    
    def add_entry_context(self, key, context):
        self._entry_context[key] = context
    def add_exit_context(self, key, context):
        self._exit_context[key] = context
    
