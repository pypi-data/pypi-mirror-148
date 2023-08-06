from awesomeTaskPy.context.event import event
import os


class systemEventRegister:
    @staticmethod
    def register():
        def callback():
            os._exit(1)

        event.register('ON_PYTHON_TASK_FINISH', callback)
        pass
