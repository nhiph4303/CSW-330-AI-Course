"""CSP model for Sudoku (STUDENT STARTER).

Complete Exercise 1 in this file:
- Build unitlist (27 units: 9 rows, 9 cols, 9 boxes)
- Build units (3 per square)
- Build peers (set union of units - {self})
- Build constraints (binary inequality arcs (xi, xj))
- Parse the input grid into self.values (domains per square)
"""

from util import *
from typing import Dict, List, Set

class csp:
    def __init__(self, domain: str = digits, grid: str = ""):
        """Create a CSP instance for a Sudoku puzzle.

        Required (Exercise 1):
          - self.unitlist: list[list[str]]
          - self.units:    dict[str, list[list[str]]]
          - self.peers:    dict[str, set[str]]
          - self.constraints: set[tuple[str, str]]
          - self.values:   dict[str, str] parsed from `grid`
        """
        # Given
        self.variables = squares
        self.domain = domain

        # TODO [E1]: Build unit lists for rows, columns, and 3x3 boxes
        # row_units = ...
        # col_units = ...
        # box_units = ...
        # self.unitlist = ...

        # 9 row units
        row_units = [cross(r, cols) for r in rows]
        # 9 column units
        col_units = [cross(rows, c) for c in cols]
        # 9 box units
        row_boxes = ['ABC', 'DEF', 'GHI']
        col_boxes = ['123', '456', '789']
        box_units = [cross(rs, cs) for rs in row_boxes for cs in col_boxes]
        self.unitlist = row_units + col_units + box_units

        # TODO [E1]: For each square, list the 3 units it belongs to
        # self.units = { ... }
        self.units = {s: [u for u in self.unitlist if s in u] for s in self.variables}

        # TODO [E1]: For each square, compute its peers (other squares in its units)
        # self.peers = { ... }
        self.peers = {s: set(sum(self.units[s], [])) - {s} for s in self.variables}

        # TODO [E1]: Build binary inequality constraints (xi, xj) for all peers
        # self.constraints = ...
        constraints = set()
        for xi in self.variables:
            for xj in self.peers[xi]:
                constraints.add((xi, xj))
        self.constraints = constraints

        # If grid is empty string, initialize every square to full domain
        self.values = (
            self.getDict(grid) 
            if grid and len(grid.strip()) == 81
             else {s: self.domain for s in self.variables}
            )

    def getDict(self, grid: str = "") -> Dict[str, str]:
        """Parse an 81-char grid string into a dict mapping each square to a domain string.

        Rules:
          - '0'        => unassigned => full domain (use self.domain)
          - '1'..'9'   => assigned    => singleton string (e.g., '4')
        """
        grid = grid.strip()
        if len(grid) != 81:
            raise ValueError("Grid string must be exactly 81 characters")

        values = {}

        # TODO [E1]: Fill values for each square based on grid[i]
        # for i, cell in enumerate(self.variables):
        #     ch = grid[i]
        #     if ch in '0':          # empty cell
        #         values[cell] = self.domain
        #     else:                   # given number
        #         values[cell] = ch
        for i, cell in enumerate(self.variables):
            ch = grid[i]
            if ch in "0.":
                values[cell] = self.domain
            elif ch in digits:
                values[cell] = ch
            else:
                raise ValueError(f"Invalid character '{ch}' at position {i}")
        return values