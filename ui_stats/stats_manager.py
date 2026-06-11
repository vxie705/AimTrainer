from typing import List


class StatsManager:

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.hits: int = 0
        self.misses: int = 0
        self.total_shots: int = 0
        self._reaction_times: List[float] = []
        self.combo: int = 0
        self.best_combo: int = 0
        self.score: int = 0
        self.total_targets_spawned: int = 0
        self.total_targets_hit: int = 0

    def register_shot(self) -> None:
        self.total_shots += 1

    def register_hit(self, reaction_time_ms: float) -> None:
        self.hits += 1
        self.total_targets_hit += 1
        self._reaction_times.append(reaction_time_ms)
        self.combo += 1
        if self.combo > self.best_combo:
            self.best_combo = self.combo
        speed_bonus = max(0, int((1000 - reaction_time_ms) / 10))
        combo_bonus = self.combo * 10
        self.score += 100 + speed_bonus + combo_bonus

    def register_miss(self) -> None:
        self.misses += 1
        self.combo = 0

    def register_target_spawned(self) -> None:
        self.total_targets_spawned += 1

    @property
    def accuracy(self) -> float:
        if self.total_shots == 0:
            return 0.0
        return (self.hits / self.total_shots) * 100.0

    @property
    def avg_reaction_time_ms(self) -> float:
        if not self._reaction_times:
            return 0.0
        return sum(self._reaction_times) / len(self._reaction_times)

    @property
    def best_reaction_time_ms(self) -> float:
        if not self._reaction_times:
            return 0.0
        return min(self._reaction_times)

    @property
    def last_reaction_time_ms(self) -> float:
        if not self._reaction_times:
            return 0.0
        return self._reaction_times[-1]

    def get_summary_lines(self) -> List[str]:
        return [
            f"Score: {self.score}",
            f"Hits: {self.hits}  Misses: {self.misses}",
            f"Accuracy: {self.accuracy:.1f}%",
            f"Avg Reaction: {self.avg_reaction_time_ms:.0f} ms",
            f"Best Reaction: {self.best_reaction_time_ms:.0f} ms",
            f"Last Reaction: {self.last_reaction_time_ms:.0f} ms",
            f"Combo: {self.combo}  Best: {self.best_combo}",
        ]