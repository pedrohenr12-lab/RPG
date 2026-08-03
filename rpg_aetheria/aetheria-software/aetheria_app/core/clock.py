from __future__ import annotations

from dataclasses import dataclass

from ..models import PlayerSession


MINUTES_PER_DAY = 24 * 60


@dataclass(frozen=True)
class TimeStamp:
    day: int
    hour: int
    minute: int

    @property
    def absolute_minute(self) -> int:
        return max(0, self.day - 1) * MINUTES_PER_DAY + self.hour * 60 + self.minute

    @property
    def label(self) -> str:
        return f"Dia {self.day}, {self.hour:02d}:{self.minute:02d}"


class GameClock:
    """Relógio canônico. O PlayerSession continua guardando os campos por compatibilidade."""

    def __init__(self, session: PlayerSession):
        self.session = session

    @property
    def now(self) -> TimeStamp:
        return TimeStamp(self.session.day, self.session.hour, self.session.minute)

    @property
    def absolute_minute(self) -> int:
        return self.now.absolute_minute

    def advance(self, minutes: int, *, traveling: bool = False) -> tuple[TimeStamp, TimeStamp]:
        before = self.now
        self.session.advance_minutes(minutes, traveling=traveling)
        return before, self.now

    def due_in(self, minutes: int) -> TimeStamp:
        total = self.absolute_minute + max(0, int(minutes))
        day_index, within = divmod(total, MINUTES_PER_DAY)
        hour, minute = divmod(within, 60)
        return TimeStamp(day_index + 1, hour, minute)

    @staticmethod
    def from_absolute(total: int) -> TimeStamp:
        day_index, within = divmod(max(0, int(total)), MINUTES_PER_DAY)
        hour, minute = divmod(within, 60)
        return TimeStamp(day_index + 1, hour, minute)
