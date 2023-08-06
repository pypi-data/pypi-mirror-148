import dataclasses


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class SortCodeSubstitution:
    orig_code: int
    new_code: int


class SortCodeSubstitutionTable:
    __slots__ = ("_sort_code_substitutions",)

    def __init__(self) -> None:
        self._sort_code_substitutions: dict[int, int] = {}

    def reload(self, lines: list[str]) -> None:
        lst = [self._parse_line(line) for line in lines]
        self._sort_code_substitutions = {x.orig_code: x.new_code for x in lst}

    def try_get_substitution(self, sort_code: int) -> int | None:
        if sort_code in self._sort_code_substitutions:
            return self._sort_code_substitutions[sort_code]
        return None

    def length(self) -> int:
        return len(self._sort_code_substitutions)

    @staticmethod
    def _parse_line(line: str) -> SortCodeSubstitution:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid record: {line}")

        try:
            orig_code = int(parts[0])
            new_code = int(parts[1])
        except ValueError:
            raise ValueError(f"Invalid record: {line}")

        return SortCodeSubstitution(orig_code=orig_code, new_code=new_code)
