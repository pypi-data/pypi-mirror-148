import dataclasses
import enum


class ModMode(str, enum.Enum):
    Mod10 = "MOD10"
    Mod11 = "MOD11"
    DblAl = "DBLAL"


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class Weights:
    u: int
    v: int
    w: int
    x: int
    y: int
    z: int
    a: int
    b: int
    c: int
    d: int
    e: int
    f: int
    g: int
    h: int


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class ModRule:
    start_code: int
    end_code: int
    mod_mode: ModMode
    weights: Weights
    exception: int | None


class WeightTable:
    __slots__ = ("_mod_rules",)

    def __init__(self) -> None:
        self._mod_rules: list[ModRule] = []

    def reload(self, lines: list[str]) -> None:
        lst = [self._parse_line(line) for line in lines]
        self._mod_rules = lst

    def length(self) -> int:
        return len(self._mod_rules)

    def try_get_rules(self, sort_code: int) -> list[ModRule]:
        return [x for x in self._mod_rules if x.start_code <= sort_code <= x.end_code]

    @staticmethod
    def _parse_weights(parts: list[str]) -> Weights:
        return Weights(
            u=int(parts[0]),
            v=int(parts[1]),
            w=int(parts[2]),
            x=int(parts[3]),
            y=int(parts[4]),
            z=int(parts[5]),
            a=int(parts[6]),
            b=int(parts[7]),
            c=int(parts[8]),
            d=int(parts[9]),
            e=int(parts[10]),
            f=int(parts[11]),
            g=int(parts[12]),
            h=int(parts[13]),
        )

    @staticmethod
    def _parse_line(line: str) -> ModRule:
        parts = line.split()
        if len(parts) not in (17, 18):
            raise ValueError(f"Invalid record: {line}")

        try:
            start_code = int(parts[0])
            end_code = int(parts[1])
            mod_mode = ModMode(parts[2])
        except ValueError:
            raise ValueError(f"Invalid record: {line}")

        try:
            weights = WeightTable._parse_weights(parts[3:17])
        except ValueError:
            raise ValueError(f"Invalid record: {line}")

        if len(parts) == 18:
            try:
                exception = int(parts[17])
            except ValueError:
                raise ValueError(f"Invalid record: {line}")
        else:
            exception = None

        return ModRule(
            start_code=start_code,
            end_code=end_code,
            mod_mode=mod_mode,
            weights=weights,
            exception=exception,
        )
