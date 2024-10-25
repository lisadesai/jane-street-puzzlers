#Knight Moves #6

#Link to puzzle: https://www.janestreet.com/puzzles/current-puzzle/

'''Intuition: Brute Force to Exhaustive Search. 

I thought the easiest way to approach this is using a brute force exhaustive search. 

This is my first time solving a JS Puzzle, so I'm not really considering optimization or anything, I just want an answer! :)

Method: find all knight paths from Start to End (both A1-C5 (Forward) and A5-C1 (Backward) cases) while keeping track of the letter of the square,
create equations out of each knight path, then plug a C value to get all corresponding A and B values until an integer pair of A and B is found.

The board looks like a graph, so recursively backtracking seems like a good method to find
all the possible knight paths. This is for the FORWARD (F) knight traversal paths. Then, we repeat for the BACKWARD (B) paths.

Then, since we have an optimization math problem here given 3 variables but only 2 equations, 
we try every combination of F/B paths, plugging C from range [1,49] until we get one combination of paths that results
in two integer A and B values, where A+B+C < 50. Finally, submit successful path and A,B,C value in submission format. :)

Let's see if this works!

'''
#imports

import numpy as np
from scipy.optimize import fsolve


#1. Get valid knight moves (valid neighbors). 
#Constraints for validity: not parent node, not a previously "visited" node, and not out of bounds (legal move).

# def knight_moves(board_size, start):
#     # Knight's possible moves
#     moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    
#     def is_valid(x, y):
#         return 0 <= x < board_size and 0 <= y < board_size
    
#     def backtrack(x, y, path):
#         # Append the current position to the path
#         path.append((x, y))
        
#         # Check all possible knight moves
#         for dx, dy in moves:
#             new_x, new_y = x + dx, y + dy
            
#             if is_valid(new_x, new_y) and (new_x, new_y) not in path:
#                 backtrack(new_x, new_y, path)
        
#         # Remove the position after exploring all moves (backtrack)
#         path.pop()
    
#     # Start the backtracking from the initial position
#     paths = []
#     backtrack(start[0], start[1], [])
#     return paths

# def create_weighted_grid():
    # dt = {}

    # for x in range(3):
    #     dt[(i,0)] = 'A'
    #     dt[(i,1)] = 'A'
    # for x in range(2):
    #     dt[(i,2)] = 'A'
    #     dt[(i,3)] = 'A'
    # for x in 

    # return dt


letter_book = {'A': [(0,0), (1,0),(2,0), (0,1), (1,1),(2,1), (0,2), (1,2), (0,3 ), (1,3 ), (0,4 ), (0,5 )],
               'B':  [(3,0 ), (4,0 ), (3,1 ), (4,1 ),(2,2), (3,2),(2,3),(3,3), (1,4),(2,4), (1,5),(2,5) ] ,
              'C': [(5,0 ),(5,1), (4,2), (5,2),(4,3), (5,3) , (3,4), (4,4), (5,4),(3,5), (4,5), (5,5)  ]}

 


# #2. Delete paths that use visited squares!
def create_equation(path):
    eq = ''
    for i in path:    
        if tuple(i) in letter_book['A']:
            eq+=('A')
        elif tuple(i) in letter_book['B']:
            eq+=('B')
        else:
            eq+=('C')
    
    return eq
# #3. Map each node in path to a letter, then string together an equation

# board_size = 6
# start_position = (0, 0)
# forward_paths = knight_moves(board_size, start_position)

# # Printing the results
# for path in forward_paths:
#     print(path)

def get_blackout_squares_x_then_y(curr, prev):
    if curr and prev:
        curr_x, curr_y = curr[0], curr[1]
        prev_x, prev_y = prev[0], prev[1]
    
    curr_x

def is_valid(x, y, board_size):
        return 0 <= x < board_size and 0 <= y < board_size

def knight_moves(board_size, start, end, depth):
    # Knight's possible moves
    moves = [ (2, 1), (1, 2), (-1, 2), (-2, 1),(-2, -1), (-1, -2), (1, -2), (2, -1) ]
    
    def backtrack(x, y, visited, path):
        # Append the current position to the path
        path.append((x, y))
        visited.add((x, y))
        #add blackout squares to visited
        

        # if depth_limit == len(path):

        #IF you hit the end square: add that path!
        if (x,y) == end:
            all_paths.append(path.copy())
            print(path)
        else:
        # Check all possible knight moves
            for dx, dy in moves:
                new_x, new_y = x + dx, y + dy

                #check if each move is a legal step (not off the board), not previously visited
                if is_valid(new_x, new_y, board_size) and (new_x, new_y) not in visited:
                    backtrack(new_x, new_y, visited, path)
            
        # Remove the position after exploring all moves (backtrack)
        visited.remove((x, y))
        path.pop()
    
    all_paths = []
    backtrack(start[0], start[1], set(), [])
    return all_paths

# Example usage
board_size = 6
start = (0, 0)
end = (5,5)
depth_limit = 7  # Set depth limit as needed
forwards_paths = knight_moves(board_size, start, end, depth_limit)

# Printing the results
# for path in forward_paths:
#     print(path)




# # Equation Solver
# def equations(vars, C):
#     a, b = vars
#     x = (2024 - 3*C)/C #todo: fix this to change according to eq passed in
#     y = x+1            #same here
#     forward = ((3*a*b) + (2*b)) - y
#     backward = (((a**2)*b + a) *b) - x
#     return [backward, forward]


# def solver():
#     # Initial guesses for x and y
#     initial_guesses = [1, 1]

#     # Solve the system of equations, where C can be a value from 1-50 to find A and B values.
#     res=[]
#     for C in range(1,51):
#         solution = fsolve(equations, initial_guesses, C)
#         if solution[0].is_integer() or solution[1].is_integer():
#             res.append(solution)
#         if solution[0] + solution[1] + C < 50: #A+B+C < 50
#             print("A+B+C < 50: ", solution, "C: ", C)
#             if solution[0].is_integer() or solution[1].is_integer():
#                 res.append(solution)
#     return res
     
# print("Res List: " , solver())

