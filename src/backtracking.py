from csp import Constraint, Variable, CSP
from constraints import *
import random


class UnassignedVars:
    '''class for holding the unassigned variables of a CSP. We can extract
       from, re-initialize it, and return variables to it.  Object is
       initialized by passing a select_criteria (to determine the
       order variables are extracted) and the CSP object.

       select_criteria = ['random', 'fixed', 'mrv'] with
       'random' == select a random unassigned variable
       'fixed'  == follow the ordering of the CSP variables (i.e.,
                   csp.variables()[0] before csp.variables()[1]
       'mrv'    == select the variable with minimum values in its current domain
                   break ties by the ordering in the CSP variables.
    '''

    def __init__(self, select_criteria, csp):
        if select_criteria not in ['random', 'fixed', 'mrv']:
            pass  #print "Error UnassignedVars given an illegal selection criteria {}. Must be one of 'random', 'stack', 'queue', or 'mrv'".format(select_criteria)
        self.unassigned = list(csp.variables())
        self.csp = csp
        self._select = select_criteria
        if select_criteria == 'fixed':
            #reverse unassigned list so that we can add and extract from the back
            self.unassigned.reverse()

    def extract(self):
        if not self.unassigned:
            pass  #print "Warning, extracting from empty unassigned list"
            return None
        if self._select == 'random':
            i = random.randint(0, len(self.unassigned) - 1)
            nxtvar = self.unassigned[i]
            self.unassigned[i] = self.unassigned[-1]
            self.unassigned.pop()
            return nxtvar
        if self._select == 'fixed':
            return self.unassigned.pop()
        if self._select == 'mrv':
            nxtvar = min(self.unassigned, key=lambda v: v.curDomainSize())
            self.unassigned.remove(nxtvar)
            return nxtvar

    def empty(self):
        return len(self.unassigned) == 0

    def insert(self, var):
        if not var in self.csp.variables():
            pass  #print "Error, trying to insert variable {} in unassigned that is not in the CSP problem".format(var.name())
        else:
            self.unassigned.append(var)


def bt_search(algo, csp, variableHeuristic, allSolutions, trace, size, cons):
    '''Main interface routine for calling different forms of backtracking search
       algorithm is one of ['BT', 'FC', 'GAC']
       csp is a CSP object specifying the csp problem to solve
       variableHeuristic is one of ['random', 'fixed', 'mrv']
       allSolutions True or False. True meansx we want to find all solutions.
       trace True of False. True means turn on tracing of the algorithm

       bt_search returns a list of solutions. Each solution is itself a list
       of pairs (var, value). Where var is a Variable object, and value is
       a value from its domain.
    '''
    varHeuristics = ['random', 'fixed', 'mrv']
    algorithms = ['BT', 'FC', 'GAC']

    #statistics
    bt_search.nodesExplored = 0

    if variableHeuristic not in varHeuristics:
        pass  #print "Error. Unknown variable heursitics {}. Must be one of {}.".format(
        #variableHeuristic, varHeuristics)
    if algo not in algorithms:
        pass  #print "Error. Unknown algorithm heursitics {}. Must be one of {}.".format(
        #algo, algorithms)

    uv = UnassignedVars(variableHeuristic, csp)
    Variable.clearUndoDict()
    for v in csp.variables():
        v.reset()
    if algo == 'BT':
        solutions = BT(uv, csp, allSolutions, trace)
    elif algo == 'FC':
        for cnstr in csp.constraints():
            if cnstr.arity() == 1:
                FCCheck(cnstr, None,
                        None)  #FC with unary constraints at the root
        solutions = FC(uv, csp, allSolutions, trace)
    elif algo == 'GAC':
        # for var in csp.variables():
        #     print(var._name, var.curDomain())
        GACEnforce(csp.constraints(), csp, None, None)  #GAC at the root
        # for var in csp.variables():
        #     print(var._name, var.curDomain())
        solutions = GAC(uv, csp, cons, allSolutions, trace, size)
        # print(solutions)
    return [solutions], bt_search.nodesExplored


def BT(unAssignedVars, csp, allSolutions, trace):
    '''Backtracking Search. unAssignedVars is the current set of
       unassigned variables.  csp is the csp problem, allSolutions is
       True if you want all solutionss trace if you want some tracing
       of variable assignments tried and constraints failed. Returns
       the set of solutions found.

      To handle finding 'allSolutions', at every stage we collect
      up the solutions returned by the recursive  calls, and
      then return a list of all of them.

      If we are only looking for one solution we stop trying
      further values of the variable currently being tried as
      soon as one of the recursive calls returns some solutions.
    '''
    if unAssignedVars.empty():
        if trace:
            pass  #print "{} Solution Found".format(csp.name())
        soln = []
        for v in csp.variables():
            soln.append((v, v.getValue()))
        return [soln]  #each call returns a list of solutions found
    bt_search.nodesExplored += 1
    solns = []  #so far we have no solutions recursive calls
    nxtvar = unAssignedVars.extract()
    if trace:
        pass  #print "==>Trying {}".format(nxtvar.name())
    for val in nxtvar.domain():
        if trace:
            pass  #print "==> {} = {}".format(nxtvar.name(), val)
        nxtvar.setValue(val)
        constraintsOK = True
        for cnstr in csp.constraintsOf(nxtvar):
            # print(cnstr._name)
            if cnstr.numUnassigned() == 0:
                # print("hi")
                # print(cnstr._name)
                if not cnstr.check():
                    # print(cnstr._name)
                    constraintsOK = False
                    if trace:
                        pass  #print "<==falsified constraint\n"
                    break
        if constraintsOK:
            # print("hi")
            new_solns = BT(unAssignedVars, csp, allSolutions, trace)
            if new_solns:
                solns.extend(new_solns)
            if len(solns) > 0 and not allSolutions:
                break  #don't bother with other values of nxtvar
                #as we found a soln.
    nxtvar.unAssign()
    # print(nxtvar._name)
    unAssignedVars.insert(nxtvar)


    return solns


def GAC(unAssignedVar: UnassignedVars, csp, cons, sol=False, trace=False, size=0):
    """
    Implementing GAC/AC-3 for Back tracking
    """
    # for var in csp.variables():
    #     print(var._name, var.curDomain())
    solutions = []
    if unAssignedVar.empty():
        for var in csp.variables():
            solutions.append((var, var.getValue()))
        b1, b2, b3, b4, b5, nxt = apt_solution(solutions, size)
        if b1 == int(cons[0]) and b2 == int(cons[1]) and b3 == int(cons[2]) and b4 == int(cons[3]) and b5 == int(cons[4]):
            print(cons[4])
            return solutions
        return []

    var = unAssignedVar.extract()
    for value in var.curDomain():
        var.setValue(value)
        DWO = False
        if GACEnforce(csp.constraintsOf(var), csp, var, value) == "DWO":
            DWO = True
        if not DWO:
            new_solutions = (GAC(unAssignedVar, csp, cons, False, False, size))
            if new_solutions:
                solutions = new_solutions
                break
        Variable.restoreValues(var, value)
    var.setValue(None)
    unAssignedVar.insert(var)
    return solutions



def GACEnforce(constraint, csp, as_var, as_val):
    """
    Prune all GAC inconsistent values
    """
    # while not constraint is None:
    while constraint != []:
        cnst = constraint.pop(0)
        for var in cnst.scope():
            for value in var.curDomain():
                if not cnst.hasSupport(var, value):
                    var.pruneValue(value, as_var, as_val)
                    if var.curDomainSize() == 0:
                        # print(var._name, cnst._name)
                        return "DWO"
                    # for recheck in csp.constraintsOf(var):
                    for recheck in csp.constraintsOf(var):
                        if recheck != cnst and not recheck in constraint:
                            constraint.append(recheck)
    return "OK"


def apt_solution(sol, size):
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    sol_dict = {}
    # print(sol)
    for (var, val) in sol:
        sol_dict[int(var.name())] = val

    for i in range(0, size):
        for j in range(0, size):
            # print(i, j)
            if (i < (size - 5) and sol_dict[(-1 - (i * size + j))] == "|" and sol_dict[(-1 - ((i+1) * size + j))] == "|" and sol_dict[(-1 - ((i+2) * size + j))] == "|" and sol_dict[(-1 - ((i+3) * size + j))] == "|"  and sol_dict[(-1 - ((i+4) * size + j))] == "|"):
                five += 1
                sol_dict[(-1 - (i * size + j))] = "^"
                sol_dict[(-1 - ((i+1) * size + j))] = "M"
                sol_dict[(-1 - ((i+2) * size + j))] = "M"
                sol_dict[(-1 - ((i+3) * size + j))] = "M"
                sol_dict[(-1 - ((i+4) * size + j))] = "v"
            elif (i < (size - 4) and sol_dict[(-1 - (i * size + j))] == "|" and sol_dict[(-1 - ((i+1) * size + j))] == "|" and sol_dict[(-1 - ((i+2) * size + j))] == "|" and sol_dict[(-1 - ((i+3) * size + j))] == "|"):
                four += 1
                sol_dict[(-1 - (i * size + j))] = "^"
                sol_dict[(-1 - ((i+1) * size + j))] = "M"
                sol_dict[(-1 - ((i+2) * size + j))] = "M"
                sol_dict[(-1 - ((i+3) * size + j))] = "v"
            elif (i < (size - 3) and sol_dict[(-1 - (i * size + j))] == "|" and sol_dict[(-1 - ((i+1) * size + j))] == "|" and sol_dict[(-1 - ((i+2) * size + j))] == "|"):
                three += 1
                sol_dict[(-1 - (i * size + j))] = "^"
                sol_dict[(-1 - ((i+1) * size + j))] = "M"
                sol_dict[(-1 - ((i+2) * size + j))] = "v"
            elif  (i < (size - 2) and sol_dict[(-1 - (i * size + j))] == "|" and sol_dict[(-1 - ((i+1) * size + j))] == "|"):
                two += 1
                sol_dict[(-1 - (i * size + j))] = "^"
                sol_dict[(-1 - ((i+1) * size + j))] = "v"
            if (j < (size - 4) and sol_dict[(-1 - (i * size + j))] == "-" and sol_dict[(-1 - (i * size + j+1))] == "-" and sol_dict[(-1 - (i * size + j+2))] == "-" and sol_dict[(-1 - (i * size + j+3))] == "-" and sol_dict[(-1 - (i * size + j+4))] == "-"):
                five += 1
                sol_dict[(-1 - (i * size + j))]  = "<"
                sol_dict[(-1 - (i * size + j+1))] = "M"
                sol_dict[(-1 - (i * size + j+2))] = "M"
                sol_dict[(-1 - (i * size + j+3))] = "M"
                sol_dict[(-1 - (i * size + j+4))] = ">"
            elif (j < (size - 4) and sol_dict[(-1 - (i * size + j))] == "-" and sol_dict[(-1 - (i * size + j+1))] == "-" and sol_dict[(-1 - (i * size + j+2))] == "-" and sol_dict[(-1 - (i * size + j+3))] == "-"):
                four += 1
                sol_dict[(-1 - (i * size + j))]  = "<"
                sol_dict[(-1 - (i * size + j+1))] = "M"
                sol_dict[(-1 - (i * size + j+2))] = "M"
                sol_dict[(-1 - (i * size + j+3))] = ">"
            elif (j < (size - 3) and sol_dict[(-1 - (i * size + j))] == "-" and sol_dict[(-1 - (i * size + j+1))] == "-" and sol_dict[(-1 - (i * size + j+2))] == "-"):
                three += 1
                sol_dict[(-1 - (i * size + j))]  = "<"
                sol_dict[(-1 - (i * size + j+1))] = "M"
                sol_dict[(-1 - (i * size + j+2))] = ">"
            elif (j < (size - 2) and sol_dict[(-1 - (i * size + j))] == "-" and sol_dict[(-1 - (i * size + j+1))] == "-"):
                two += 1
                sol_dict[(-1 - (i * size + j))]  = "<"
                sol_dict[(-1 - (i * size + j+1))] = ">"

    for i in range(1, size-1):
        for j in range(1, size-1):
            if sol_dict[(-1 - (i * size + j))] == "-" or sol_dict[(-1 - (i * size + j))] == "|":
                one += 1
                sol_dict[(-1 - (i * size + j))] = "S"

    return one, two, three, four, five, sol_dict
