# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: For each unit, we add the constraint that no box can contain a symbol that part of a "naked twin" pair found two other boxes in the same unit. To accomplish this,
we first search inside each unit for pairs of boxes that have identical, two digit possibilities. ( For ex boxes A1 and A2 having both value "34"). Then we delete those possibilities from the rest of the boxes in unit ( in our example, we delete 3 and 4 from all the other boxes exept A1 and A2 in the unit).

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal Sudoku has one extra set of constraints compared to clasical Sudoku:
the two diagonals must each contain each symbol (1-9) exactly once.
So we need to extend our unitlist ( which already contains row_units, column_units and square_untis) by adding diagonal units.
Once we add the new units ( two diagonal units ), the only_choice function will do the work of enforcing the constraint that these untis ( ass well as the classical units) contain each symbol exactly once.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.