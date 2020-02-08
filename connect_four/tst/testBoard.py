import unittest

# if __package__ is None:
#     import sys
#     from os import path
#     sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#     from src.board import *
# else:
#     from ..src.board import *

from ..src.board import *

class TestBoard(unittest.TestCase):

    def testSimple(self):
        b = Board()
        b.put(Color.RED, 1)
        self.assertFalse(b.gameOver())


if __name__ == '__main__':
    unittest.main()