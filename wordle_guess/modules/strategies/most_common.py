from . import strategy

class MostCommonStrategy(strategy.Strategy):
    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        return list(sorted(candidates.keys(), key=lambda k: candidates[k], reverse=True))