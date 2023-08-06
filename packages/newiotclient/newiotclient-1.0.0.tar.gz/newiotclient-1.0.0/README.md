# newiotclient

## Description
MQTT client for iot.lonelyassistant.com, authentication using JWT 

### Usage
    
    import time
    from newiotclient.core import MqttJwtToken, JwtTokenThread, JwtMqttClient
    
    def on_message(m_client, userdata, msg):
        print('++++++ do something ++++++')
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))} {msg.payload.decode()}')
        
    def run():
        
        # Get these options from iot.lonelyassistant.com
        parameters = {
            'host': '0.0.0.0',
            'port': 1883,
            'tls': False,
            # 'client_id': 'xxx-xxxx',
            'product_key': 'LASS-xxxxxxxxxxxxxxxxxxx',
            'device_sn': 'xxxxxxxxxxxx',
            'register_username': 'register-xxxxxxxx',
            'register_password': 'register-xxxxxxxx',
            'refresh_jwt_username': 'jwt-refresh-xxxxxxxx',
            'refresh_jwt_password': 'jwt-refresh-xxxxxxxx'
        }
        
        topic = 'xxxxxxxx/device/dt/001/LASS-xxxxxxxxxxxxxxxxxxx/xxxxxxxxxxxx'
        
        mqtt_jwt_token = MqttJwtToken(**parameters)
        jwt_thread = JwtTokenThread(mqtt_jwt_token)
        jwt_thread.setDaemon(True)
        jwt_thread.start()
        jwt_thread.join()
        
        jwt_client = JwtMqttClient(loop_forever=False, on_message=on_message)
        jwt_client.sub(topic)

    try:
        while True:
            jwt_client.pub(topic, 'hello')
            time.sleep(5)
    except KeyboardInterrupt:
        jwt_client.end()


    if __name__ == '__main__':
        run()

### Issues
https://github.com/laonan/newiot-pyclient/issues
