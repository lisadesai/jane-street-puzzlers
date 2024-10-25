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
we try every combination of F/B paths, plugging C from range [1,50] until we get one combination of paths that results
in two integer A and B values. Finally, submit successful path and A,B,C value in submission format. :)

Let's see if this works!

'''
#1. Get valid knight moves (valid neighbors). 
#Constraints for validity: not parent node, not a previously "visited" node, and not out of bounds (legal move).

#2. 