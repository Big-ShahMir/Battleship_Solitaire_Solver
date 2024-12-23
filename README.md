# Battleship Solitaire Solver

## Overview  
The **Battleship Solitaire Solver** is a Python program designed to solve Battleship Solitaire puzzles by leveraging techniques from constraint satisfaction problems (CSP). Battleship Solitaire is a single-player puzzle game similar to the Battleship board game but requires logical deduction to place ships on a grid based on row, column, and ship constraints.

This solver automatically computes valid solutions for Battleship Solitaire puzzles by encoding the game rules as constraints and applying advanced search techniques. It ensures solutions adhere to all puzzle rules, including ship placement, grid constraints, and ship isolation.

## How It Works  
1. **Input Parsing**:  
   The solver reads a plain-text input file describing the puzzle:
   - **Row Constraints**: Number of ship parts in each row.
   - **Column Constraints**: Number of ship parts in each column.
   - **Ship Constraints**: Count of each type of ship (submarines, destroyers, cruisers, battleships, carriers).
   - **Initial Grid**: A partially filled NxN grid containing hints for ship placements.

2. **Constraint Satisfaction Problem (CSP)**:  
   The program formulates the puzzle as a CSP with:
   - **Variables**: Grid cells that may contain water or parts of ships.
   - **Constraints**: Logical rules such as row/column constraints, ship type counts, and isolation between ships.

3. **Search Techniques**:  
   The solver applies CSP techniques like:
   - **Backtracking Search**: Efficiently explores potential solutions.
   - **Constraint Propagation**: The **AC-3 GAC (Generalized Arc Consistency) algorithm** is employed to reduce the search space by ensuring all constraints between variables are satisfied. This improves efficiency by pruning invalid states early in the solving process.
   - **Heuristics**: Implements strategies like Minimum Remaining Value and Least Constraining Value to optimize variable and value selection.

4. **Output Generation**:  
   Once a solution is found, the program outputs the solved grid in a plain-text file, adhering to the input format conventions.

## Why It’s Good  
- **Automates Puzzle Solving**: No manual solving required—just input the puzzle, and the solver does the rest.  
- **Robust & Efficient**: Handles puzzles of varying difficulty by combining powerful CSP techniques with heuristic optimization.  
- **Rule Compliance**: Guarantees solutions respect all Battleship Solitaire rules, including row/column constraints and ship isolation.  
- **Extensible**: Can be adapted to solve other grid-based logic puzzles by modifying constraints.  

## How to Use  
1. Prepare an input file in the specified format:
   - First line: Row constraints (space-separated numbers).  
   - Second line: Column constraints (space-separated numbers).  
   - Third line: Number of each ship type (submarines, destroyers, cruisers, battleships, carriers).  
   - Remaining lines: NxN grid representing the puzzle.  

   Example input:  
    211222
    140212
    32100
    000000
    0000S0
    000000
    000000
    00000.
    000000   

2. Run the solver with:  
    python3 battle.py --inputfile <input_file> --outputfile <output_file>

3. The output file will contain the solved grid.

    Example output:
       <>....
       ....S.
       .^....
       .M...S
       .v.^..
       ...v.S

## Key Features  
- **Dynamic CSP Solver**: Integrates backtracking search, forward checking, and AC-3 for constraint satisfaction.  
- **Efficient Heuristics**: Uses MRV, degree heuristics, and LCV to optimize the search process.  
- **Preprocessing**: Automatically handles trivial constraints (e.g., rows/columns with no ship parts).  
- **Scalable**: Can handle puzzles of varying grid sizes within the time limit.  

## Requirements  
- Python 3.9+   
