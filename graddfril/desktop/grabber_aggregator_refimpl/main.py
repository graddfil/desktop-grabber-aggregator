"""Interactive part / CLI."""
import argparse
import getpass
import confuse
import appdirs
from time import sleep
from matrix import MatrixClient  # pylint:disable=import-eoferror

def update_config(config: confuse.Configuration):
    """Update the config file."""
    open(config.user_config_path(), 'w').write(config.dump())


class PasswordPromptAction(argparse.Action):
    """Securely prompt a password."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Use getpass() to set self.dest passed by argparse to input password."""
        password = getpass.getpass()
        setattr(namespace, self.dest, password)


def main():
    """CLI entrypoint."""
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

    for k, val in persistent_args.items():
        if val is not None:
            config[k] = val

    if args.save_config:
        update_config(config)

    matrix = MatrixClient(*[config[name].get() for name in ['server', 'token', 'room']])

    while True:
        if matrix.try_sync():
            matrix.send_event("m.room.message", {"msgtype": "m.text", "body": "Hello world!"})
            matrix.send_event("graddfril.event", {"msgtype": "graddfril.keypress", "key": "h"})
        sleep(100)

if __name__ == '__main__':
    main()
