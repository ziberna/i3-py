import i3wsbar
import unittest
import time

class BarTest(unittest.TestCase):
    def setUp(self):
        self.bar = i3wsbar.i3wsbar()
    
    def test_bar_connected(self):
        self.assertTrue(self.bar.socket.connected)
    
    def test_colors(self):
        workspaces = self.bar.socket.get('get_workspaces')
        self.assertIsNotNone(workspaces)
        for workspace in workspaces:
            print(self.bar.colors.get_color(workspace))
    
    def test_format(self):
        workspaces = self.bar.socket.get('get_workspaces')
        self.assertIsNotNone(workspaces)
        print(self.bar.format(workspaces))
    
    def tearDown(self):
        self.bar.quit()
        self.bar = None

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BarTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
