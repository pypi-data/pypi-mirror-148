
class PMF:
    WDEFAULT = 1.0

    def __init__(self):
        self._pmf = {}

    def get(self, keys):
        return [self._pmf.get(op, PMF.WDEFAULT) for op in keys]

    def set(self, key, val):
        self._pmf[key] = val

    def update(self, key, val):
        newval = self._pmf.get(key, PMF.WDEFAULT) * val
        self._pmf[key] = newval

    def update_posteriors(self, p) -> None:
        reg_codes = set(p[ix] for ix in range(1, len(p)) if p.arity_at(ix) == 0)
        for c in reg_codes:
            self._received[c] += 1

            # Use the expectation value of the posterior (beta) distribution
            posterior = (self._received[c] + 1) / (self._sent[c] + 2)
            self.set(c, posterior)
