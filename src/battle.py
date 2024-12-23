from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search
import sys
import argparse


# def print_solution(s, size):
#     s_ = {}
#
#     for (var, val) in s:
#         print(var.name, val)
#         s_[int(var.name())] = val
#         # print((var.name()))
#     for i in range(1, size - 1):
#         for j in range(1, size - 1):
#             print(s_[-1 - (i * size + j)], end="")
#         print('')

def print_solution(s, size):
    # print(s)
    sol_dict = {}
    for (var, val) in s:
        sol_dict[int(var.name())] = val
        # print(var.name())

    for i in range(0, size):
        for j in range(0, size):
            # print(i, j)
            if (i < (size - 5) and sol_dict[(-1 - (i * size + j))] == "|" and sol_dict[(-1 - ((i+1) * size + j))] == "|" and sol_dict[(-1 - ((i+2) * size + j))] == "|" and sol_dict[(-1 - ((i+3) * size + j))] == "|"  and sol_dict[(-1 - ((i+4) * size + j))] == "|"):
                sol_dict[(-1 - (i * size + j))] = "^"
                sol_dict[(-1 - ((i+1) * size + j))] = "M"
                sol_dict[(-1 - ((i+2) * size + j))] = "M"
                sol_dict[(-1 - ((i+3) * size + j))] = "M"
                sol_dict[(-1 - ((i+4) * size + j))] = "v"
            elif (i < (size - 4) and sol_dict[(-1 - (i * size + j))] == "|" and sol_dict[(-1 - ((i+1) * size + j))] == "|" and sol_dict[(-1 - ((i+2) * size + j))] == "|" and sol_dict[(-1 - ((i+3) * size + j))] == "|"):
                sol_dict[(-1 - (i * size + j))] = "^"
                sol_dict[(-1 - ((i+1) * size + j))] = "M"
                sol_dict[(-1 - ((i+2) * size + j))] = "M"
                sol_dict[(-1 - ((i+3) * size + j))] = "v"
            elif (i < (size - 3) and sol_dict[(-1 - (i * size + j))] == "|" and sol_dict[(-1 - ((i+1) * size + j))] == "|" and sol_dict[(-1 - ((i+2) * size + j))] == "|"):
                sol_dict[(-1 - (i * size + j))] = "^"
                sol_dict[(-1 - ((i+1) * size + j))] = "M"
                sol_dict[(-1 - ((i+2) * size + j))] = "v"
            elif  (i < (size - 2) and sol_dict[(-1 - (i * size + j))] == "|" and sol_dict[(-1 - ((i+1) * size + j))] == "|"):
                sol_dict[(-1 - (i * size + j))] = "^"
                sol_dict[(-1 - ((i+1) * size + j))] = "v"
            if (j < (size - 4) and sol_dict[(-1 - (i * size + j))] == "-" and sol_dict[(-1 - (i * size + j+1))] == "-" and sol_dict[(-1 - (i * size + j+2))] == "-" and sol_dict[(-1 - (i * size + j+3))] == "-" and sol_dict[(-1 - (i * size + j+4))] == "-"):
                sol_dict[(-1 - (i * size + j))]  = "<"
                sol_dict[(-1 - (i * size + j+1))] = "M"
                sol_dict[(-1 - (i * size + j+2))] = "M"
                sol_dict[(-1 - (i * size + j+3))] = "M"
                sol_dict[(-1 - (i * size + j+4))] = ">"
            elif (j < (size - 4) and sol_dict[(-1 - (i * size + j))] == "-" and sol_dict[(-1 - (i * size + j+1))] == "-" and sol_dict[(-1 - (i * size + j+2))] == "-" and sol_dict[(-1 - (i * size + j+3))] == "-"):
                sol_dict[(-1 - (i * size + j))]  = "<"
                sol_dict[(-1 - (i * size + j+1))] = "M"
                sol_dict[(-1 - (i * size + j+2))] = "M"
                sol_dict[(-1 - (i * size + j+3))] = ">"
            elif (j < (size - 3) and sol_dict[(-1 - (i * size + j))] == "-" and sol_dict[(-1 - (i * size + j+1))] == "-" and sol_dict[(-1 - (i * size + j+2))] == "-"):
                sol_dict[(-1 - (i * size + j))]  = "<"
                sol_dict[(-1 - (i * size + j+1))] = "M"
                sol_dict[(-1 - (i * size + j+2))] = ">"
            elif (j < (size - 2) and sol_dict[(-1 - (i * size + j))] == "-" and sol_dict[(-1 - (i * size + j+1))] == "-"):
                sol_dict[(-1 - (i * size + j))]  = "<"
                sol_dict[(-1 - (i * size + j+1))] = ">"

    for i in range(1, size-1):
        for j in range(1, size-1):
            if sol_dict[(-1 - (i * size + j))] == "-" or sol_dict[(-1 - (i * size + j))] == "|":
                sol_dict[(-1 - (i * size + j))] = "S"

    for i in range(1, size - 1):
        for j in range(1, size - 1):
            print(sol_dict[-1 - (i * size + j)], end="")
        print('')


#parse board and ships info
#file = open(sys.argv[1], 'r')
#b = file.read()
parser = argparse.ArgumentParser()
parser.add_argument(
    "--inputfile",
    type=str,
    required=True,
    help="The input file that contains the puzzles."
)
parser.add_argument(
    "--outputfile",
    type=str,
    required=True,
    help="The output file that contains the solution."
)
args = parser.parse_args()
file = open(args.inputfile, 'r')
b = file.read()
b2 = b.split()
size = len(b2[0])
size = size + 2
b3 = []
b3 += ['0' + b2[0] + '0']
b3 += ['0' + b2[1] + '0']
b3 += [b2[2] + ('0' if len(b2[2]) == 3 else '')]
b3 += ['0' * size]
for i in range(3, len(b2)):
    b3 += ['0' + b2[i] + '0']
b3 += ['0' * size]
board = "\n".join(b3)
b4 = b3[3:]

varlist = []
varn = {}
conslist = []

check_vars = []
row_cons = []
col_cons = []
ship_cons = [0,0,0,0,0]
#ADD CODE HERE TO CHECK GIVEN 0 CONSTRAINTS IN ROW AND COLUMN AND IF VALUES GIVEN THEN MAKE THE REST WATER.

# print(board)
# print(size)
# print(b3)

for i in range(0, size):
    # print(type(b3[0][i]))
    row_cons.append(b3[0][i])

for i in range(0, size):
    col_cons.append(b3[1][i])


for i in range(5):
    if i < len(b3[2]):
        ship_cons[i] = (b3[2][i])


# Subtract and Match
row_count = {}
col_count = {}
for i in range(0, size):
    if i not in row_count:
        row_count[i] = 0
    for j in range(0, size):
        if j not in col_count:
            col_count[j] = 0
        v = None
        if b4[i][j] != '0' and b4[i][j] != '.':
            row_count[i] += 1
            col_count[j] += 1

#1/0 variables
for i in range(0, size):
    for j in range(0, size):
        v = None
        # if -1 - (i * size + j) == -22:
        #     print( b4[i][j])
        if i == 0 or i == size - 1 or j == 0 or j == size - 1:
            v = Variable(str(-1 - (i * size + j)), ["."])  # Edges cant be ships
        elif b4[i][j] == 'M' or b4[i][j] == 'S':
            v = Variable(str(-1 - (i * size + j)), ["|", "-"])
            # v.setValue(b4[i][j])
        elif b4[i][j] == '^' or b4[i][j] == 'v':
            v = Variable(str(-1 - (i * size + j)), ["|"])
            # v.setValue("|")
        elif b4[i][j] == '<' or b4[i][j] == '>':
            v = Variable(str(-1 - (i * size + j)), ["-"])
            # v.setValue("-")
        elif b4[i][j] == '.':
            v = Variable(str(-1 - (i * size + j)), ['.'])  # Given
            # v.setValue(".")
        elif (row_cons[i] == "0" and i != 0 and i != size) or (
                int(row_cons[i]) - row_count[i] == 0):
            v = Variable(str(-1 - (i * size + j)),["."])  # Not Edges = can be ships
        elif (col_cons[j] == "0" and j != 0 and j != size) or (
                int(col_cons[j]) - col_count[j] == 0):
            v = Variable(str(-1 - (i * size + j)), ["."])  # Not Edges = can be ships
        else:
            v = Variable(str(-1 - (i * size + j)), [".", "-", "|"])  # Not Corners = can be ships
        # varlist.append(v)
        varn[str(-1 - (i * size + j))] = v

# redo = []
#Further restrict domain
for i in range(0, size):
    for j in range(0, size):
        if i >= 1 or i <= size - 2 or j >= 1 or j <= size - 2:
            if b4[i][j] == "<":
                if str(-1 - ((i) * size + j+1)) in varn:
                    varn[str(-1 - ((i) * size + j+1))] = Variable(str(-1 - (i * size + j+1)), ["-"])
                    # redo.append(Variable(str(-1 - (i * size + j+1)), ["-"]))
                if str(-1 - ((i) * size + j-1)) in varn:
                    varn[str(-1 - ((i) * size + j-1))] = Variable(str(-1 - (i * size + j-1)), ["."])
                    # redo.append(Variable(str(-1 - (i * size + j-1)), ["."]))
            elif b4[i][j] == ">":
                if str(-1 - ((i) * size + j+1)) in varn:
                    varn[str(-1 - ((i) * size + j+1))] = Variable(str(-1 - (i * size + j+1)), ["."])
                    # redo.append( Variable(str(-1 - (i * size + j+1)), ["."]))
                if str(-1 - ((i) * size + j-1)) in varn:
                    varn[str(-1 - ((i) * size + j-1))] = Variable(str(-1 - (i * size + j-1)), ["-"])
                    # redo.append(Variable(str(-1 - (i * size + j-1)), ["-"]))
            elif b4[i][j] == "^":
                if str(-1 - ((i-1) * size + j)) in varn:
                    varn[str(-1 - ((i-1) * size + j))] = Variable(str(-1 - ((i-1) * size + j)), ["."])
                    # redo.append(Variable(str(-1 - ((i-1) * size + j)), ["."]))
                if str(-1 - ((i+1) * size + j)) in varn:
                    varn[str(-1 - ((i+1) * size + j))] = Variable(str(-1 - ((i+1) * size + j)), ["|"])
                    # redo.append(Variable(str(-1 - ((i+1) * size + j)), ["|"]))
            elif b4[i][j] == "v":
                if str(-1 - ((i-1) * size + j)) in varn:
                    varn[str(-1 - ((i-1) * size + j))] = Variable(str(-1 - ((i-1) * size + j)), ["|"])
                    # redo.append(Variable(str(-1 - ((i-1) * size + j)), ["|"]))
                if str(-1 - ((i+1) * size + j)) in varn:
                    varn[str(-1 - ((i+1) * size + j))] = Variable(str(-1 - ((i+1) * size + j)), ["."])
                    # redo.append(Variable(str(-1 - ((i+1) * size + j)), ["."]))
            elif b4[i][j] == "M":
                if j == 1 or j == size - 1:
                    if str(-1 - ((i-1) * size + j)) in varn:
                        varn[str(-1 - ((i-1) * size + j))] = Variable(str(-1 - ((i-1) * size + j)), ["|"])
                    if str(-1 - ((i+1) * size + j)) in varn:
                        varn[str(-1 - ((i+1) * size + j))] = Variable(str(-1 - ((i+1) * size + j)), ["|"])
                if i == 1 or 1 == size - 1:
                    if str(-1 - ((i) * size + j+1)) in varn:
                        varn[str(-1 - ((i) * size + j+1))] = Variable(str(-1 - ((i) * size + j+1)), ["-"])
                    if str(-1 - ((i) * size + j-1)) in varn:
                        varn[str(-1 - ((i) * size + j-1))] = Variable(str(-1 - ((i) * size + j-1)), ["-"])
            elif b4[i][j] == "S":
                if str(-1 - ((i-1) * size + j)) in varn:
                    varn[str(-1 - ((i-1) * size + j))] = Variable(str(-1 - ((i-1) * size + j)), ["."])
                if str(-1 - ((i+1) * size + j)) in varn:
                    varn[str(-1 - ((i+1) * size + j))] = Variable(str(-1 - ((i+1) * size + j)), ["."])
                if str(-1 - ((i) * size + j+1)) in varn:
                    varn[str(-1 - ((i) * size + j+1))] = Variable(str(-1 - ((i) * size + j+1)), ["."])
                if str(-1 - ((i) * size + j-1)) in varn:
                    varn[str(-1 - ((i) * size + j-1))] = Variable(str(-1 - ((i) * size + j-1)), ["."])


varlist = list(varn.values())

# for i in range(len(redo)):
#     for j in range(len(varlist)):
#         if redo[i].name() == varlist[j].name():
#             varlist[j] = redo[i]

# for var in varlist:
#     print(var)


#make 1/0 variables match board info
ii = 0
for i in board.split()[3:]:
    jj = 0
    for j in i:
        # print(j)
        if j == ".":
            conslist.append(TableConstraint('bool_match1',
                                            [varn[str(-1 - (ii * size + jj))]],
                                            [["."]]))
        elif j == '<' or j == '>':
            conslist.append(TableConstraint('bool_match2',
                                            [varn[str(-1 - (ii * size + jj))]],
                                            [['-']]))
        elif j == '^' or j == 'v':
            conslist.append(TableConstraint('bool_match3',
                                            [varn[str(-1 - (ii * size + jj))]],
                                            [['|']]))
        elif j == 'M' or j == 'S':
        # else:
            conslist.append(TableConstraint('bool_match4',
                                            [varn[str(-1 - (ii * size + jj))]],
                                            [['|'], ['-']]))
        jj += 1
    ii += 1


row_constraint = []
for i in board.split()[0]:
    row_constraint += [int(i)]

for row in range(0, size):
    conslist.append(NValuesConstraint('row',
                                      [varn[str(-1 - (row * size + col))] for
                                       col in range(0, size)],
                                      ['-', '|'],
                                      row_constraint[row], row_constraint[row]))

col_constraint = []
for i in board.split()[1]:
    col_constraint += [int(i)]

for col in range(0, size):
    conslist.append(NValuesConstraint('col',
                                      [varn[str(-1 - (col + row * size))] for
                                       row in range(0, size)],
                                      ['-', '|'],
                                      col_constraint[col], col_constraint[col]))


for i in range(0, size):
    for j in range(0, size):
        if i != 0 and i != size - 1 and j != 0 and j != size - 1:
            conslist.append(TableConstraint(
                'right_side' + str(i) + str(j) + '_to_' + str(i) + str(j + 1),
                [varn[str(-1 - (i * size + j))],
                 varn[str(-1 - (i * size + j + 1))]],
                [['|', '.'], ['.', '|'], ['.', '-'], ['.', '.'],
                 ['-', '-'], ['-', '.']]))
            conslist.append(TableConstraint(
                'left_side' + str(i) + str(j) + '_to_' + str(i) + str(j - 1),
                [varn[str(-1 - (i * size + j))],
                 varn[str(-1 - (i * size + j - 1))]],
                [['|', '.'], ['.', '|'], ['.', '-'], ['.', '.'],
                 ['-', '-'], ['-', '.']]))
            conslist.append(TableConstraint(
                'up_side' + str(i) + str(j) + '_to_' + str(i - 1) + str(j),
                [varn[str(-1 - (i * size + j))],
                 varn[str(-1 - ((i - 1) * size + j))]],
                [['|', '.'], ['.', '|'], ['.', '-'],
                 ['.', '.'], ['|', '|'], ['-', '.']]))
            conslist.append(TableConstraint(
                'down_side' + str(i) + str(j) + '_to_' + str(i + 1) + str(j),
                [varn[str(-1 - (i * size + j))],
                 varn[str(-1 - ((i + 1) * size + j))]],
                [['.', '|'], ['.', '-'],
                 ['.', '.'], ['|', '|'], ['-', '.'], ['|', '.']]))
            conslist.append(TableConstraint(
                'diag_up_r' + str(i) + str(j) + '_to_' + str(i - 1) + str(
                    j + 1), [varn[str(-1 - (i * size + j))],
                             varn[str(-1 - ((i - 1) * size + (j + 1)))]],
                [['.', '|'], ['.', '.'], ['.', '-'],
                 ['|', '.'], ['-', '.']]))
            conslist.append(TableConstraint(
                'diag_up_l' + str(i) + str(j) + '_to_' + str(i - 1) + str(
                    j - 1), [varn[str(-1 - (i * size + j))],
                             varn[str(-1 - ((i - 1) * size + (j - 1)))]],
                [['.', '|'], ['.', '.'], ['.', '-'],
                 ['|', '.'], ['-', '.']]))
            conslist.append(TableConstraint(
                'diag_down_l' + str(i) + str(j) + '_to_' + str(i + 1) + str(
                    j - 1), [varn[str(-1 - (i * size + j))],
                             varn[str(-1 - ((i + 1) * size + (j - 1)))]],
                [['.', '|'], ['.', '-'], ['.', '.'],
                 ['|', '.'], ['-', '.']]))
            conslist.append(TableConstraint(
                'diag_down_r' + str(i) + str(j) + '_to_' + str(i + 1) + str(
                    j + 1), [varn[str(-1 - (i * size + j))],
                             varn[str(-1 - ((i + 1) * size + (j + 1)))]],
                [['.', '|'], ['.', '-'],
                 ['.', '.'], ['|', '.'], ['-', '.']]))



#./S/</>/v/^/M variables
#these would be added to the csp as well, before searching,
#along with other constraints
#for i in range(0, size):
#  for j in range(0, size):
#    v = Variable(str(i*size+j), ['.', 'S', '<', '^', 'v', 'M', '>'])
#    varlist.append(v)
#    varn[str(str(i*size+j))] = v
#connect 1/0 variables to W/S/L/R/B/T/M variables
#    conslist.append(TableConstraint('connect', [varn[str(-1-(i*size+j))], varn[str(i*size+j)]], [[0,'.'],[1,'S'],[1,'<'],[1,'^'],[1,'v'],[1,'M'],[1,'>']]))

#find all solutions and check which one has right ship #'s
csp = CSP('battleship', varlist, conslist)
# for var in csp.variables():
#     if var._name == "-22":
#         print(var._name, var.curDomain())
# for cs in csp.constraints():
#     print(cs._name)

solutions, num_nodes = bt_search('GAC', csp, 'mrv', True, False, size, ship_cons)
sys.stdout = open(args.outputfile, 'w')
for i in range(len(solutions)):
    # print("hi")
    print_solution(solutions[i], size)
    # print("--------------")
