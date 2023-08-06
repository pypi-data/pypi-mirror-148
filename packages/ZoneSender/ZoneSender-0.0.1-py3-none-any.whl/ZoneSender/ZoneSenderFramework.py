import json
import os
import typing

from .CanParserNodeClient import CanParserNodeClient
from .CanStackNodeClient import CanStackNodeClient
from .SomeipNodeClient import SomeipNodeClient


class ZoneSenderFramework(object):
    '''
    ZoneSender 的基础类，可以用来实现对硬件的简单控制\n
    该对象有几个成员变量，可以查看相应的对象介绍页面来了解函数列表:\n
        - CanStack: ZoneSender.CanStackNodeClient\n
        - CanParser: ZoneSender.CanParserNodeClient\n
        - SomeipStack: ZoneSender.SomeipNodeClient\n
    通过调用几个成员变量的函数实现各种控制功能\n
    '''
    def __init__(self) -> None:
        super().__init__()
        self.CanStack = CanStackNodeClient()
