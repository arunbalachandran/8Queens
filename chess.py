import json

class move:
    def __init__(self, queen, row, column):
        self.queen = queen
        self.row = row
        self.column = column

# initialization
display_ongoing = int(raw_input("Do you want to display the output? : 1 or 0 "))
with open("positions.json") as data_file:
    data = json.load(data_file)
current_queen, row, column = 0, int(data['positions']['row']), int(data['positions']['column'])
stack = []    # empty stack of "moves" (each consisting of a queen and a board position)
temp_mv = move(current_queen, row, column) # (queen 0, position = (user defined))
num_queen = 7 # considering 0 as the first queen, 7 is the highest queen index
stack_popped = False                    # initially as no moves recorded
first_time, move_cnt = 1, 0

while (True):                           # iterates through queens 0 - 7
    temp_mv.queen = current_queen
    # backtracking
    if (stack_popped):                  # if previous position failed, move prev. queen one column to the right
        stack_popped = False
        temp_mv.column += 1
    elif first_time:                    # so as to not override user defined queen-column (first queen)
        first_time = 0
    else:                               # place the new queens at column 0
        move_cnt += 1
        temp_mv.row = (temp_mv.row + 1)%8
        temp_mv.column = 0
    # while ((there is a conflict between position and previous moves recorded in s) and (position.column <= n)):
    while (temp_mv.column <= num_queen):
        if (any(temp_mv.column == i1.column for i1 in stack)):
            temp_mv.column += 1         # seek the first non-conflicting position
        elif (any(abs(temp_mv.row - i2.row) == abs(temp_mv.column - i2.column) for i2 in stack)):
            temp_mv.column += 1         # seek the first non-conflicting position
        else:
            break

    if (temp_mv.column > num_queen):    # no admissible position found
        current_queen -= 1              # backtrack to previous queen
        if (stack):                     # if stack is not empty
            temp_mv = stack[-1]         # pop previous queen's tentative move
            stack.pop()
            stack_popped = True
        else: # if stack is empty here, we're out of luck - there's no solution
            print("No solutions exist")
            break                       # report that no solutions exist
    else:                               # no conflict, so record move
        final_mv = move(temp_mv.queen, temp_mv.row, temp_mv.column)
        stack.append(final_mv)
        current_queen += 1              # on to next queen
        # display the ongoing moves
        if (display_ongoing == 1):
            display_matrix = [[0]*8 for i in range(8)]  # 8*8 chessboard for output
            for moves in stack:
                display_matrix[moves.row][moves.column] = moves.queen + 1
            for rows in range(8):
                print display_matrix[rows]
            print "\n"
    if (current_queen > num_queen):
        print "The total number of moves taken is : " + str(move_cnt)
        break
