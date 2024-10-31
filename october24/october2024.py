#Knight Moves #6

#Link to puzzle: https://www.janestreet.com/puzzles/current-puzzle/

'''Intuition: Brute Force to Exhaustive Search. 

I thought the easiest way to approach this is using a brute force exhaustive search. 

This is my first time solving a JS Puzzle, so I'm not really considering optimization or anything, I just want an answer! :)

Method: find all knight paths from Start to End (both A1-F6 (Forward) and A6-F1 (Backward) cases) while keeping track of the letter of the square,
create equations out of each knight path, then plug a C value to get all corresponding A and B values until an integer pair of A and B is found.

The board looks like a graph, so recursively backtracking seems like a good method to find
all the possible knight permutations. This is for the FORWARD (F) knight traversal paths. Then, we repeat for the BACKWARD (B) paths.

Then, since we have an optimization math problem here given 3 variables but only 2 equations, 
we try every combination of F/B paths, plugging C from range [1,49] until we get one combination of paths that results
in two integer A and B values, where A+B+C < 50. Finally, submit successful path and A,B,C value in submission format. :)

Let's see if this works!

'''
import numpy as np
from scipy.optimize import fsolve
from collections import deque

print("----------------Begin program----------------")
print("---------------------------------------------")

# 0. Create dictionary of A, B and C values. Refer to image to see assignations.
letter_book = {'A': [(0,0), (1,0),(2,0), (0,1), (1,1),(2,1), (0,2), (1,2), (0,3 ), (1,3 ), (0,4 ), (0,5 )],
               'B':  [(3,0 ), (4,0 ), (3,1 ), (4,1 ),(2,2), (3,2),(2,3),(3,3), (1,4),(2,4), (1,5),(2,5) ] ,
              'C': [(5,0 ),(5,1), (4,2), (5,2),(4,3), (5,3) , (3,4), (4,4), (5,4),(3,5), (4,5), (5,5)  ]}

 

#1. Get valid knight moves based on puzzle constraints. 
def is_valid(x, y, board_size):
    return 0 <= x < board_size and 0 <= y < board_size

def get_paths(board_size, start, end, depth_limit):
    # Knight's possible moves
    moves = [ (2, 1), (1, 2), (-1, 2), (-2, 1),(-2, -1), (-1, -2), (1, -2), (2, -1) ]

    def backtrack(x, y, visited, path, depth):
        if depth > depth_limit:
            return  #exit early if already exceeding depth

        # Append the current position to the path
        path.append((x, y))
        visited.add((x, y))
            

        #If you hit the end square: add that path!
        if (x,y) == end: # len(path) == depth_limit: 
            all_paths.append(path.copy())
            # print(path)
        else:
        # Check all possible knight moves
            for dx, dy in moves:
                new_x, new_y = x + dx, y + dy

                #check if each move is a legal step (not off the board), not previously visited
                if is_valid(new_x, new_y, board_size) and (new_x, new_y) not in visited:
                    if len(path) < depth_limit:  #check if we exceeded depth limit before recurse again
                        backtrack(new_x, new_y, visited, path, depth+1)
            
        # Remove the position after exploring all moves (backtrack)
        visited.remove((x, y))
        path.pop()
    
    all_paths = []
    backtrack(start[0], start[1], set(), [], 0)
    return all_paths

board_size = 6
back_start = (0, 5)
back_end = (5,0)
for_start = (0,0)
for_end = (5,5)
depth_limit_f = 7  #Prevents long run time due to deep recursion. 
depth_limit_b = 7 
backward_paths = get_paths(board_size, back_start, back_end, depth_limit_b)
forward_paths = get_paths(board_size, for_start, for_end, depth_limit_f)

#NOTE: I haven't accounted for blackout squares yet, so some of these paths may be invalid due to re-traversing "used" squares




#2. Generate equation from path of moves
backward_path_equations = {}
forward_path_equations = {}

def create_equation(path):
    eq = ''
    for i in path:    
        if tuple(i) in letter_book['A']:
            eq+=('A')
        elif tuple(i) in letter_book['B']:
            eq+=('B')
        else:
            eq+=('C')
    l= 0
    r=0
    q= deque()
    q.append("(")
    while r < len(eq):
        q.append(eq[r])
        r+=1
        if r< len(eq):
            if eq[l]== eq[r]:
                q.append("+")
            else:
                q.append(")")
                q.appendleft("(")
                q.append("*")
        else:
            q.append(")")
        l+=1
    letter_equation = eq
    equation_math_string = ''.join(q)

    return [letter_equation, equation_math_string]


print(f"Number of valid Forward paths at depth_limit {depth_limit_f}: ", len(forward_paths)) 
print(f"Number of valid Backward paths at depth_limit {depth_limit_b}: ", len(backward_paths)) 

def create_feq_beq():
    feqs= []
    beqs = []

    for path in forward_paths:
        lst = create_equation(path)
        feqs.append(lst[1])
        forward_path_equations[str(path)] = lst

    for path in backward_paths:
        lst = create_equation(path)
        beqs.append(lst[1])
        backward_path_equations[str(path)] = lst #KEY is path of moves as string, VAL is lst above [letter eq, num eq]

    return feqs, beqs

feqs, beqs = create_feq_beq()

# 3. Equation Solver
def equations(vars, constant, f,b):
    A, B = vars
    C = constant
    feq = eval(f.replace('A', str(A)).replace('B', str(B)).replace('C', str(C))+ '- 2024')
    beq = eval(b.replace('A', str(A)).replace('B', str(B)).replace('C', str(C))+ '- 2024')
    return [beq, feq]

def is_clean_decimal(value):
    return abs(value- round(value)) < 1e-10
     
def solver(feq, beq):
    initial_guesses = [4, 8] #Test values, randomly picked from factors of 24
    res=[]
     
    for constant in [1,2,4,8,11,22,23,44,46]: #Test: use factors of 2024 < 50 to ensure even divisibility first
        def wrapper(vars):
            return equations(vars, constant, feq, beq)
        solution = fsolve(wrapper, initial_guesses)

        #check if these are valid solution guesses
        what_beq_eval, what_feq_eval =equations(solution, constant, feq, beq)

        #Check against non-negative and A+B+C<50 constraints
        if np.isclose(what_beq_eval, 0, atol=1e-10) and np.isclose(what_feq_eval, 0, atol=1e-10):
            if solution[0] + solution[1] + constant < 50:  
                if solution[0] >0 and solution[1] > 0:  
                    a = solution[0]
                    b = solution[1] 
                    if is_clean_decimal(a) and  is_clean_decimal(b):
                        res.append((a,b,constant, feq, beq))
    return res
     
 
def print_final_list(feqs, beqs):
    final = []
    for f in feqs:
        for b in beqs:
            results = solver(f,b)
            if results:
                final.append(results)
            print("Valid Results for Forward: ", f,  " and Backward: ", b, " : ", results)
            print("\n")
    print("----------------------------------FINAL:----------------------------------: ")
    print("\n")
    print(final)
    print("\n")
    return final

final = print_final_list(feqs, beqs)

 
 #4. Get moves from final equations  
def print_moves():
    f_nodes = set()
    b_nodes = set()
    for lst in final:
        sol = lst[0]
        a ,b,c = sol[0], sol[1], sol[2]
        forward, backward = sol[3], sol[4]

        for key, val in forward_path_equations.items():
            if val[1] == forward:
                f_nodes.add((round(a), round(b) , round(c), key))
        for key, val in backward_path_equations.items():
            if val[1] == backward:
                b_nodes.add((round(a), round(b) , round(c), key))    
             
    print("F Path Moves: ", f_nodes)
    print("\n")
    print("B Path Moves: ", b_nodes)
    print("\n")

print_moves()


#5. Check if moves use unused squares (manually for now, I didn't create a blackout move check)

#6. Possible Final Answer
print("Possible Final Answer", "\n", "A= 4  B=7 C=22",  "\n", "Moves:  [(0, 0), (2, 1), (0, 2), (2, 3), (1, 5), (3, 4), (5, 5)] for F Equation:  (((A+A+A)*B+B)*C+C)", "\n", "Moves:  [(0, 5), (1, 3), (0, 1), (2, 2), (3, 0), (4, 2), (5, 0)] for B Equation:  (((A+A+A)*B+B)*C+C)")
# A= 4  B=7 C=22
# Moves:  [(0, 0), (2, 1), (0, 2), (2, 3), (1, 5), (3, 4), (5, 5)] F Equation:  (((A+A+A)*B+B)*C+C)
# Moves:  [(0, 5), (1, 3), (0, 1), (2, 2), (3, 0), (4, 2), (5, 0)] B Equation:  (((A+A+A)*B+B)*C+C)
