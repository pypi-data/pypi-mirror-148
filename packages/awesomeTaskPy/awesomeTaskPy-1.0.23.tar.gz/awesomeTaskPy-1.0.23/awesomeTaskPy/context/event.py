import sys
import os

eventMap = {}


class event:
    @staticmethod
    def kill(err=None):
        sys.stdout.close()
        if err != None:
            sys.stderr.write(err)
        sys.stderr.close()
        if err!=None:
            os._exit(1)
        else:
            os._exit(0)

    @staticmethod
    def register(name, fun):
        if name not in eventMap:
            eventMap[name] = []
        eventMap[name].append(fun)

    @staticmethod
    def dispatch(event, params):
        if event in eventMap.keys():
            for i in eventMap[event]:
                i(params)
