import argparse
import getpass
import confuse
from graddfril.desktop.grabber_aggregator_refimpl.matrix import MatrixClient


def update_config(config: confuse.Configuration):
    open(config.user_config_path(), 'w').write(config.dump())


class PasswordPromptAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        password = getpass.getpass()
        setattr(namespace, self.dest, password)


def main():
    config = confuse.Configuration('graddfril')

    parser = argparse.ArgumentParser(description='Graddfril grabber aggregator')
    parser.add_argument('-s', '--server')
    parser.add_argument('-r', '--room')
    parser.add_argument('-u', '--user')
    parser.add_argument('-t', '--token')
    parser.add_argument('-p', '--password-prompt', dest='password', nargs=0, action=PasswordPromptAction)
    parser.add_argument('--save-config', action='store_true')
    args = parser.parse_args()

    persistent_args = {k: vars(args)[k] for k in ('server', 'room', 'user', 'token')}

    if args.password:
        persistent_args['token'] = MatrixClient.get_token(args.server, args.user, args.password)['access_token']

    for k, v in persistent_args.items():
        if v is not None:
            config[k] = v

    if args.save_config:
        update_config(config)

    matrix = MatrixClient.from_config(config)
    matrix.send_event("m.room.message", {"msgtype": "m.text",
                                         "body": "Hello world!"})
    matrix.send_event("graddfril.event", {"msgtype": "graddfril.keypress",
                                          "key": "h"})

if __name__ == '__main__':
    main()
