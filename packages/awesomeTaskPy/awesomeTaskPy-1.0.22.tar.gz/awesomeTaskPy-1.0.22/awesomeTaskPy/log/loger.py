import os
import time
import json
import sys

logerObj = {}


def mkdir(path):
    if not os.path.isdir(os.path.dirname(path)):
        mkdir(os.path.dirname(path))
    if not os.path.isdir(path):
        os.mkdir(path)


class loger():
    __startAt = None
    __taskId = None
    # ��־��ŵ�·��
    __logPath = None
    # ��ʱ��־
    __tmpPath = None
    # ��ʵ��־���·��
    __reaLogPath = None
    # �ָ����
    __SEPARATOR = "<=========>"
    # ���÷���ֵ���·��
    __realResultPath = None
    __queue = None

    def __init__(self, taskId):
        self.__taskId = taskId
        self.num = 1
        self.__logPath = sys.path[0] + "/runtime" + "/" + taskId + "/"
        mkdir(self.__logPath)
        self.__tmpPath = self.__logPath + "tmp.log"
        self.__reaLogPath = self.__logPath + "runtime.log"
        self.__reaLogPath = self.__logPath + "runtime.log"
        self.__reaLogPath = self.__logPath + "input.log"
        self.__realResultPath = self.__logPath + "result.log"
        self.__outputResultPath = self.__logPath + "childrenTask/"
        # ����ϴε��õĽ�� ��������´˽�� �����ӽڵ�ش������Ľڵ�
        if os.path.isfile(self.__realResultPath):
            os.unlink(self.__realResultPath)
        # self.flushTmpLog()

    def setQueue(self, queue):
        self.__queue = queue

    def writeToServer(self, msg):
        self.__queue.send(msg)

    # �����ʱ���� д��������־
    def flushTmpLog(self):
        self.__queue.close()
        if os.path.isfile(self.__tmpPath):
            logString = open(self.__tmpPath, encoding="utf-8").read()
            logString = logString + self.__SEPARATOR
            with open(self.__reaLogPath, "a") as f:
                f.write(logString + '\n')
            os.unlink(self.__tmpPath)

    # д����־
    def write(self, content):
        data = {
            "content": content,
            "event": "ON_TASK_NODE_LOG",
            "taskId": self.__taskId
        }
        self.writeToServer(data)
        return self

    # ������ֵд�뵽�ļ���
    def writeRes(self, content):
        data = {
            "content": content,
            "event": "ON_TASK_NODE_RESULT",
            "taskId": self.__taskId
        }
        self.writeToServer(data)
        return self

    # ������ִ�еĹ��������ɵĲ��� ��������������
    def writeOutputAndFork(self, content):
        with open(self.__outputResultPath + str(self.num) + ".log", "w") as f:
            f.write(json.dumps(content))
        self.num = self.num + 1
        return self

    @staticmethod
    def instance(taskId):
        if (taskId in logerObj.keys()):
            return logerObj[taskId]
        obj = loger(taskId)
        logerObj[taskId] = obj
        return obj
