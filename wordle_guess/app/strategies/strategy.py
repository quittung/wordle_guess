from multiprocessing.pool import Pool

class Strategy(object):
    def __init__(self, pool: Pool = None) -> None:
        self.pool = pool

    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        return candidates

    def sort_initial(self, candidates: dict[str, int]) -> list[str]:
        return self.sort_candidates(candidates)