import os
import sys
import time
import uuid
import ssl
import json
import threading
import requests
import pickle
from paho.mqtt import client as mqtt_client


class MqttJwtToken:

    TOKEN_OBJ_NAME = 'jwt_token.p'

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.tls = kwargs['tls']
        self.register_username = kwargs['register_username']
        self.register_password = kwargs['register_password']
        self.refresh_jwt_username = kwargs['refresh_jwt_username']
        self.refresh_jwt_password = kwargs['refresh_jwt_password']

        if 'client_id' not in kwargs or kwargs['client_id'] is None:
            self.client_id = str(uuid.uuid1())
        else:
            self.client_id = kwargs['client_id']

        self.register_topic_sub = f'lass/dt/register/{kwargs["product_key"]}/{kwargs["device_sn"]}'
        self.register_topic_pub = f'lass/cmd/register/{kwargs["product_key"]}/{kwargs["device_sn"]}'

        self.refresh_topic_sub = f'lass/dt/jwt/refresh/{kwargs["product_key"]}/{kwargs["device_sn"]}'
        self.refresh_topic_pub = f'lass/cmd/jwt/refresh/{kwargs["product_key"]}/{kwargs["device_sn"]}'

    def on_connect(self, m_client, userdata, flags, rc):
        if rc == 0:
            print(f'Connected ({userdata}) to MQTT Broker {self.host} as {self.client_id}!')
            if userdata == 'register':
                print('Start registering...')
                m_client.publish(self.register_topic_pub, payload=json.dumps({"get_jwt": 1}))

            if userdata == 'jwt_token_refresh':
                print('Start refreshing...')
                token = self.get_token()
                payload = {'refresh': token['refresh']}
                m_client.publish(self.refresh_topic_pub, payload=json.dumps(payload))
        else:
            print(f'Failed to connect, return code: {rc}, maybe authorization server return 403.')

    def on_disconnect(self, client, userdata, rc):
        print(f'disconnect from {self.host}:{self.port}')
        print(f'Disconnection returned result: {rc}, userdata: {userdata}')

    def on_message(self, m_client, userdata, msg):
        # print(f"Received {msg.payload.decode()} from {msg.topic} topic qos {msg.qos} {msg.retain}")
        if userdata == 'register' or userdata == 'jwt_token_refresh':
            m_client.disconnect()
            print(f'Received token ({userdata}), disconnect.')
            token_obj = json.loads(msg.payload.decode())
            token_obj['create_cache_time'] = int(time.time())
            token_obj['tls'] = self.tls
            token_obj['host'] = self.host
            token_obj['port'] = self.port
            token_file = open(self.TOKEN_OBJ_NAME, 'wb')
            pickle.dump(token_obj, token_file)
            token_file.close()

            # print(f'Token is cached: {token_obj}')
            print(f'Token is cached.')

            m_client.loop_stop(force=False)
            timer = threading.Timer(token_obj['access_lifetime'], self.refresh_jwt_token)
            timer.start()

    def register(self):
        self.__sub('register')

    def refresh_jwt_token(self):

        token = self.get_token()
        if token is not None:
            time_delta_sec = int(time.time()) - 10 - token['create_cache_time']

            if time_delta_sec >= token['access_lifetime']:
                if time_delta_sec >= token['refresh_lifetime']:
                    print(f'\033[31mRefresh_token expired! please register device again, then try again.\033[0m')
                    print(f'\033[31mBefore registering device, clean jwt cache first: python -m newiotclient clean\033[0m')
                    try:
                        sys.exit(0)
                    except Exception as e:
                        print(f'Refresh_token expired! {str(e)}')
                else:
                    self.__sub('jwt_token_refresh')
        else:
            self.register()

    def __sub(self, userdata):
        if userdata == 'register':
            username = self.register_username
            password = self.register_password
            sub_topic = self.register_topic_sub
        else:
            username = self.refresh_jwt_username
            password = self.refresh_jwt_password
            sub_topic = self.refresh_topic_sub

        client = mqtt_client.Client(self.client_id)
        client.reinitialise(client_id=self.client_id, clean_session=True, userdata=userdata)
        client.username_pw_set(username, password)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        if self.tls:
            client.tls_set(self.get_cert_file(), tls_version=ssl.PROTOCOL_TLSv1_2)
            client.tls_insecure_set(True)
        client.connect(host=self.host, port=self.port)
        print(f'{self.host}:{self.port}')
        print(f'Sub topic ({userdata}): {sub_topic}')
        client.subscribe(sub_topic)
        client.loop_forever()

    @staticmethod
    def get_cert_file():
        return f'{os.path.abspath(os.path.dirname(__file__))}/cert/ca-bundle.crt'

    @classmethod
    def get_token(cls):
        try:
            token_file = open(cls.TOKEN_OBJ_NAME, 'rb')
            token = pickle.load(token_file)
            token_file.close()
            return token
        except (FileNotFoundError, EOFError):
            return None


class JwtTokenThread(threading.Thread):
    def __init__(self, mqtt_jwt_token):
        thread_name = 'jwt_token_thread'
        super().__init__(name=thread_name)

        self.mqtt_jwt_token = mqtt_jwt_token

    def run(self) -> None:
        self.mqtt_jwt_token.refresh_jwt_token()


class JwtMqttClient:
    def __init__(self, loop_forever=True, on_connect=None, on_disconnect=None, on_message=None, on_subscribe=None,
                 on_publish=None):

        token = MqttJwtToken.get_token()
        # client_id = token['client_id']
        # client = mqtt_client.Client(client_id)
        client = mqtt_client.Client()
        is_tls = token['tls']
        if is_tls:
            client.tls_set(MqttJwtToken.get_cert_file(), tls_version=ssl.PROTOCOL_TLSv1_2)
            client.tls_insecure_set(True)
        client.username_pw_set(token['access'], 'jwt')

        # callback functions
        client.on_connect = self.on_connect if on_connect is None else on_connect
        client.on_disconnect = self.on_disconnect if on_disconnect is None else on_disconnect
        client.on_message = self.on_message if on_message is None else on_message
        client.on_subscribe = self.on_subscribe if on_subscribe is None else on_subscribe
        client.on_publish = self.on_publish if on_publish is None else on_publish

        client.connect(host=token['host'], port=token['port'])
        if not loop_forever:
            client.loop_start()

        self.loop_forever = loop_forever
        self.no_response_sub = []  # 未获得服务器响应的订阅消息 id 列表
        self.client = client

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print(f'Connection returned with result code: {rc}')

    @staticmethod
    def on_message(client, userdata, msg):
        print(f'Received message, topic: {msg.topic} payload: {msg.payload.decode()}')

    @staticmethod
    def on_disconnect(client, userdata, rc):
        print(f'Disconnection returned result: {rc}')

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.no_response_sub.remove(mid)

    @staticmethod
    def on_publish(client, userdata, mid):
        print(f'Published {mid}')

    def end(self):
        if not self.loop_forever:
            self.client.loop_stop()
        self.client.disconnect()

    def sub(self, topic):
        # multiple topics: [('topic1', 0), ('topic2', 0)]
        result, mid = self.client.subscribe(topic)
        self.no_response_sub.append(mid)
        if self.loop_forever:
            self.client.loop_forever()

    def pub(self, topic, payload):
        self.client.publish(topic=topic, payload=payload)
