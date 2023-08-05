"""Some helper functions and classes that I want in nearly every project."""

__version__ = "0.1.0"

import enum
import sys
from typing import (
    Iterable,
    Iterator,
    List,
    NoReturn,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from . import dict  # noqa: F401

T = TypeVar("T")

# region types

Result = Union[T, Exception]


S = TypeVar("S", bound="SumType")


class SumType(enum.Enum):
    @classmethod
    def new(cls: Type[S], s: Union[str, int]) -> S:
        if isinstance(s, str):
            # I like using dashes in identifiers/string literals
            s = s.replace("-", "_")
            names = [c.name for c in cls]
            assert s in names, f"{cls.__name__} '{s}' must be one of {', '.join(names)}"
            return cls[s]

        if isinstance(s, int):
            for c in cls:
                if c.value == s:
                    return c

            values = [c.value for c in cls]
            raise ValueError(f"{cls.__name__} '{s}' must be one of {', '.join(values)}")

        raise ValueError(f"Can't use '{s}' as a literal!")

    # I like to use names as values for these; I don't really care about the actual value
    def __str__(self) -> str:
        return self.name.replace("_", "-")

    def __repr__(self) -> str:
        return str(self)

    @property
    def formatted(self) -> str:
        words = str(self).split("-")
        words = [word.capitalize() for word in words]
        return " ".join(words)

    @staticmethod
    def auto() -> enum.auto:
        return enum.auto()


# endregion


# region global functions


def get(s: Set[T]) -> T:
    """
    Returns a arbitrary (first) element of s
    """
    return next(iter(s))


def argsort(lst: Sequence[T], reverse: bool = False) -> List[int]:
    return [i for e, i in sorted(((e, i) for i, e in enumerate(lst)), reverse=reverse)]


def flattened(nested_list: List[List[T]]) -> List[T]:
    """
    Takes a list of lists and returns a flattened list

    Check list(itertools.chain(*regular_list)) for performance
    """
    return [item for sublist in nested_list for item in sublist]


def indexed(lst: Sequence[T], indices: Iterable[int]) -> List[T]:
    result = []
    for i in indices:
        result.append(lst[i])
    return result


def grouped(things: Sequence[T], size: int = 1) -> Iterator[Tuple[T, ...]]:
    """
    Produces a sliding window over 'things'.

    Example:
        grouped([1, 2, 3, 4], 2) == [(1, 2), (2, 3), (3, 4)]
    """
    rows = [things[i:] for i in range(size)]

    return zip(*rows)


def unwrap(maybe: Result[T]) -> T:
    if isinstance(maybe, Exception):
        raise maybe

    return maybe


def never(value: NoReturn) -> NoReturn:
    raise AssertionError(f"Unhandled value: {value} ({type(value).__name__})")


def eprint(*args, **kwargs):  # type: ignore
    """
    Print to stderr.
    """
    print(*args, file=sys.stderr, **kwargs)


# endregion
