import unittest
import builtins
import sys
import wx
import mwx
import mwx.utilus as mwxu
from mwx.graphman import Layer

app = wx.App()
frame = mwx.Frame(None)

class TestUtilus(unittest.TestCase):

    def test_typename(self):
        values = (
            (wx, "wx"),
            (mwx, "mwx"),
            (frame, "Frame"),
            (mwx.Frame, "Frame"),
            (mwx.funcall, "funcall"),
            (mwx.typename, "typename"),
            (mwx.graphman.Layer, "mwx.graphman:Layer"),
            (mwx.graphman.Layer, "mwx.graphman:Layer"),
        )
        for text, result in values:
            self.assertEqual(mwxu.typename(text), result)
    
    def test_where(self):
        values = (
            (sys, sys),
            (wx, 'C:\\Python39\\lib\\site-packages\\wx\\__init__.py'),
            (mwx, 'C:\\usr\\home\\lib\\python\\Lib\\mwx\\__init__.py'),
            (frame, 'C:\\usr\\home\\lib\\python\\Lib\\mwx\\framework.py'),
            (frame.Update, builtins),
        )
        for text, result in values:
            self.assertEqual(mwxu.where(text), result)

if __name__ == '__main__':
    unittest.main()
