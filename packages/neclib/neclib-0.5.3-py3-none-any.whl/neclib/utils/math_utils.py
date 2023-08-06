"""Utility functions for arithmetic operations."""

__all__ = ["clip", "frange", "discretize", "counter"]

import itertools
import math
from typing import Generator

from ..typing import Literal


def clip(
    value: float, minimum: float = None, maximum: float = None, *, absmax: float = None
) -> float:
    """Limit the ``value`` to the range [``minimum``, ``maximum``].

    Parameters
    ----------
    value
        Arbitrary parameter.
    minimum
        Lower limit of ``value``.
    maximum
        Upper limit of ``value``.
    absmax
        Upper limit of absolute value of ``value``.

    Examples
    --------
    >>> clip(1.2, 0, 1)
    1
    >>> clip(41, 0, 100)
    41
    >>> clip(-4, absmax=3)
    -3

    """
    if absmax is not None:
        minimum, maximum = -1 * abs(absmax), abs(absmax)
    if minimum > maximum:
        raise ValueError("Minimum should be less than maximum.")
    return min(max(minimum, value), maximum)


def frange(
    start: float, stop: float, step: float = 1.0, *, inclusive: bool = False
) -> Generator[float, None, None]:
    """Float version of built-in ``range``, with support for stop value inclusive.

    Parameters
    ----------
    start
        First value to be yielded.
    stop
        Last value to be yielded never exceeds this limit.
    step
        Difference between successive 2 values to be yielded.
    inclusive
        If ``True``, ``stop`` value can be yielded when ``stop - start`` is multiple of
        ``step``.

    Notes
    -----
    Because of floating point overflow, errors may appear when ``print``-ing the result,
    but it's the same as almost equivalent function ``numpy.arange``.

    Examples
    --------
    >>> list(frange(0, 1, 0.2))
    [0, 0.2, 0.4, 0.6, 0.8]
    >>> list(frange(0, 1, 0.2, inclusive=True))
    [0, 0.2, 0.4, 0.6, 0.8, 1]

    """
    if inclusive:
        num = -1 * math.ceil((start - stop) / step) + 1
        # HACK: ``-1 * ceil(x) + 1`` is ceiling function, but if ``x`` is integer,
        # return ``ceil(x) + 1``, so no ``x`` satisfies ``quasi_ceil(x) == x``.
    else:
        num = math.ceil((stop - start) / step)

    for i in range(num):
        yield start + (step * i)


def discretize(
    value: float,
    start: float = 0.0,
    step: float = 1.0,
    *,
    method: Literal["nearest", "ceil", "floor"] = "nearest",
) -> float:
    """Convert ``value`` to nearest element of arithmetic sequence.

    Parameters
    ----------
    value
        Parameter to discretize.
    start
        First element of element of arithmetic sequence.
    step
        Difference between the consecutive 2 elements of the sequence.
    method
        Discretizing method.

    """
    discretizer = {"nearest": round, "ceil": math.ceil, "floor": math.floor}
    return discretizer[method]((value - start) / step) * step + start


def counter(stop: int = None) -> Generator[int, None, None]:
    """Generate integers from 0 to ``stop``.

    .. warning::

        Do not ``list`` the result, unless stop value is explicitly set. ``list``-ing
        infinite generator will cause memory leak.

    Parameters
    ----------
    stop
        Number of yielded values.

    Examples
    --------
    >>> list(counter(5))
    [0, 1, 2, 3, 4]
    >>> list(counter())
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...]  # -> memory leak

    """
    if stop is None:
        yield from itertools.count()
    elif stop < 0:
        raise ValueError("Stop value should be non-negative.")
    else:
        yield from range(stop)
