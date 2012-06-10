import i3
import unittest
import platform
py3 = platform.python_version_tuple() > ('3',)

class ParseTest(unittest.TestCase):
    def setUp(self):
        self.msg_types = ['get_tree', 4, '4']
        self.event_types = ['output', 1, '1']
    
    def test_msg_parse(self):
        msg_types = []
        for msg_type in self.msg_types:
            msg_types.append(i3.parse_msg_type(msg_type))
        for index in range(-1, len(msg_types) - 1):
            self.assertEqual(msg_types[index], msg_types[index+1])
            self.assertIsInstance(msg_types[index], int)
    
    def test_event_parse(self):
        event_types = []
        for event_type in self.event_types:
            event_types.append(i3.parse_event_type(event_type))
        for index in range(-1, len(event_types) - 1):
            self.assertEqual(event_types[index], event_types[index+1])
            self.assertIsInstance(event_types[index], str)
    
    def test_msg_type_error(self):
        border_lower = -1
        border_higher = len(i3.MSG_TYPES)
        values = ['joke', border_lower, border_higher, -100, 100]
        for val in values:
            self.assertRaises(i3.MessageTypeError, i3.parse_msg_type, val)
            self.assertRaises(i3.MessageTypeError, i3.parse_msg_type, str(val))
    
    def test_event_type_error(self):
        border_lower = -1
        border_higher = len(i3.EVENT_TYPES)
        values = ['joke', border_lower, border_higher, -100, 100]
        for val in values:
            self.assertRaises(i3.EventTypeError, i3.parse_event_type, val)
            self.assertRaises(i3.EventTypeError, i3.parse_event_type, str(val))
    
    def test_msg_error(self):
        """If i3.yada doesn't pass, see http://bugs.i3wm.org/report/ticket/693"""
        self.assertRaises(i3.MessageError, i3.focus)  # missing argument
        self.assertRaises(i3.MessageError, i3.yada)  # doesn't exist
        self.assertRaises(i3.MessageError, i3.meh, 'some', 'args')
    

class SocketTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_connection(self):
        def connect():
            return i3.Socket('/nil/2971.socket')
        self.assertRaises(i3.ConnectionError, connect)
    
    def test_response(self, socket=i3.default_socket()):
        workspaces = socket.get('get_workspaces')
        self.assertIsNotNone(workspaces)
        for workspace in workspaces:
            self.assertTrue('name' in workspace)
    
    def test_multiple_sockets(self):
        socket1 = i3.Socket()
        socket2 = i3.Socket()
        socket3 = i3.Socket()
        for socket in [socket1, socket2, socket3]:
            self.test_response(socket)
        for socket in [socket1, socket2, socket3]:
            socket.close()
    
    def test_pack(self):
        packed = i3.default_socket().pack(0, "haha")
        if py3:
            self.assertIsInstance(packed, bytes)


class GeneralTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_getattr(self):
        func = i3.some_attribute
        self.assertTrue(callable(func))
        socket = i3.default_socket()
        self.assertIsInstance(socket, i3.Socket)
    
    def test_success(self):
        data = {'success': True}
        self.assertEqual(i3.success(data), True)
        self.assertEqual(i3.success([data, {'success': False}]), [True, False])
        data = {'success': False, 'error': 'Error message'}
        self.assertIsInstance(i3.success(data), i3.MessageError)
    
    def test_container(self):
        container = i3.container(title='abc', con_id=123)
        output = ['[title="abc" con_id="123"]',
                '[con_id="123" title="abc"]']
        self.assertTrue(container in output)

    def test_criteria(self):
        self.assertTrue(i3.focus(clasS='xterm'))
    
    def test_filter1(self):
        windows = i3.filter(nodes=[])
        for window in windows:
            self.assertEqual(window['nodes'], [])
    
    def test_filter2(self):
        unfocused_windows = i3.filter(focused=False)
        parent_count = 0
        for window in unfocused_windows:
            self.assertEqual(window['focused'], False)
            if window['nodes'] != []:
                parent_count += 1
        self.assertGreater(parent_count, 0)
    
    def test_filter_function_wikipedia(self):
        """You have to have a Wikipedia tab opened in a browser."""
        func = lambda node: 'Wikipedia' in node['name']
        nodes = i3.filter(function=func)
        self.assertTrue(nodes != [])
        for node in nodes:
            self.assertTrue('free encyclopedia' in node['name'])

if __name__ == '__main__':
    test_suits = []
    for Test in [ParseTest, SocketTest, GeneralTest]:
        test_suits.append(unittest.TestLoader().loadTestsFromTestCase(Test))
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(test_suits))

