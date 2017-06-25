'''
    Author: Josip Vukoja
    Date created: 6/25/2017
    Date last modified: 6/25/2017
    Python Version: 2.7.9
'''

import minesweeperHufsy
import unittest
from mock import patch, Mock
import StringIO
import sys

class TestMinesweeper(unittest.TestCase):
    def setUp(self):
        self.game = minesweeperHufsy.Game()

    def test_board_creation(self):
        self.assertIsNotNone(self.game)

    #when user enters non integer characters as row and column input
    @patch.object(minesweeperHufsy.Game, 'run')
    def test_check_input_rows_columns_for_ValueError(self, mock_run):
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['s','2'])
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['2','s'])
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['s','s'])
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['sfsd','2'])
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['2','sfsd'])
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['2','sf sd'])
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['sf sd','2'])
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['2','2 2'])
        self.assertRaises(ValueError,self.game.check_input_rows_columns, ['2 2 ','2'])  


    #when user enteres empty string for rows and columns
    @patch.object(minesweeperHufsy.Game, 'run')
    def test_check_input_rows_columns_for_IndexError(self, mock_run):
        self.assertRaises(IndexError,self.game.check_input_rows_columns, [])

    #when user enteres desired rows and columns which are out of range 0 < n,m <= 100 
    @patch.object(minesweeperHufsy.Game, 'run')
    def test_check_input_rows_columns_for_out_of_range_values(self, mock_run):
        #mock_run.return_value = False
        self.assertTrue(self.game.check_input_rows_columns(['-2','2']))
        self.assertTrue(self.game.check_input_rows_columns(['2','-2']))
        self.assertTrue(self.game.check_input_rows_columns(['222','2']))
        self.assertTrue(self.game.check_input_rows_columns(['2','222']))
        self.assertTrue(self.game.check_input_rows_columns(['0','2']))
        self.assertTrue(self.game.check_input_rows_columns(['0','222']))
        self.assertTrue(self.game.check_input_rows_columns(['222','0']))
        self.assertTrue(self.game.check_input_rows_columns(['2','0']))
        self.assertTrue(self.game.check_input_rows_columns(['101','101']))

    def test_find_bombs_around(self):
        self.assertEqual(self.game.find_bombs_around([['*', '*','*','*'], ['.', '.','.','.']],1,0),2)
        self.assertEqual(self.game.find_bombs_around([['*', '*','*','*'], ['.', '.','.','.']],1,2),3)
        self.assertEqual(self.game.find_bombs_around([['*', '*','*','*'], ['.', '.','.','.']],1,3),2)

        self.assertEqual(self.game.find_bombs_around([['*', '*'], ['.', '.']],1,0),2)
        self.assertEqual(self.game.find_bombs_around([['*', '*'], ['.', '.']],1,1),2)

    @patch.object(minesweeperHufsy.Game, 'print_unfinished_input')
    def test_is_row_input_valid(self,mock_print_unfinished_input):
        self.game.m = 6
        self.assertTrue(self.game.is_row_input_valid('..*..*'))
        self.assertTrue(self.game.is_row_input_valid('......'))
        self.assertTrue(self.game.is_row_input_valid('******'))
        self.assertFalse(self.game.is_row_input_valid('**sf**'))
        self.assertFalse(self.game.is_row_input_valid('asdfeg'))

    # if user enters doesn't complete the board field it will be printed out 
    def test_print_unfinished_input(self):
        self.game.n = 3
        self.game.m = 3
        self.game.counter = 2
        self.game.bomb_locations = {'fields': {1: [['.', '.'], ['.', '*']], 2: [['*', '*', '.'], ['.', '.', '.']]}}
        
        # redirects stdout
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        self.game.print_unfinished_input()
        sys.stdout = sys.__stdout__  # Reset redirect.

        self.assertTrue(capturedOutput.getvalue() == "3 3\n**.\n...\n")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
