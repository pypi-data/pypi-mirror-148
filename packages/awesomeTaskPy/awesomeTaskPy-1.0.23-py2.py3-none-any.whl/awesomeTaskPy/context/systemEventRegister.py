from awesomeTaskPy.context.event import event
import os
import sys

class systemEventRegister:
    @staticmethod
    def register():
        def callback():
            event.kill()
        event.register('ON_PYTHON_TASK_FINISH', callback)
        pass
