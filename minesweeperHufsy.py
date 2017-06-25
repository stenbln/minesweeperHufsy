'''
    Author: Josip Vukoja
    Date created: 6/24/2017
    Date last modified: 6/25/2017
    Python Version: 2.7.9
'''

from __future__ import print_function #used to expand functionality of print_function e.g. print() can now be modified to disable automatic new line

class Game(object):
    def __init__(self):
        self.prompt = [] #used for storing raw user input for number of rows and columns
        self.n = None #rows
        self.m = None #columns
        self.direction_x = [ -1, -1, -1, 0, 0, 1, 1, 1 ] # helper lists for x axis used for traversing neigbouring fields
        self.direction_y = [ -1, 0, 1, -1, 1, -1, 0, 1 ] # helper lists for y axis used for traversing neigbouring fields
        self.counter = 0 # used for counting how many fields are entered
        self.bomb_locations = {'fields':{}} # used for storing all of the user entered and validated 2D matrix data for multiple complete fields e.g. {'fields': {1: [['.', '.'], ['.', '*']], 2: [['.', '.', '.'], ['.', '.', '.'], ['*', '*', '*']]}}

    def solve(self):
        """
        Finds and prints the solution. Creates a solved 2D matrix for each of the keys in a self.bomb_locations['fields'] dictionary

        """
        for key in self.bomb_locations['fields']:
            field_matrix = self.bomb_locations['fields'][key]
            solved_matrix = field_matrix #creates an exact copy of the 2D matrix. Bomb values are calculated and the matrix values are then modified
            
            # loops over 2D matrix. Calculates the number of bombs and populates solved matrix with numbers
            for i in range(len(field_matrix)):
                for j in range(len(field_matrix[i])):
                    if (field_matrix[i][j] == '.'):
                        bombs_around = self.find_bombs_around(field_matrix,i,j)
                        solved_matrix[i][j] = bombs_around
                    elif (field_matrix[i][j] == '*'):
                        solved_matrix[i][j] = '*'
            print ("Field " + "#"+str(key))
            for element in solved_matrix:
                for e in element:
                    print (e, end="") #prints items without adding new line
                print ()
            if (key != self.counter):# makes sure that there isn't a new line on the last item in the dictionary
                print()

    def find_bombs_around(self,field_matrix,i,j):
        """
        Finds the number of bombs around a particular field. 1 field can maximally be surrounded by 8 other fields

        Args:
            field_matrix: 2D matrix that is filled either with either empty fields '.' or bombs '*' .
            i,j: matrix indices of the element whose neigbouring bombs needs to be calculated

        Returns:
            bombs_around: Returns how many bombs are around a particular field. 

        """
        height = len(field_matrix) 
        length = len(field_matrix[0])
        bombs_around = 0
        for n in range(8):
            x = i+self.direction_x[n]
            y = j+self.direction_y[n]

            # make sure that that neighbouring fields are not outside the whole bomb field
            if (x<0 or y<0 or x>=height or y>=length):
                pass
            elif ((field_matrix[x][y]) == '*'):
                bombs_around += 1

        return bombs_around

    def print_unfinished_input(self):
        """
        Prints unifished user input if user enters something wrong e.g. incorrect number of columns or wrong characters
        """
        print (str(self.n) + " " + str(self.m)) # prints last entered rows and columns (e.g. 4 4)
        for element in self.bomb_locations['fields'][self.counter]:
            for e in element:
                print (e, end="") #prints item without adding new line
            print()


    def is_row_input_valid(self,row):
        """
        Checks if the user row input is valid

        Args:
            row: string of '*' and '.' e.g. valid input is '.*.*..' and invalid input is 'sf2.**.ds'

        Returns:
            True or False

        """

        # make sure that there are no other characters in the input except "*" and "."
        for i in row:
            if (i!='*' and i!='.'):
                print ('Please enter only valid characters (e.g. "." or "*")')
                self.print_unfinished_input()
                return False
        # make sure that user input length matches the number of specified columns 
        if (len(row)!=self.m): 
            print ('Please match the correct number of columns')
            self.print_unfinished_input(self)
            return False
        else:
            return True

    def check_input_rows_columns(self,prompt_list):
        """
        Checks is the user input of desired number of rows and columns valid

        Args:
            prompt_list: list of prompted user input e.g. ['4','4']

        Raises:
        ValueError: thrown in case if non-integers are entered for a desired number of rows and columns
        IndexError: thrown in case if empty string is entered as a desired number of rows and columns e.g. '' or []

        """
        try:
            self.n = int(prompt_list[0]) 
            self.m = int(prompt_list[1])

            # if 0 0 and zero input is entered, find the solution and quit the program
            if (self.n==0 and self.m==0):
                self.solve()
                quit()

            elif (self.n<=0 or self.m<=0 or self.n>100 or self.m>100):
                print ("Please make sure that number fall into category 0 < n,m <= 100 ")
                self.run()
                return True #used for testing

        except (ValueError):
             print("Oops!  Those were not valid numbers")
             self.run()
             # re-raising Exception so it can be caught in the tests
             raise ValueError
        except (IndexError):
            print("Oops! Those were not valid numbers, you entered an empty string")
            self.run()
            # re-raising Exception so it can be caught in the tests
            raise IndexError


    def run(self):
        """
        Main part of the program which is called after each successful complete user input and until 0 0 is entered

        """
        self.prompt = raw_input('Enter the number of rows and columns (e.g. 4 4) or to solve and exit the game (e.g. 0 0): \n') # get a string input from the console
        prompt_list = self.prompt.split() # create a list out of user input (e.g. raw string input of '4 4' is converted to a list ['4','4'] )

        self.check_input_rows_columns(prompt_list)

        self.counter += 1 #count how many complete fields user has entered so far
        self.bomb_locations['fields'][self.counter] = [] #create a list under a particular key in dictionary where bomb locations for a particular field are saved
        
        #get self.n input rows from the user 
        for i in range(0,self.n):
            row = raw_input('')
            while not self.is_row_input_valid(row): #ask for the user input until it is inputed correctly 
                row = raw_input('')
            self.bomb_locations['fields'][self.counter].append(list(row)) #creates a 2D matrix of validated user input of bomb locations for a particular field
        
        self.run()
        

                
def main():
    game = Game()
    game.run()

if __name__ == "__main__": 
    main()
