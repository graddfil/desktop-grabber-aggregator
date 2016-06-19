import testtools
import confuse
from graddfril.desktop.grabber_aggregator_refimpl import matrix  # pylint:disable=import-error


class TestMatrixClientFromConfig(testtools.TestCase):
    def setUp(self):
        super(TestMatrixClientFromConfig, self).setUp()
        self.config = confuse.Configuration("graddfril")

    def test_init_from_config(self):
        mx_client = matrix.MatrixClient(*[self.config[name].get(str) for name in ['server', 'token', 'room']])
        room_name = mx_client.api.get_room_name(self.config['room'].get(str))['name']

        self.expectThat(room_name, testtools.matchers.IsInstance(str))
