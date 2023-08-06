import random
from typing import List
from .._program import Program


class Query:
    def __init__(self, query_codes: List[int], ar0_codes=[], ar1_codes=[], ar2_codes=[]):
        if isinstance(query_codes, Program):
            raise ValueError("The query accepts a sequence of codes, not a full Program.")
        self.query_codes = query_codes
        self.query_size = len(query_codes)
        self.ar0_codes = ar0_codes
        self.ar1_codes = ar1_codes
        self.ar2_codes = ar2_codes
        self.output_code = query_codes[0]

    def __call__(self, p: Program) -> bool:
        """Match programs p to this query sequence."""

        plen = len(p)
        ixP = 0
        ixQP = 0
        while 1:
            if ixQP >= self.query_size and ixP >= plen:
                return True

            qcode = self.query_codes[ixQP]

            if qcode == 0:
                if not p.arity_at(ixP) == 0:
                    return False
            elif qcode == 1:
                if not p.arity_at(ixP) == 1:
                    return False
            elif qcode == 2:
                if not p.arity_at(ixP) == 2:
                    return False

            elif qcode == 3:
                offset = self._consume_wildcard(self.query_codes[ixQP:])
                ixQP += offset

                st_end = p.find_end(ixP)
                program_subtree = p._codes[ixP:st_end]
                ixP = st_end - 1
                if len(program_subtree) - 1 > self.n_edges:
                    return False

                subtree_terminals = set(filter(lambda code: Program.arity_of(1, code) == 0, program_subtree))
                if self.must_contain.difference(subtree_terminals):
                    return False
                if self.cant_contain.intersection(subtree_terminals):
                    return False

            elif qcode == 4:
                ixQP += 1
                banned_terminal = self.query_codes[ixQP]
                if not p.arity_at(ixP) == 0:
                    return False
                if p[ixP] == banned_terminal:
                    return False

            else:
                if not qcode == p[ixP]:
                    return False

            ixP += 1
            ixQP += 1

        return True

    def partial_codes(self) -> List:
        """Return a partially filled out code sequence for the QCell to complete.
        The complete program is always expected to match the user query.

        The partially filled out code sequence either has elements (op_codes, reg_codes) or (None, None)."""
        res = []
        ix = 0
        while ix < len(self.query_codes):
            code = self.query_codes[ix]

            if code == 0:
                res.append(([], self.ar0_codes))
            elif code == 1:
                res.append((self.ar1_codes, []))
            elif code == 2:
                res.append((self.ar2_codes, []))

            elif code == 3:
                ix += self._consume_wildcard(self.query_codes[ix:])
                if self.must_contain:
                    available_terms = set(random.choices(self.ar0_codes, k=max(len(self.must_contain), 30)))
                    available_terms = list(available_terms.union(self.must_contain).difference(self.cant_contain))
                    available_codes = self.ar1_codes + self.ar2_codes
                else:
                    available_codes, available_terms = None, None

                min_size = 2 * (len(self.must_contain) - 1)
                max_size = min(10, self.n_edges)
                subtree_size = random.randint(min_size, max_size)
                res.extend([(available_codes, available_terms)] * subtree_size)

            elif code == 4:
                ix += 1
                available = self.ar0_codes[:]
                available.remove(self.query_codes[ix])
                res.append(([], available))

            else:
                a = code // 1000
                a = 0 if a >= 10 else a
                if a:
                    res.append(([code], []))
                else:
                    res.append(([], [code]))

            ix += 1

        return res + [(None, None)] * (Program.SIZE - len(res))

    def _consume_wildcard(self, codes):
        self.must_contain = set()
        self.cant_contain = set()
        ix = 1
        while 1:
            code = codes[ix]
            if code >= 50 and code <= 80:
                self.n_edges = code - 50
                break

            if code == 4:
                self.cant_contain.add(codes[ix + 1])
                ix += 2
                continue

            self.must_contain.add(codes[ix])
            ix += 1

        return ix + 1
