import hypothesis
from hypothesis import strategies

from preface import argsort, flattened, get, grouped, indexed


@hypothesis.given(strategies.sets(strategies.integers(), min_size=1))
def test_get(s):
    assert get(s) in s


@hypothesis.given(strategies.lists(strategies.integers()))
def test_argsort(lst):
    assert list(sorted(lst)) == [lst[i] for i in argsort(lst)]


@hypothesis.given(strategies.lists(strategies.lists(strategies.integers())))
def test_flattened(seq):
    flat = flattened(seq)
    assert len(flat) == sum(len(subseq) for subseq in seq)
    for subseq in seq:
        for item in subseq:
            assert item in flat


@hypothesis.given(
    strategies.lists(strategies.integers(min_value=-100, max_value=100)),
    strategies.integers(min_value=1, max_value=5),
)
def test_grouped(seq, size):
    for window in grouped(seq, size):
        assert len(window) == size


@hypothesis.strategies.composite
def list_and_indices(draw, elements=strategies.integers()):
    lst = draw(strategies.lists(elements, min_size=1))
    indices = draw(
        strategies.lists(
            strategies.integers(min_value=0, max_value=len(lst) - 1), min_size=1
        )
    )
    return (lst, indices)


@hypothesis.given(list_and_indices())
def test_indexed(args):
    seq, indices = args
    for elem in indexed(seq, indices):
        assert elem in seq
