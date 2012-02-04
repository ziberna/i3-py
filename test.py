import i3
import unittest


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
            self.assertTrue(isinstance(msg_types[index], int))
    
    def test_event_parse(self):
        event_types = []
        for event_type in self.event_types:
            event_types.append(i3.parse_event_type(event_type))
        for index in range(-1, len(event_types) - 1):
            self.assertEqual(event_types[index], event_types[index+1])
            self.assertTrue(isinstance(event_types[index], str))
    
    def test_msg_error(self):
        border_lower = -1
        border_higher = len(i3.msg_types)
        values = ['joke', border_lower, border_higher, -100, 100]
        for val in values:
            self.assertRaises(i3.MessageTypeError, i3.parse_msg_type, val)
            self.assertRaises(i3.MessageTypeError, i3.parse_msg_type, str(val))
    
    def test_event_error(self):
        border_lower = -1
        border_higher = len(i3.event_types)
        values = ['joke', border_lower, border_higher, -100, 100]
        for val in values:
            self.assertRaises(i3.EventTypeError, i3.parse_event_type, val)
            self.assertRaises(i3.EventTypeError, i3.parse_event_type, str(val))
    

class SocketTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_reponse(self):
        workspaces = i3.msg('get_workspaces')
        for workspace in workspaces:
            self.assertTrue('name' in workspace)
    

if __name__ == '__main__':
    for Test in [ParseTest, SocketTest]:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test)
        unittest.TextTestRunner(verbosity=2).run(suite)
