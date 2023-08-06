# newiotclient

## Description
MQTT client for iot.lonelyassistant.com, authentication using JWT 

### Usage

#### Config

    [broker]
    host = 0.0.0.0
    port = 1883
    tls  = False
    ;client_id: xxx-xxxx
    
    [device]
    product_key = LASS-xxxxxxxx
    device_sn = xxxxxx
    register_username = register-xxxxx
    register_password = register-xxxxx
    refresh_jwt_username = jwt-refresh-xxxxx
    refresh_jwt_password = jwt-refresh-xxxxx
    
#### Subscribe Topic
    
    import time
    from newiotclient.core import MqttJwtToken, JwtMqttClientSub
    
    topic = 'xxxxxx/device/dt/001/LASS-xxxxxx/xxxxxx'
    
    
    def on_message(m_client, userdata, msg):
        print('++++++ get message ++++++')
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))} {msg.payload.decode()}')
        print('++++++ do something here +++++++')
    
    
    def run():
    
        def token_success(token):
            print('============================= get token =================================')
            sub = JwtMqttClientSub(topic=topic, on_message=on_message)
            sub.start()
            sub.join()
    
        mqtt_jwt_token = MqttJwtToken(config_ini='./dev.ini')
        mqtt_jwt_token.on_success = token_success
        mqtt_jwt_token.retrieving()
    
    
    if __name__ == '__main__':
        run()

#### Publish Topic

    import time
    from newiotclient.core import MqttJwtToken, JwtMqttClientPub
    
    topic = 'xxxxxx/device/dt/001/LASS-xxxxxx/xxxxxx'
    
    
    def token_success(token):
        print('============================= get token =================================')
        while True:
            payload = 'hello'
            sub = JwtMqttClientPub(topic=topic, payload=payload)
            sub.start()
            sub.end()
            sub.join()
    
            time.sleep(5)
    
    
    def run():
        mqtt_jwt_token = MqttJwtToken(config_ini='./dev.ini')
        mqtt_jwt_token.on_success = token_success
        mqtt_jwt_token.retrieving()
    
    
    if __name__ == '__main__':
        run()

### Issues
https://github.com/laonan/newiot-pyclient/issues
