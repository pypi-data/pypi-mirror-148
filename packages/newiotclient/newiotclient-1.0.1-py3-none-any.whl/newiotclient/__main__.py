import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, ArgumentError
from newiotclient.core import MqttJwtToken


def parse_args():
    parse = ArgumentParser(description='CLI for newiotclient')
    parse.add_argument('action', help='action jwt cache')
    parse.add_argument('-c', '--config', help='config file')
    args = parse.parse_args()
    return args


def token_success(token):
    print(f'Retrieving JWT... {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}')
    print(token)


if __name__ == '__main__':
    action = parse_args().action
    config = parse_args().config
    if action == 'clean':
        MqttJwtToken.clean_token()
    elif action == 'jwt':
        if config is None:
            raise ArgumentError(argument=config, message='fetch jwt need config file -c/--config')
        else:
            mqtt_jwt_token = MqttJwtToken(config_ini=config)
            mqtt_jwt_token.on_success = token_success
            mqtt_jwt_token.retrieving()





