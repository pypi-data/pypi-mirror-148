from typing import Any, Dict, Reversible, Union

StrDict = Dict[str, object]
Key = Union[str, Reversible[str]]
Primitive = Union[str, int, float, bool, None]


def _index(dct: StrDict, key: str) -> StrDict:
    new_dct = dct[key]

    if not isinstance(new_dct, dict):
        raise ValueError(f"Cannot index dct with key '{key}'")

    return new_dct


def get(dct: StrDict, key: Key, sep: str = ".") -> Any:
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))
    while len(key) > 1:
        dct = _index(dct, key.pop())

    return dct[key[0]]


def contains(dct: StrDict, key: Key, sep: str = ".") -> bool:
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))
    while len(key) > 1:
        popped = key.pop()
        if popped not in dct:
            return False
        dct = _index(dct, popped)

    return key[0] in dct


def delete(dct: StrDict, key: Key, sep: str = ".") -> None:
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))

    while len(key) > 1:
        dct = _index(dct, key.pop())

    del dct[key[0]]


def set(dct: StrDict, key: Key, value: Any, sep: str = ".") -> None:
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))

    while len(key) > 1:
        k = key.pop()

        if k not in dct:
            dct[k] = {}

        dct = _index(dct, k)

    dct[key[0]] = value


def merge(*dcts: StrDict) -> StrDict:
    result: StrDict = {}
    for dct in dcts:
        for key, value in flattened(dct).items():
            set(result, key, value)

    return result


def flattened(dct: Dict[str, Any]) -> Dict[str, Primitive]:
    new = {}
    for key, value in dct.items():
        if isinstance(value, dict):
            for nested_key, nested_value in flattened(value).items():
                new[key + "." + nested_key] = nested_value
            continue

        new[key] = value

    return new
