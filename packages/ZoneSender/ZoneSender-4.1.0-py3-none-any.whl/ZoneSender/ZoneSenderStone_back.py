import json
import os
import time
import typing
import uuid
from concurrent.futures import ThreadPoolExecutor

import grpc
import paho.mqtt.client as mqtt

from .ObjIo import (CanFrame, CanISignalIPdu, CanMessage, CanSignal,
                    SomeipPackage)
from .Protos import (CanParserNode_pb2, CanParserNode_pb2_grpc,
                     CanStackNode_pb2, CanStackNode_pb2_grpc, SomeIpNode_pb2,
                     SomeIpNode_pb2_grpc)

MAX_MESSAGE_LENGTH = 32*1024*1024
class ZoneSenderStone(object):
    def __init__(self) -> None:
        super().__init__()
        ########################################
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
        self._threadPool = ThreadPoolExecutor(2)
        self._mqttClient = mqtt.Client(
            client_id=uuid.uuid4().hex,
            transport='websockets')
        self._mqttClient.on_connect = self._OnMqttConnect
        self._mqttClient.on_message = self._OnMqttMessage
        self._mqttClient.on_disconnect = self._OnMqttDisconnect
        self._mqttClient.connect('127.0.0.1', 8083)
        self._mqttClient.loop_start()
        
    @typing.overload
    def Subscribe(self, can_message: 'CanMessage') -> None:
        ...
    @typing.overload
    def Subscribe(self, can_frame: 'CanFrame') -> None:
        ...
    @typing.overload
    def Subscribe(self, can_signal: 'CanSignal') -> None:
        ...
    @typing.overload
    def Subscribe(self, can_pdu: 'CanISignalIPdu') -> None:
        ...
    @typing.overload
    def Subscribe(self, someip_package: 'SomeipPackage') -> None:
        ...
    @typing.overload
    def Subscribe(self, topic: 'str') -> None:
        ...
    def Subscribe(self, *args) -> None:
        '''
        订阅事件
        '''
        obj_ = args[0]
        if (isinstance(obj_, CanMessage)):
            self._mqttClient.subscribe('zonesender/canstacknode/message/{0}/{1}'.format(obj_.channel, hex(obj_.arbitration_id).lower()))
            self._mqttClient.publish(
                topic='zonesender/canstacknode/subscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'channel': obj_.channel,
                    'arbitration_id': obj_.arbitration_id,
                }).encode('utf-8')
            )
        elif (isinstance(obj_, CanFrame)):
            self._mqttClient.subscribe('zonesender/canparsernode/frame/{0}/{1}'.format(obj_.channel, obj_.name))
            self._mqttClient.publish(
                topic='zonesender/canparsernode/subscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'channel': obj_.channel,
                    'name': obj_.name,
                    'type': 'frame',
                }).encode('utf-8')
            )
        elif (isinstance(obj_, CanSignal)):
            self._mqttClient.subscribe('zonesender/canparsernode/signal/{0}/{1}'.format(obj_.channel, obj_.name))
            self._mqttClient.publish(
                topic='zonesender/canparsernode/subscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'channel': obj_.channel,
                    'name': obj_.name,
                    'type': 'signal',
                }).encode('utf-8')
            )
        elif (isinstance(obj_, CanISignalIPdu)):
            self._mqttClient.subscribe('zonesender/canparsernode/pdu/{0}/{1}'.format(obj_.channel, obj_.name))
            self._mqttClient.publish(
                topic='zonesender/canparsernode/subscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'channel': obj_.channel,
                    'name': obj_.name,
                    'type': 'pdu',
                }).encode('utf-8')
            )
        elif (isinstance(obj_, str)):
            self._mqttClient.subscribe(obj_)
        elif (isinstance(obj_, SomeipPackage)):
            if (obj_.serviceName == ''):
                print('不能订阅空的 someip service')
                return
            self._mqttClient.subscribe('zonesender/someipnode/someippackage/{0}'.format(obj_.serviceName))
            self._mqttClient.publish(
                topic='zonesender/someipnode/subscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'service_name': obj_.serviceName
                }).encode('utf-8')
            )
    
    @typing.overload
    def UnSubscribe(self, can_message: 'CanMessage') -> None:
        ...
    @typing.overload
    def UnSubscribe(self, can_frame: 'CanFrame') -> None:
        ...
    @typing.overload
    def UnSubscribe(self, can_pdu: 'CanISignalIPdu') -> None:
        ...
    @typing.overload
    def UnSubscribe(self, can_signal: 'CanSignal') -> None:
        ...
    @typing.overload
    def UnSubscribe(self, someip_package: 'SomeipPackage') -> None:
        ...
    @typing.overload
    def UnSubscribe(self, topic: 'str') -> None:
        ...
    def UnSubscribe(self, *args) -> None:
        '''
        取消订阅事件
        '''
        obj_ = args[0]
        if (isinstance(obj_, CanMessage)):
            self._mqttClient.unsubscribe('zonesender/canstacknode/message/{0}/{1}'.format(obj_.channel, hex(obj_.arbitration_id).lower()))
            self._mqttClient.publish(
                topic='zonesender/canstacknode/unsubscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'channel': obj_.channel,
                    'arbitration_id': obj_.arbitration_id,
                }).encode('utf-8')
            )
        elif (isinstance(obj_, CanFrame)):
            self._mqttClient.unsubscribe('zonesender/canparsernode/frame/{0}/{1}'.format(obj_.channel, obj_.name))
            self._mqttClient.publish(
                topic='zonesender/canparsernode/unsubscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'channel': obj_.channel,
                    'name': obj_.name,
                    'type': 'frame',
                }).encode('utf-8')
            )
        elif (isinstance(obj_, CanISignalIPdu)):
            self._mqttClient.unsubscribe('zonesender/canparsernode/pdu/{0}/{1}'.format(obj_.channel, obj_.name))
            self._mqttClient.publish(
                topic='zonesender/canparsernode/unsubscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'channel': obj_.channel,
                    'name': obj_.name,
                    'type': 'pdu',
                }).encode('utf-8')
            )
        elif (isinstance(obj_, CanSignal)):
            self._mqttClient.unsubscribe('zonesender/canparsernode/signal/{0}/{1}'.format(obj_.channel, obj_.name))
            self._mqttClient.publish(
                topic='zonesender/canparsernode/unsubscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'channel': obj_.channel,
                    'name': obj_.name,
                    'type': 'signal',
                }).encode('utf-8')
            )
        elif (isinstance(obj_, SomeipPackage)):
            self._mqttClient.unsubscribe('zonesender/someipnode/someippackage/{0}'.format(obj_.serviceName))
            self._mqttClient.publish(
                topic='zonesender/someipnode/unsubscribe',
                payload=json.dumps({
                    'client_id': self._mqttClient._client_id.decode('utf-8'),
                    'service_name':obj_.serviceName
                }).encode('utf-8')
            )

    def OnCanFrame(self, timestamp: 'float', can_frame: 'CanFrame') -> None:
        '''
        当收到一个CAN报文应该做什么
        此函数在收到任何 CAN 报文的时候触发
        '''
        pass

    def OnCanPdu(self, timestamp: 'float', can_pdu: 'CanISignalIPdu') -> None:
        '''
        收到一个CANPDU的时候做什么
        '''
        pass

    def OnCanSignal(self, timestamp: 'float', can_signal: 'CanSignal') -> None:
        '''
        收到一个CANSignal的时候做什么
        '''
        pass

    def OnCanMessage(self, timestamp: 'float', can_message: 'CanMessage') -> None:
        '''
        收到一个 CANMessage 的时候做什么
        '''
        pass

    def OnSomeipPackage(self, timestamp: 'float', someip_package: 'SomeipPackage') -> None:
        '''
        收到一个 someip 包做什么
        '''
        pass

    @typing.overload
    def SendCan(self, msg: 'CanMessage') -> None:
        ...
    @typing.overload
    def SendCan(self, msg: 'CanISignalIPdu') -> None:
        ...
    def SendCan(self, *args) -> None:
        '''
        发送一条CAN报文
        '''
        obj_ = args[0]
        try:
            if (isinstance(obj_, CanMessage)):
                d_ = {
                    'id': obj_.arbitration_id,
                    'ext': obj_.is_extended_id,
                    'rem': obj_.is_remote_frame,
                    'chl': obj_.channel,
                    'dlc': obj_.dlc,
                    'd': obj_.data,
                    'fd': obj_.is_fd,
                }
                self._mqttClient.publish(
                    topic='zonesender/canstacknode/requests/send_can_message',
                    payload=json.dumps(d_).encode('utf-8')
                )
            elif (isinstance(obj_, CanISignalIPdu)):
                d_ = {
                    'name': obj_.name,
                    'chl': obj_.channel,
                    'context': obj_.context,
                }
                self._mqttClient.publish(
                    topic='zonesender/canparsernode/requests/send_can_pdu',
                    payload=json.dumps(d_).encode('utf-8')
                )
        except Exception as e_:
            print(e_)

    def StartLog(
        self, 
        name: 'str', 
        file_path: 'str', 
        channels: typing.List['int'],
        max_log_time_minute: 'int' = 60) -> None:
        '''
        启动一个记录任务
        '''
        try:
            abs_file_path_ = os.path.abspath(file_path)
            res_ = self._canStub.StartLog(
                CanStackNode_pb2.log_start_request(
                    name = name,
                    file_path = abs_file_path_,
                    max_log_time_minute = max_log_time_minute,
                    channels = channels,
                )
            )
            print('StartLog reasut: {0} reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    @typing.overload
    def SetCycleSendTask(self, period_ms: 'int', can_msg: 'CanMessage', times: 'int' = -1) -> None:
        ...
    @typing.overload
    def SetCycleSendTask(self, period_ms: 'int', can_frame: 'CanISignalIPdu', times: 'int' = -1) -> None:
        ...
    @typing.overload
    def SetCycleSendTask(self, period_ms: 'int', can_frame: 'CanFrame', times: 'int' = -1) -> None:
        ...
    def SetCycleSendTask(self, *args) -> None:
        '''
        设置, 修改, 取消, 定时任务
        '''
        period_ms_ = int(args[0])
        obj_ = args[1]
        times_ = int(args[2]) if (len(args) == 3) else -1
        try:
            if (isinstance(obj_, CanMessage)):
                # 设置循环发送 CanMessage
                d_ = {
                    'name': obj_.name,
                    'id': obj_.arbitration_id,
                    'ext': obj_.is_extended_id,
                    'rem': obj_.is_remote_frame,
                    'chl': obj_.channel,
                    'dlc': obj_.dlc,
                    'd': obj_.data,
                    'fd': obj_.is_fd,
                    'times': times_,
                    'period': period_ms_,
                }
                self._mqttClient.publish(
                    topic='zonesender/canstacknode/requests/send_can_message_cyc',
                    payload=json.dumps(d_).encode('utf-8')
                )
            elif (isinstance(obj_, CanFrame)):
                # 设置循环发送 CanFrame
                d_ = {
                    'name': obj_.name,
                    'chl': obj_.channel,
                    'times': times_,
                    'period': period_ms_,
                    'd': [],    # TODO 暂时保留 d 来发送空数据，保持接口一致
                    'context': obj_.context,
                }
                self._mqttClient.publish(
                    topic='zonesender/canparsernode/requests/send_can_frame_cyc',
                    payload=json.dumps(d_).encode('utf-8')
                )
            elif (isinstance(obj_, CanISignalIPdu)):
                # 设置循环发送 CAN PDU
                d_ = {
                    'name': obj_.name,
                    'chl': obj_.channel,
                    'context': obj_.context,
                    'times': times_,
                    'period': period_ms_,
                }
                self._mqttClient.publish(
                    topic='zonesender/canparsernode/requests/send_can_pdu_cyc',
                    payload=json.dumps(d_).encode('utf-8')
                )
        except Exception as e_:
            print(e_)

    def StopLog(
        self, 
        name: 'str') -> None:
        '''
        停止一个记录任务
        '''
        try:
            res_ = self._canStub.StopLog(
                CanStackNode_pb2.log_stop_request(
                    name = name,
                )
            )
            print('StopLog result: {0}, reason: {1}'.format(res_.result, res_.reason))
        except Exception as e_:
            print(e_)

    def SomeipCallAsync(self, someip_package: 'SomeipPackage') -> None:
        '''
        作为 Client调用，请求一个 someip method | get | set
        '''
        try:
            d_ = {
                'sv_name': someip_package.serviceName,
                'ince_id': someip_package.instanceId,
                'if_name': someip_package.interfaceName,
                'if_type': someip_package.interfaceType,
                'context': someip_package.context
            }
            self._mqttClient.publish(
                topic='zonesender/someipnode/request/call',
                payload=json.dumps(d_).encode('utf-8')
            )
        except Exception as e_:
            print(e_)

    def SomeipSetDefaultAnswer(self, someip_package: 'SomeipPackage') -> None:
        '''
        作为 Server 调用，设置后台 SomeIpServer 的数据
        '''
        try:
            d_ = {
                'sv_name': someip_package.serviceName,
                'ince_id': someip_package.instanceId,
                'if_name': someip_package.interfaceName,
                'if_type': someip_package.interfaceType,
                'context': someip_package.context
            }
            self._mqttClient.publish(
                topic='zonesender/someipnode/request/setvalue',
                payload=json.dumps(d_).encode('utf-8')
            )
        except Exception as e_:
            print(e_)

    def SomeipPublish(self, someip_package: 'SomeipPackage') -> None:
        '''
        作为 Server 调用，发送一次 Notification 或者 Event
        '''
        try:
            d_ = {
                'sv_name': someip_package.serviceName,
                'ince_id': someip_package.instanceId,
                'if_name': someip_package.interfaceName,
                'if_type': someip_package.interfaceType,
                'context': someip_package.context
            }
            self._mqttClient.publish(
                topic='zonesender/someipnode/request/publish',
                payload=json.dumps(d_).encode('utf-8')
            )
        except Exception as e_:
            print(e_)

    
    def SomeipCallSync(self, someip_package_in: 'SomeipPackage', someip_package_out: 'SomeipPackage', timeout: 'int' = 1000) -> 'int':
        '''
        同步调用 SomeipCall

        return:
            0: 收到回复
            1: 超时
            1000: 异常
        '''
        try:
            d_ = {
                'sv_name': someip_package_in.serviceName,
                'ince_id': someip_package_in.instanceId,
                'if_name': someip_package_in.interfaceName,
                'if_type': someip_package_in.interfaceType,
                'context': someip_package_in.context
            }
            res_ = self._someipNodeStub.SomeipCallSync(
                SomeIpNode_pb2.someip_call_context(
                    timeout = timeout,
                    str_context = json.dumps(d_)
                )
            )
            result_ = res_.result
            if (result_ == 0):
                # 成功回复
                recv_d_ = json.loads(res_.str_context)
                someip_package_out.srcIp = recv_d_['src_ip']
                someip_package_out.srcPort = recv_d_['src_port']
                someip_package_out.destIp = recv_d_['dest_ip']
                someip_package_out.destPort = recv_d_['dest_port']
                someip_package_out.interfaceType = recv_d_['type']
                someip_package_out.serviceId = recv_d_['sv_id']
                someip_package_out.instanceId = recv_d_['ince_id']
                someip_package_out.interfaceId = recv_d_['if_id']
                someip_package_out.interfaceName = recv_d_['if_name']
                someip_package_out.context = recv_d_['context']
                return 0
            else:
                print(res_.reason)
                return result_
        except Exception as e_:
            print(e_)
            return 1000
            
    def CanEncode(
        self, 
        can_obj: typing.Optional['CanISignalIPdu']) -> int:
        '''
        对 CAN 对象进行编码
        
        Args:\n
            can_obj CanISignalIPdu

        return:\n
            0              编码成功\n
            -1             类型不对\n
            1              找不到对应的通道\n
            2              找不到对应的 PDU 名字\n
            3              找不到 PDU context 中指定的信号名\n
            1000           Error\n
        '''
        try:
            if (isinstance(can_obj, CanISignalIPdu)):
                res_ = self._canDbParserStub.EncodePdu(
                    CanParserNode_pb2.i_signal_i_pdu_obj(
                        channel=can_obj.channel,
                        pdu_name=can_obj.name,
                        pdu_context=json.dumps(can_obj.context)
                    )
                )
                result_ = res_.result.result
                if (result_ == 0):
                    can_obj.data = res_.data
                else:
                    print(res_.result.reason)
                return result_
            else:
                return -1
        except Exception as e_:
            print(e_)
            return 1000



    def _OnMqttMessage(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage) -> None:
        '''
        当收到MQTTMwssage的时候做什么
        '''
        topic_split_ = msg.topic.split('/')
        # print(msg.topic)
        # 消息分发
        if (topic_split_[1] == 'canstacknode'):
            recv_d_ = json.loads(msg.payload.decode('utf-8'))
            # 收到 CAN 数据
            if (topic_split_[2] == 'message'):
                # 收到 CANMessage
                self._DealWithCanMessage(recv_d_)
        elif (topic_split_[1] == 'canparsernode'):
            recv_d_ = json.loads(msg.payload.decode('utf-8'))
            # print(recv_d_)
            if (topic_split_[2] == 'frame'):
                # 收到 CanFrame
                self._DealWithCanFrame(recv_d_)
            elif (topic_split_[2] == 'signal'):
                # 收到CANSIgnal
                self._DealWithCanSignal(recv_d_)
            elif (topic_split_[2] == 'pdu'):
                # 收到CANPdu
                self._DealWithCanISignalIPdu(recv_d_)
        elif (topic_split_[1] == 'out'):
            print(msg.payload.decode('utf-8'))
        elif (topic_split_[1] == 'someipnode'):
            recv_d_ = json.loads(msg.payload.decode('utf-8'))
            if (topic_split_[2] == 'someippackage'):
                # 收到 SomeipPackage
                # print(recv_d_)
                self._DealWithSomeipPackage(recv_d_)

    def _OnMqttConnect(self, client: mqtt.Client, userdata, flags, rc) -> None:
        '''
        连接到 MQTT Broker 的时候做什么
        '''
        self._mqttClient.subscribe('zonesender/out/info')
        self._mqttClient.subscribe('zonesender/out/warn')
        self._mqttClient.subscribe('zonesender/out/error')
        self._mqttClient.subscribe('zonesender/out/debug')

    def _OnMqttDisconnect(self, client: mqtt.Client, userdata, rc) -> None:
        '''
        当断开与MQTT Broker 连接的时候做什么
        '''
        while (True):
            try:
                client.reconnect()
                break
            except Exception as e_:
                print(e_)
            time.sleep(2)

    def _DealWithCanMessage(self, recv_d: 'dict') -> None:
        '''
        处理接收到的 CaneMessage 消息
        '''
        can_msg_ = CanMessage(
            arbitration_id=recv_d['id'], 
            channel=recv_d['chl'], 
            dlc=recv_d['dlc'], 
            data=recv_d['d'],
            is_fd=recv_d['fd'],
            is_extended_id=recv_d['ext'],
            is_remote_frame=recv_d['rem'])
        self._threadPool.submit(
            self.OnCanMessage,
            recv_d['t'], can_msg_
        )

    def _DealWithCanFrame(self, recv_d: 'dict') -> None:
        '''
        处理收到的 CanFrame 消息
        '''
        can_frame_ = CanFrame(
            name=recv_d['name'],
            channel=recv_d['chl']
        )
        can_frame_.data = recv_d['d']
        can_frame_.dlc = recv_d['dlc']
        can_frame_.id = recv_d['id']
        self._threadPool.submit(
            self.OnCanFrame,
            recv_d['t'], can_frame_
        )

    def _DealWithCanISignalIPdu(self, recv_d: 'dict') -> None:
        '''
        处理收到的 CanISignalIPdu 消息
        '''
        can_pdu_ = CanISignalIPdu(
            name=recv_d['name'],
            channel=recv_d['chl']
        )
        can_pdu_.data = recv_d['d']
        self._threadPool.submit(
            self.OnCanPdu,
            recv_d['t'], can_pdu_
        )

    def _DealWithCanSignal(self, recv_d: 'dict') -> None:
        '''
        处理收到的 CanSignal 消息
        '''
        can_signal_ = CanSignal(
            name=recv_d['name'],
            channel=recv_d['chl'],
            data=recv_d['d'],
            unit=recv_d['u'],
            mean=recv_d['m'],
        )
        self._threadPool.submit(
            self.OnCanSignal,
            recv_d['t'], can_signal_
        )

    def _DealWithSomeipPackage(self, recv_d: 'dict') -> None:
        '''
        处理接收到的 SomeipPackage
        '''
        # print(recv_d)
        someip_package_ = SomeipPackage(recv_d['sv_name'])
        someip_package_.srcIp = recv_d['src_ip']
        someip_package_.srcPort = recv_d['src_port']
        someip_package_.destIp = recv_d['dest_ip']
        someip_package_.destPort = recv_d['dest_port']
        someip_package_.interfaceType = recv_d['type']
        someip_package_.serviceId = recv_d['sv_id']
        someip_package_.instanceId = recv_d['ince_id']
        someip_package_.interfaceId = recv_d['if_id']
        someip_package_.interfaceName = recv_d['if_name']
        someip_package_.context = recv_d['context']
        self._threadPool.submit(
            self.OnSomeipPackage,
            recv_d['t'], someip_package_
        )
