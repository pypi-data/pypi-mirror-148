from collections import Counter

from . import Query

from _qepler import QCell

class BaseAlgorithm:
    QLCELL_COUNT = 25

    def __init__(self):
        self.qcells = [QCell() for _ in range(BaseAlgorithm.QLCELL_COUNT)]

    def update(self, models):
        for qcell in self.qcells:
            qcell.decay()

        qid_counter = Counter()

        for m in models:
            qid = m._program.qid

            if qid_counter[qid] >= 6:
                continue

            self.qcells[qid].update(m._program)
            qid_counter[qid] += 1

    def update_priors(self, priors, reset):
        for qcell in self.qcells:
            qcell.update_priors(priors, reset)

    def generate_programs(self, ar0_codes, ar1_codes, ar2_codes, output_code, max_complexity, query_codes):
        query = Query(query_codes, ar0_codes, ar1_codes, ar2_codes)

        res = []
        for qid, qcell in enumerate(self.qcells):
            programs = qcell.generate_programs(ar0_codes, ar1_codes, ar2_codes, output_code, query, max_complexity)

            for p in programs:
                plen = len(p)
                if not plen:
                    continue
                if plen <= max_complexity + 1 and query(p):
                    p.qid = qid
                    res.append(p)

        return res
