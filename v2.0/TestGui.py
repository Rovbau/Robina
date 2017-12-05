import unittest
from Gui import *

class ModelMock:
    def addObserver(self, observer):
        pass

class TestGui(unittest.TestCase):

    def testTransform(self):
        self.runTestTransform(0,   0,  10,  12, 1, (310, 312))
        self.runTestTransform(0,   0, -10, -12, 1, (290, 288))
        self.runTestTransform(15,  0,  10,  12, 1, (325, 312))
        self.runTestTransform(0, -20, -10, -12, 1, (290, 268))

    def runTestTransform(self, xOffset, yOffset, x, y, correction, expectedResult):
        gui = Gui(ModelMock(), None)
        gui.xOffset = xOffset
        gui.yOffset = yOffset
        actualResult = gui._transform(x, y, correction)
        self.assertEqual(actualResult, expectedResult)

if __name__ == '__main__':
    unittest.main()
