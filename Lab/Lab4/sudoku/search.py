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
    if isComplete(assignment):
        return {
            v: (csp_inst.values[v] if len(csp_inst.values[v]) == 1 else assignment[v])
            for v in csp_inst.variables
        }

    var = Select_Unassigned_Variables(assignment, csp_inst)

    for value in Order_Domain_Values(var, assignment, csp_inst):
        if isConsistent(var, value, assignment, csp_inst):
            # Lưu trạng thái để có thể hoàn tác
            saved_domain = csp_inst.values[var]
            csp_inst.values[var] = value
            assignment[var] = value

            inferences = {}
            fc = Inference(assignment, inferences, csp_inst, var, value)
            if fc != "FAILURE":
                result = Recursive_Backtracking(assignment, csp_inst)
                if result:
                    return result

            # Hoàn tác (undo) khi nhánh thất bại
            for v, old_dom in inferences.items():
                csp_inst.values[v] = old_dom
            csp_inst.values[var] = saved_domain
            assignment.pop(var, None)

    return None


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
    queue = []
    # B1: loại 'value' khỏi miền của tất cả peers(var)
    for p in csp_inst.peers[var]:
        dom = csp_inst.values[p]
        if value in dom:
            if p not in inferences:     # lưu miền cũ để hoàn tác
                inferences[p] = dom
            new_dom = dom.replace(value, "")
            csp_inst.values[p] = new_dom
            if len(new_dom) == 0:
                return "FAILURE"
            if len(new_dom) == 1 and p not in assignment:
                assignment[p] = new_dom
                queue.append(p)

    # B2: lan truyền các biến vừa trở thành đơn giá trị
    while queue:
        s = queue.pop()
        val_s = csp_inst.values[s]      # dạng '3' (chuỗi 1 ký tự)
        for p in csp_inst.peers[s]:
            dom = csp_inst.values[p]
            if len(dom) > 1 and val_s in dom:
                if p not in inferences:
                    inferences[p] = dom
                new_dom = dom.replace(val_s, "")
                csp_inst.values[p] = new_dom
                if len(new_dom) == 0:
                    return "FAILURE"
                if len(new_dom) == 1 and p not in assignment:
                    assignment[p] = new_dom
                    queue.append(p)

    return inferences


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
    if queue is None:
        queue = list(csp_inst.constraints)  # tất cả các cung (xi, xj)

    while queue:
        xi, xj = queue.pop(0)
        if Revise(csp_inst, xi, xj):
            if len(csp_inst.values[xi]) == 0:
                return False  # domain rỗng → vô nghiệm
            # thêm lại các cung (xk, xi) để kiểm tra lan truyền
            for xk in csp_inst.peers[xi] - {xj}:
                queue.append((xk, xi))
    return True

    util.raiseNotDefined()


def Revise(csp_inst, xi, xj):
    """
    [Exercise 3] REVISE:
      - Remove any value a in domain(xi) that has no supporting value b in domain(xj)
        under the constraint a != b.
    Return True iff a removal happened.
    """
    # TODO [E3]: Implement REVISE
    revised = False
    to_remove = []
    for a in csp_inst.values[xi]:
        # nếu mọi b trong domain(xj) đều bằng a => không hợp lệ
        if all(a == b for b in csp_inst.values[xj]):
            to_remove.append(a)
    if to_remove:
        for a in to_remove:
            csp_inst.values[xi] = csp_inst.values[xi].replace(a, "")
        revised = True
    return revised
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
    unassigned = [v for v in csp_inst.variables if v not in assignment]
    return min(unassigned, key=lambda v: len(csp_inst.values[v]))


def isComplete(assignment):
    """
    [Exercise 2] Check if assignment is complete (all 81 squares assigned).
    """
    # TODO [E2]
    return len(assignment) == len(squares)
    

def isConsistent(var, value, assignment, csp_inst):
    """
    [Exercise 2] Check consistency: no assigned peer has the same value.
    """
    # TODO [E2]
    for peer in csp_inst.peers[var]:
        if peer in assignment and assignment[peer] == value:
            return False
    return True


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
