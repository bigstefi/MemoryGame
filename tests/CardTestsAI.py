import unittest
import pygame
#from src.Card import Card, BACK, FACE

class CardTestsAI(unittest.TestCase):
    def setUp(self):
        self.x = 10
        self.y = 20
        self.width = 50
        self.height = 60
        self.colorFace = (255, 0, 0)
        self.colorBack = (0, 0, 255)
        self.card = Card(self.x, self.y, self.width, self.height, self.colorFace, self.colorBack)
        # Create a dummy pygame surface for drawing
        pygame.display.init()
        self.screen = pygame.display.set_mode((100, 100))

    def tearDown(self):
        pygame.display.quit()

    def test_initial_state(self):
        self.assertEqual(self.card._side, BACK)
        self.assertEqual(self.card._color, self.colorBack)
        rect = self.card.GetRectangle()
        self.assertEqual((rect.x, rect.y, rect.width, rect.height), (self.x, self.y, self.width, self.height))

    def test_swap_side(self):
        self.card.SwapSide()
        self.assertEqual(self.card._side, FACE)
        self.assertEqual(self.card._color, self.colorFace)
        self.card.SwapSide()
        self.assertEqual(self.card._side, BACK)
        self.assertEqual(self.card._color, self.colorBack)

    def test_get_color(self):
        self.assertEqual(self.card.GetColor(), self.colorBack)
        self.card.SwapSide()
        self.assertEqual(self.card.GetColor(), self.colorFace)

    def test_onclick_swaps_and_shows(self):
        # OnClick should swap side and call Show (which sets color)
        self.card.OnClick(self.screen)
        self.assertEqual(self.card._side, FACE)
        self.assertEqual(self.card._color, self.colorFace)
        self.card.OnClick(self.screen)
        self.assertEqual(self.card._side, BACK)
        self.assertEqual(self.card._color, self.colorBack)

    def test_show_sets_color(self):
        # Show should set color based on side
        self.card._side = BACK
        self.card.Show(self.screen)
        self.assertEqual(self.card._color, self.colorBack)
        self.card._side = FACE
        self.card.Show(self.screen)
        self.assertEqual(self.card._color, self.colorFace)

if __name__ == "__main__":
    unittest.main()
