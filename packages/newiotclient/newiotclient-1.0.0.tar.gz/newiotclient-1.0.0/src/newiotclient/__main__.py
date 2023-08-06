import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parse_args():
    parse = ArgumentParser(description='CLI for newiotclient')
    parse.add_argument('action', help='action jwt cache')
    args = parse.parse_args()
    return args


if __name__ == '__main__':
    action = parse_args().action
    if action == 'clean':
        try:
            os.remove('./jwt_token.p')
            print('Jwt cache cleaned!')
        except FileNotFoundError:
            print('No jwt cache yet!')

