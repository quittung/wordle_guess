class Strategy(object):
    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        return candidates

    def sort_initial(self, candidates: dict[str, int]) -> list[str]:
        return self.sort_candidates(candidates)