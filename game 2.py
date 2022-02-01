import random
import copy
import numpy as np

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def position(self,state):
        black = []
        red = []
        for row in range(5):
            for col in range(5):
                if state[row][col] == 'b':
                    black.append((row,col))
                elif state[row][col] == 'r':
                    red.append((row,col))
        return black,red

    def heuristic_game_value(self, state, piece):
        b,r = self.position(state)
        if piece == 'b':
            #my side, opposite side
            m = 'b'
            o = 'r'

        elif piece == 'r':
            m = 'r'
            o = 'b'

        # max myside, opposite 
        max_m = 0
        max_o = 0
        # to count myside, opposite side
        num_m = 0
        num_o = 0

        #horizontal
        for i in range(5):
            for j in range(5):
                if state[i][j] == m:
                    num_m += 1
            if num_m > max_m:
                max_m = num_m
            num_m = 0
        i=0
        j=0
        for i in range(5):
            for j in range(5):
                if state[i][j] == o:
                    num_o += 1
            if num_o > max_o:
                max_o = num_o
            num_o = 0

        # for vertical
        for col in range(5):
            for j in range(5):
                if state[j][col] == m:
                    num_m += 1
            if num_m > max_m:
                max_m = num_m
            num_m = 0
        col=0
        j=0
        for col in range(5):
            for j in range(5):
                if state[j][col] == o:
                    num_o += 1
            if num_o > max_o:
                max_o = num_o
            num_o = 0


        # for / diagonal
        num_m = 0
        num_o = 0

        for row in range(3, 5):
            for col in range(2):
                if state[row][col] == m:
                    num_m += 1
                if state[row - 1][col + 1] == m:
                    num_m += 1
                if state[row - 2][col + 2] == m:
                    num_m += 1
                if state[row - 3][col + 3] == m:
                    num_m += 1

                if num_m > max_m:
                    max_m = num_m
                num_m = 0

        row = 0
        col= 0

        for row in range(3, 5):
            for col in range(2):
                if state[row][col] == o:
                    num_o += 1
                if state[row - 1][col + 1] == o:
                    num_o += 1
                if state[row - 2][col + 2] == o:
                    num_o += 1
                if state[row - 3][col + 3] == o:
                    num_o += 1
                if num_o > max_o:
                    max_o = num_o
                num_o = 0

        # for \ diagonal
        num_m = 0
        num_o = 0
        row = 0
        col = 0
        for row in range(2):
            for col in range(2):
                if state[row][col] == m:
                    num_m += 1
                if state[row + 1][col + 1] == m:
                    num_m += 1
                if state[row + 2][col + 2] == m:
                    num_m += 1
                if state[row + 3][col + 3] == m:
                    num_m += 1
                if num_m > max_m:
                    max_m = num_m
                num_m = 0

        row = 0
        col = 0
        for row in range(2):
            for col in range(2):
                if state[row][col] == o:
                    num_o += 1
                if state[row + 1][col + 1] == o:
                    num_o += 1
                if state[row + 2][col + 2] == o:
                    num_o += 1
                if state[row + 3][col + 3] == o:
                    num_o += 1
                if num_o > max_o:
                    max_o = num_o
                num_o = 0

        # for 3x3 at corner - special teeko2 
        num_m = 0
        num_o = 0
        row = 0
        col = 0
        for row in range(3):
            for col in range(3):
                if state[row][col] == m:
                    num_m += 1
                if state[row][col + 2] == m:
                    num_m += 1
                if state[row + 2][col] == m:
                    num_m += 1
                if state[row + 2][col + 2]== m:
                    num_m += 1
                if num_m > max_m:
                    max_m = num_m
                num_m = 0

        row = 0
        col = 0
        for row in range(3):
            for col in range(3):
                if state[row][col] == o:
                    num_o += 1
                if state[row][col + 2] == o:
                    num_o += 1
                if state[row + 2][col] == o:
                    num_o += 1
                if state[row + 2][col + 2]== o:
                    num_o += 1
                if num_o > max_o:
                    max_o = num_o
                num_o = 0

        #return 0, if equal
        if max_m == max_o:
            return 0, state

        # return pos, my side is larger
        if max_m >= max_o:
            return max_m/6, state 

        #return neg, opp is larger
        return (-1) * max_o/6, state


    #minmax
    def max_value(self, state, depth):
        state_update = state
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            return self.game_value(state),state

        #if it gets bigger then 4, it becomes too slow(more than 5 sec)
        if depth >= 3:
            return self.heuristic_game_value(state,self.my_piece)

        else:
            #to compare,set it with -infinity
            alpha = float('-Inf')
            #compare with successcor
            for succ in self.succ(state, self.my_piece):
                val = self.min_value(succ,depth+1)
                if val[0] > alpha:
                    alpha = val[0]
                    state_update = succ
        return alpha, state_update

    def min_value(self, state,depth):
        state_update = state
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            return self.game_value(state),state
        
        if depth >= 3:
            return self.heuristic_game_value(state, self.opp)

        else:
            beta = float('Inf')
            for succ in self.succ(state, self.opp):
                val = self.max_value(succ,depth+1)
                if val[0] < beta:
                    beta = val[0]
                    state_update = succ
        return beta, state_update

    def succ(self, state, piece):
        ls = []
        num_red = 0
        num_black = 0

        #count red, black 
        for i in range(5):
            for j in range(5):
                if state[i][j] == 'r':
                    num_red += 1
                if state[i][j] == 'b':
                    num_black += 1

        #when drop phase
        if num_black + num_red < 8:  
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        state_cp = copy.deepcopy(state)
                        state_cp[i][j] = piece
                        ls.append(state_cp)
        else: 
            coordinates = []
            for i in range(5):
                for j in range(5):
                    if state[i][j] == piece:
                        coordinates.append([i, j])
            for c in coordinates:
                if c[0] - 1 >= 0 and state[c[0] - 1][c[1]] == ' ':
                    state_cp = copy.deepcopy(state)
                    state_cp[c[0]][c[1]] = ' '
                    state_cp[c[0] - 1][c[1]] = piece
                    ls.append(state_cp)
                if c[0] + 1 <= 4 and state[c[0] + 1][c[1]] == ' ':
                    state_cp = copy.deepcopy(state)
                    state_cp[c[0]][c[1]] = ' '
                    state_cp[c[0] + 1][c[1]] = piece
                    ls.append(state_cp)
                if c[1] - 1 >= 0 and state[c[0]][c[1] - 1] == ' ':
                    state_cp = copy.deepcopy(state)
                    state_cp[c[0]][c[1]] = ' '
                    state_cp[c[0]][c[1] - 1] = piece
                    ls.append(state_cp)
                if c[1] + 1 <= 4 and state[c[0]][c[1] + 1] == ' ':
                    state_cp = copy.deepcopy(state)
                    state_cp[c[0]][c[1]] = ' '
                    state_cp[c[0]][c[1] + 1] = piece
                    ls.append(state_cp)
                if c[0] - 1 >= 0 and c[1] - 1 >= 0 and state[c[0] - 1][c[1] - 1] == ' ':
                    state_cp = copy.deepcopy(state)
                    state_cp[c[0]][c[1]] = ' '
                    state_cp[c[0] - 1][c[1] - 1] = piece
                    ls.append(state_cp)
                if c[0] - 1 >= 0 and c[1] + 1 <= 4 and state[c[0] - 1][c[1] + 1] == ' ':
                    state_cp = copy.deepcopy(state)
                    state_cp[c[0]][c[1]] = ' '
                    state_cp[c[0] - 1][c[1] + 1] = piece
                    ls.append(state_cp)
                if c[0] + 1 <= 4 and c[1] - 1 >= 0 and state[c[0] + 1][c[1] - 1] == ' ':
                    state_cp = copy.deepcopy(state)
                    state_cp[c[0]][c[1]] = ' '
                    state_cp[c[0] + 1][c[1] - 1] = piece
                    ls.append(state_cp)
                if c[0] + 1 <= 4 and c[1] + 1 <= 4 and state[c[0] + 1][c[1] + 1] == ' ':
                    state_cp = copy.deepcopy(state)
                    state_cp[c[0]][c[1]] = ' '
                    state_cp[c[0] + 1][c[1] + 1] = piece
                    ls.append(state_cp)
        return ls

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True   # TODO: detect drop phase

        #check if drop phase
        numB = sum((i.count('b') for i in state))
        numR = sum((i.count('r') for i in state))
        if numB >= 4 and numR >= 4:
            drop_phase = False

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move = []
            a, state_update = self.max_value(state, 0)
            # compare current with succ
            arr1 = np.array(state) == np.array(state_update)
            arr2 = np.where(arr1 == False) 
            
            if state[arr2[0][0]][arr2[1][0]] == ' ':
                (origrow, origcol) = (arr2[0][1],arr2[1][1])
                (row,col) = (arr2[0][0], arr2[1][0])
            else:
                (origrow, origcol) = (arr2[0][0], arr2[1][0])
                (row, col) = (arr2[0][1], arr2[1][1])
            move.insert(0, (row, col))
            #should move drop phase end
            move.insert(1, (origrow, origcol)) 
            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move2 = []
        a, state_update = self.max_value(state,0)
        #compare current and succ
        arr1 = np.array(state) == np.array(state_update)
        arr2 = np.where(arr1 == False)
        (row, col) = (arr2[0][0], arr2[1][0])
        while not state[row][col] == ' ':
            (row, col) = (arr2[0][0], arr2[1][0])

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move2.insert(0, (row, col))
        return move2

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == state[row + 3][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1

        # TODO: check / diagonal wins
        for row in range(3, 5):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row - 1][col + 1] == state[row - 2][col + 2] == state[row - 3][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1

        # TODO: check 3x3 square corners wins
        for row in range(3):
            for col in range(3):
                if state[row][col] != ' ' and state[row][col] == state[row][col + 2] == state[row + 2][col] == state[row + 2][col + 2]:
                    return 1 if state[row][col] == self.my_piece else -1
        
        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
