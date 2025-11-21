import unittest
#from src.GameTable import GameTable

class GameTableTests(unittest.TestCase):
    def setUp(self):
        self.width = 800
        self.height = 600
        self.card_count = 8
        self.game_table = GameTable(self.width, self.height, self.card_count)

    def test_initialization(self):
        self.assertEqual(self.game_table._width, self.width)
        self.assertEqual(self.game_table._height, self.height)
        self.assertEqual(self.game_table._cardCount, self.card_count)
        self.assertEqual(len(self.game_table._cards), self.card_count)
        self.assertFalse(self.game_table._solved)

    def test_define_card_colors(self):
        colors = self.game_table.DefineCardColors(8)
        self.assertEqual(len(colors), 4)
        self.assertTrue(all(isinstance(c, tuple) and len(c) == 3 for c in colors))

    def test_calculate_rows_columns(self):
        rows, columns = self.game_table.CalculateRowsColumns(8)
        self.assertEqual(rows * columns, 8)

    def test_get_random_colors(self):
        colors = self.game_table.DefineCardColors(8)
        random_colors = self.game_table.GetRandomColors(colors)
        self.assertEqual(len(random_colors), 8)
        self.assertCountEqual(random_colors[:4] + random_colors[4:], colors * 2)

    def test_is_solved_initial(self):
        self.assertFalse(self.game_table.IsSolved())

    def test_get_statistics_initial(self):
        stats = self.game_table.GetStatistics()
        self.assertIn("Clicks", stats)
        self.assertIn("Precision", stats)
        self.assertEqual(stats["Clicks"], 0)

if __name__ == "__main__":
    unittest.main()
