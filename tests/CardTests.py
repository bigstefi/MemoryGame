import unittest
#from src.Card import Card
#import Card


class CardTests(unittest.TestCase):
    def setUp(self):
        x : int = 0
        y: int = 0
        width : int = 100
        height : int = 100
        colorFace = (255, 0, 0)
        colorBack = (0, 0, 0)
        self._card = Card(x, y, width, height, colorFace, colorBack)

    def GetRectangle_test(self):
        x : int = 0
        y: int = 0
        width : int = 100
        height : int = 100
        colorFace = (255, 0, 0)
        colorBack = (0, 0, 0)

        card = Card.Card(x, y, width, height, colorFace, colorBack)

        rectangle = card.GetRectangle()

        self.assertIsNotNone(rectangle)
        self.assertEqual(rectangle.x, x)
        self.assertEqual(rectangle.y, y)
        self.assertEqual(rectangle.width, width)
        self.assertEqual(rectangle.height, height)

if __name__ == "__main__":
    unittest.main()