from matrix_client.api import MatrixHttpApi


class MatrixClient:
    '''
    :param server: Matrix server to use.
    :param token: Matrix token.
    :param room: Room id for sending data.
    '''

    def __init__(self, server: str, token: str, room: str):
        self.server = server
        self.token = token
        self.room = room

        self.api = MatrixHttpApi(self.server, token=self.token)
        self.api.initial_sync()

    @classmethod
    def from_config(cls, config):
        server = config['server'].get()
        room = config['room'].get()
        token = config['token'].get()

        return cls(server, token, room)

    def send_event(self, event_type, content):
        return self.api.send_message_event(self.room, event_type, content)

    @staticmethod
    def get_token(server: str, user: str, password: str) -> str:
        return MatrixHttpApi(server).login("m.login.password",
                                           user=user,
                                           password=password)
