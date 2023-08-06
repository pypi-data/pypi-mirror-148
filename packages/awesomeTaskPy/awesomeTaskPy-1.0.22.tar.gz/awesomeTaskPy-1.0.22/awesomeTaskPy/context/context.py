import base64
import json

from awesomeTaskPy.log.loger import loger
from awesomeTaskPy.queue.queue import queue
from awesomeTaskPy.context.systemEventRegister import systemEventRegister
import sys

contextObj = None


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


class context():
    __taskInfo = None
    __log = None
    __queue = None

    def __init__(self, taskInfo):
        if taskInfo is not None:
            self.__taskInfo = taskInfo
            self.__log = loger.instance(self.__taskInfo['taskId'])
            self.__queue = queue(taskInfo)
            self.__log.setQueue(self.__queue)

    def getTaskInfo(self):
        return self.__taskInfo

    def getTaskInfoExtendParams(self, key, default=None):
        if 'extendParams' not in self.__taskInfo.keys():
            return default
        extendParams = self.__taskInfo['extendParams']
        if key not in extendParams:
            return default
        return extendParams[key]

    def getLoger(self):
        return self.__log

    def getQueue(self):
        return self.__queue


def getContext():
    global contextObj
    if contextObj is None:
        contextObj = context(json.loads(sys.argv[1]))
    return contextObj


def initContext():
    global contextObj
    if contextObj != None:
        return contextObj
    if len(sys.argv) >= 2:
        taskInfo = json.loads(base64.b64decode(sys.argv[1]))
        if not isinstance(taskInfo, dict):
            taskInfo = json.loads(taskInfo)
        contextObj = context(taskInfo)
        # ע��ϵͳ�¼�  ע���¼�����ò�Ҫ�������Ĵ���
        # �����¼��ĵ������ڽ��ܽڵ㴫����߳���
        # �ڴ��¼�����ִ�����֮ǰ�����ȡ���ڵ㷵�ص�����
        systemEventRegister.register()
    else:
        contextObj = context(None)
        raise Exception("context failed find taskInfo from command")
