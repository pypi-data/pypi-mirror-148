import json
import os
import typing

import grpc
from .Protos import (CanParserNode_pb2, CanParserNode_pb2_grpc,
                    CanStackNode_pb2, CanStackNode_pb2_grpc, SomeIpNode_pb2,
                    SomeIpNode_pb2_grpc)

from .ObjIo import CanStackConfig

MAX_MESSAGE_LENGTH = 32*1024*1024

class ZoneSenderFramework(object):
    '''
    ZoneSender的底座
    '''
    def __init__(self) -> None:
        super().__init__()
        self._canStub = CanStackNode_pb2_grpc.CanStackNodeStub(
            channel=grpc.insecure_channel(
                target='{0}:{1}'.format('127.0.0.1', 6001),
                options = [
                    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                ]
            )
        )
        self._canDbParserStub = CanParserNode_pb2_grpc.CanParserNodeStub(
            channel=grpc.insecure_channel(
                target='{0}:{1}'.format('127.0.0.1', 6005),
                options = [
                    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                ]
            )
        )
        self._someipNodeStub = SomeIpNode_pb2_grpc.SomeIpNodeStub(
            channel=grpc.insecure_channel(
                target='{0}:{1}'.format('127.0.0.1', 6002),
                options= [
                    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                ]
            )
        )


    def SetCanStackConfig(
        self,
        configs: typing.List['CanStackConfig']
        ) -> None:
        '''
        设置CAN配置
        用此函数来设置CAN硬件的参数
        '''
        try:
            configs_ = list()
            for config_ in configs:
                configs_.append(
                    CanStackNode_pb2.can_channel_config(
                        channel = config_.channel,
                        bitrate = config_.bitrate,
                        is_fd = config_.isFd,
                        fd_bitrate = config_.fdBitrate,
                        bus_type = config_.busType,
                        app_name = config_.appName,
                    )
                )
            res_ = self._canStub.SetConfigs(
                CanStackNode_pb2.can_channel_configs(
                    configs = configs_
                )
            )
            print('SetCanStackConfig result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def StartCanStack(self) -> None:
        '''
        启动CAN协议栈
        '''
        try:
            res_ = self._canStub.StartCanStack(CanStackNode_pb2.Common__pb2.empty())
            print('StartCanStack result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def StopCanStack(self) -> None:
        '''
        关闭Can协议栈
        '''
        try:
            res_ = self._canStub.StopCanStack(CanStackNode_pb2.Common__pb2.empty())
            print('StopCanStack result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def ClearCanCycTask(self) -> None:
        '''
        关闭所有CAN循环任务
        '''
        try:
            res_ = self._canStub.ClearSend(CanStackNode_pb2.Common__pb2.empty())
            print('ClearCanCycTask result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def AddCanDbFile(self, db_path: 'str') -> None:
        '''
        添加一个DB文件
        '''
        try:
            res_ = self._canDbParserStub.AddDbFile(
                CanParserNode_pb2.db_path(
                    db_path = db_path,
                )
            )
            print('AddCanDbFile result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def SetCanDbConfig(self, config_d: 'dict') -> None:
        '''
        设置CANDBConfig文件
        {
            0: 'PTCANFD',
            1: 'BOCAN'
        }
        '''
        try:
            l_ = list()
            for channel_, cluster_name_ in config_d.items():
                l_.append(CanParserNode_pb2.db_config_pair(
                    channel = channel_,
                    db_name = cluster_name_,
                ))
            res_ = self._canDbParserStub.SetConfig(
                CanParserNode_pb2.db_configs(
                    configs = l_
                )
            )
            print('SetCanDbConfig result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def ClearCanDb(self) -> None:
        '''
        清除所有的CANDB配置
        '''
        try:
            res_ = self._canDbParserStub.Clear(
                CanParserNode_pb2.Common__pb2.empty()
            )
            print('清除所有 CANDB 配置 result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def Clear(self) -> None:
        '''
        清除所有订阅
        停止CAN协议栈
        清除所有的CANDB文件
        '''
        self._ClearSubscribeCanMessage()
        self._ClearSubscribeCanParser()
        self.StopCanStack()
        self.ClearCanDb()
        self.ClearLog()

    def _ClearSubscribeCanParser(self) -> None:
        '''
        清除 Canparser 所有的订阅
        '''
        try:
            res_ = self._canDbParserStub.ClearSubscribe(
                CanParserNode_pb2.Common__pb2.empty()
            )
            print('清除所有 CanParser 的订阅 result: {0}, reason: {0}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def _ClearSubscribeCanMessage(self) -> None:
        '''
        取消对所有 Can Message 的订阅
        '''
        try:
            res_ = self._canStub.ClearSubscribe(
                CanStackNode_pb2.Common__pb2.empty()
            )
            print('清除所有 CanStack 的订阅 result: {0}, reason: {0}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def ClearLog(self) -> None:
        '''
        取消所有的Log
        '''
        try:
            res_ = self._canStub.ClearLogger(CanStackNode_pb2.Common__pb2.empty())
            print('清除所有数据记录任务 result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def GetMqttTopicTree(self) -> 'dict':
        '''
        获取所有的 Mqtt Tree dict 对象
        '''
        try:
            res_ = self._canDbParserStub.GetMqttTopicTreeJson(
                CanParserNode_pb2.Common__pb2.empty()
            )
            parser_json_str_ = res_.str_json
            parser_d_ = json.loads(parser_json_str_)
            return parser_d_
        except Exception as e_:
            print(e_)
            return dict()
        
    def StartSomeIpStack(self, ip_addr: 'str', iface: 'str') -> 'bool':
        '''
        启动 SomeIp 协议栈
        '''
        try:
            res_ = self._someipNodeStub.StartSomeIpStack(
                SomeIpNode_pb2.Common__pb2.net_info(
                    ip_addr = ip_addr,
                    iface = iface
                )
            )
            print('启动Someip协议栈, result: {0}, reason: {1}'.format(res_.result, res_.reason))
            if (not res_.result == 0):
                return False
            return True
        except Exception as e_:
            print(e_)
            return False

    def StopSomeIpStack(self) -> 'bool':
        '''
        关闭 SomeIp 协议栈
        '''
        try:
            res_ = self._someipNodeStub.StopSomeIpStack(
                SomeIpNode_pb2.Common__pb2.empty()
            )
            print('关闭SomeIp协议栈, result: {0}, reason:{1}'.format(res_.result, res_.reason))
            if (not res_.result == 0):
                return False
            return True
        except Exception as e_:
            print(e_)
            return False

    def AddSomeIpArxml(self, arxml_path: 'str') -> 'bool':
        '''
        添加一个 SomeIp Arxml 文件
        可以重复调用添加多个
        '''
        try:
            res_ = self._someipNodeStub.AddSomeIpArxml(
                SomeIpNode_pb2.Common__pb2.file_path(
                    path = arxml_path
                )
            )
            print('加载 SomeIp Arxml 文件 result: {0}, reason: {1}'.format(res_.result, res_.reason))
            if (not res_.result == 0):
                return False
            return True
        except Exception as e_:
            print(e_)
            return False

    def GetSomeIpServiceInfos(self) -> 'dict':
        '''
        获取当前已经加载的 SomeIp Arxml Info
        '''
        try:
            res_ = self._someipNodeStub.GetSomeIpServiceInfos(
                SomeIpNode_pb2.Common__pb2.empty()
            )
            print('获取当前加载的SomeIp Arxml 信息成功')
            return json.loads(res_.json_str_info)
        except Exception as e_:
            print(e_)
            return {}

    def UpdateSomeIpServiceConfig(self, service_name: 'str', instance_id: 'int', service_type: 'str') -> 'bool':
        '''
        更新SomeIp中服务的信息
        in:
            service_id: SomeIp Service ID
            instance_id: SomeIp Service Instance ID
            service_type: consumer | provider | unbind 表示该服务设置为什么类型
        '''
        try:
            res_ = self._someipNodeStub.UpdateSomeipServiceConfig(
                SomeIpNode_pb2.service_tag(
                    service_name = service_name,
                    instance_id = instance_id,
                    service_type = service_type
                )
            )
            print('更新 SomeIp 服务设定 result: {0}, reason: {1}'.format(res_.result, res_.reason))
            if (not res_.result == 0):
                return False
            return True
        except Exception as e_:
            print(e_)
            return False

    def SomeIpStackReset(self) -> 'bool':
        '''
        复位 SomeIp 协议栈，并清空 SomeIp 服务配置
        '''
        try:
            res_ = self._someipNodeStub.Reset(
                SomeIpNode_pb2.Common__pb2.empty()
            )
            print('复位 SomeIp 协议栈 result: {0}, reason: {1}'.format(res_.result, res_.reason))
            if (not res_.result == 0):
                return False
            return True
        except Exception as e_:
            print(e_)
            return False

    def GetSomeIpStackStatus(self) -> 'int':
        '''
        获取当前 Someip Stack 的状态

        return
            0 正在运行
            1 协议栈未启动
            2 协议栈未初始化
            1000 Error
        '''
        try:
            res_ = self._someipNodeStub.GetSomeipStackStatus(
                SomeIpNode_pb2.Common__pb2.empty()
            )
            return res_.result
        except Exception as e_:
            print(e_)
            return 1000