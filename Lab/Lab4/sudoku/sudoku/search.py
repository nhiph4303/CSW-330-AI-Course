"""
In search.py, you will implement Backtracking and AC-3 for Sudoku.
Complete Exercise 2 (Backtracking) and Exercise 3 (AC-3) here.
"""

from csp import *
from copy import deepcopy
import util

# ---------- High-level entry points ----------

def Backtracking_Search(csp_inst):
    """
    [Exercise 2] Standard Backtracking Search that calls Recursive_Backtracking.
    """
    # Preprocessing: AC3 to reduce domains before starting backtracking
    try:
        ac3 = AC3(csp_inst)     # run AC-3 before searching
    except:
        ac3 = True          # in case AC3 is not implemented yet, continue anyway
    if ac3 is False:
        return "Failure"    # AC-3 detected inconsistency

    # Initial (possibly partial) assignment from singleton domains (optional helper)
    assignment = {v: csp_inst.values[v]
                  for v in csp_inst.variables
                  if len(csp_inst.values[v]) == 1}

    return Recursive_Backtracking(assignment, csp_inst)


def Recursive_Backtracking(assignment, csp_inst):
    """
    [Exercise 2] Recursive backtracking:
      - If assignment complete => return csp_inst.values
      - Select unassigned variable (use MRV)
      - For each value (optionally order by LCV)
         * If consistent, assign and propagate (Inference / Forward Checking or AC3)
         * Recurse
         * Undo on failure
    """
    # TODO [E2]: Implement recursive backtracking
    util.raiseNotDefined()


# ---------- Inference / Propagation ----------

def Inference(assignment, inferences, csp_inst, var, value):
    """
    [Exercise 2] Implement forward checking (unit propagation optional):
      - Remove 'value' from each peer's domain
      - If a domain becomes empty => 'FAILURE'
      - If a domain becomes singleton => enqueue for further propagation
    Return 'FAILURE' or a dict {var: previous_domain} to allow restoration.
    """
    # TODO [E2]: Forward checking
    util.raiseNotDefined()


def AC3(csp_inst, queue=None):
    """
    [Exercise 3] AC-3 algorithm:
      - Initialize queue with all arcs (xi, xj), or use provided queue
      - While queue not empty:
          * if Revise(csp_inst, xi, xj) and domain(xi) becomes empty => return False
          * if revised, add (xk, xi) for all xk in peers[xi] - {xj}
      - Return True if arc-consistent
    """
    # TODO [E3]: Implement AC-3
    util.raiseNotDefined()


def Revise(csp_inst, xi, xj):
    """
    [Exercise 3] REVISE:
      - Remove any value a in domain(xi) that has no supporting value b in domain(xj)
        under the constraint a != b.
    Return True iff a removal happened.
    """
    # TODO [E3]: Implement REVISE
    util.raiseNotDefined()


# ---------- Heuristics & Checks ----------

def Order_Domain_Values(var, assignment, csp_inst):
    """
    [Exercise 2] OPTIONAL LCV: order var's domain least-constraining first.
    Base version may just return as-is.
    """
    # TODO [E2 optional]: LCV
    return list(csp_inst.values[var])


def Select_Unassigned_Variables(assignment, csp_inst):
    """
    [Exercise 2] MRV: choose an unassigned variable with the smallest domain size.
    """
    # TODO [E2]: MRV
    util.raiseNotDefined()


def isComplete(assignment):
    """
    [Exercise 2] Check if assignment is complete (all 81 squares assigned).
    """
    # TODO [E2]
    util.raiseNotDefined()


def isConsistent(var, value, assignment, csp_inst):
    """
    [Exercise 2] Check consistency: no assigned peer has the same value.
    """
    # TODO [E2]
    util.raiseNotDefined()


# ---------- Display / Output (keep provided) ----------

def display(values):
    """
    Display the solved sudoku on screen
    """
    for row in rows:
        if row in 'DG':
            print("-------------------------------------------")
        for col in cols:
            if col in '47':
                print(' | ', values[row + col], ' ', end=' ')
            else:
                print(values[row + col], ' ', end=' ')
        print(end='\n')

def write(values):
    """
    Write the string output of solved sudoku to file
    """
    output = ""
    for variable in squares:
        output = output + values[variable]
    return output
