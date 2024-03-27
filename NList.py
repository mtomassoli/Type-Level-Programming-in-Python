from __future__ import annotations
from typing import Callable, overload, Literal, TypeVar, Generic

# import write_ops as _           # creates the opsN.py files
from misc import Digit, PosDigit, L0, L1
from ops1 import adc1, sbb1
from ops2 import adc2, sbb2
from ops3 import adc3, sbb3
from ops4 import adc4, sbb4

type EmptyNList = NList[L0, L0, L0, L0]
type NonEmptyNList = (NList[PosDigit, Digit, Digit, Digit] |
                      NList[Digit, PosDigit, Digit, Digit] |
                      NList[Digit, Digit, PosDigit, Digit] |
                      NList[Digit, Digit, Digit, PosDigit])

N1 = TypeVar('N1', bound=Digit, covariant=True)
N2 = TypeVar('N2', bound=Digit, covariant=True)
N3 = TypeVar('N3', bound=Digit, covariant=True)
N4 = TypeVar('N4', bound=Digit, covariant=True)

@overload
def or_none[T](x: T, ret_none: L0) -> T: ...
@overload
def or_none[T](x, ret_none: L1) -> None: ...
def or_none[T](x: T, ret_none) -> T | None: ...

# NOTE: It's important that `NList` be covariant in its length-related typevars
#   or we will NOT be able to use `NonEmptyNList`. That requires the use of
#   `TypeVar`.
#   This could be avoided by using a single type var for the length:
#       class NList[LEN: tuple[Digit, Digit, Digit, Digit]]: ...
#   Then defining `ZeroLen` and `PosLen` for tuples would work because tuples
#   are covariant in their type vars.
class NList(Generic[N4, N3, N2, N1]):
    """Fixed-length list of length N4 N3 N2 N1, read as a 4-digit number."""
    def __init__(self, length: tuple[N4, N3, N2, N1]) -> None:
        pass

    # NOTE: This CANNOT be a @property, although it would make sense...
    @overload
    def is_empty(self: EmptyNList) -> Literal[True]: ...
    @overload
    # NOTE: We could use `self: NList` and ignore the overlap with the previous
    #   overload, but this is cleaner. Also note that this trick won't work
    #   with the method `last_val` below.
    def is_empty(self: NonEmptyNList) -> Literal[False]: ...
    def is_empty(self) -> bool: ...

    @property    
    def last_val(self: NonEmptyNList) -> int: ...      # `int` is not important

    # NOTE: `__add__` is ONY called when the addends are the same type, and
    #   `__radd__` when `__add__` CANNOT be called.
    #   This means that `__add__` will be called for nlists of same length, and
    #   `__radd__` for nlists of different lengths.
    # NOTE: we CANNOT implement this as a non-method function because:
    #   * here, in a class, N4, N3, N2, and N1 are fixed
    #   * in a normal 2-arg function, type inference will always find a common
    #     union-type for the 2 args, even if they're different, so there's NO
    #     way (AFAICT) to exclude different-length nlists.
    def __add__(self, right_nl: NList[N4, N3, N2, N1]) -> NList[N4, N3, N2, N1]:
        """point-wise addition"""
        ...

    def __radd__(self, left_nl: NList[N4, N3, N2, N1]) -> NList[N4, N3, N2, N1]:
        """point-wise addition"""
        ...
    
    def concat[X1: Digit, X2: Digit, X3: Digit, X4: Digit,
               Y1: Digit, Y2: Digit, Y3: Digit, Y4: Digit,
               Z1: Digit, Z2: Digit, Z3: Digit, Z4: Digit,
               C1: Digit, C2: Digit, C3: Digit
    ](
        # NOTE: Using N4, N3, N2, and N1 directly doesn't work, so we type-hint
        #   `self` itself!
        #   BUG in Pyright?
        self: NList[X4, X3, X2, X1],
        nlist2: NList[Y4, Y3, Y2, Y1], *,
        # NOTE: No, we CANNOT use the same `adc` (add with carry) because
        #   otherwise its generic types will be bound once and reused for all
        #   its instances, which is NOT what we want here.
        #   BUG in Pyright?
        # NOTE: The trick with the default argument (`= adc1`) does NOT work
        #   recursively, that is, we CANNOT use `concat` itself as a default
        #   arg in another function. The problem is that Pyright gives up and
        #   doesn't resolve it.
        _adc_digit1: Callable[[X1, Y1, L0], tuple[Z1, C1]] = adc1,
        _adc_digit2: Callable[[X2, Y2, C1], tuple[Z2, C2]] = adc2,
        _adc_digit3: Callable[[X3, Y3, C2], tuple[Z3, C3]] = adc3,
        _adc_digit4: Callable[[X4, Y4, C3], tuple[Z4, L0]] = adc4,
        # and so on... but gets slooow and buggy (in VSCode, at least) :(
    ) -> NList[Z4, Z3, Z2, Z1]:
        """Concatenates 2 nlists of the same length."""
        ...
    
    def get[X1: Digit, X2: Digit, X3: Digit, X4: Digit,
            Y1: Digit, Y2: Digit, Y3: Digit, Y4: Digit,
            Z1: Digit, Z2: Digit, Z3: Digit, Z4: Digit,
            B1: Digit, B2: Digit, B3: Digit, B4: Digit,
            R,
    ](
        self: NList[X4, X3, X2, X1],
        idx: tuple[Y4, Y3, Y2, Y1], *,
        _sbb_digit1: Callable[[X1, Y1, L1], tuple[Z1, B1]] = sbb1,
        _sbb_digit2: Callable[[X2, Y2, B1], tuple[Z2, B2]] = sbb2,
        _sbb_digit3: Callable[[X3, Y3, B2], tuple[Z3, B3]] = sbb3,
        _sbb_digit4: Callable[[X4, Y4, B3], tuple[Z4, B4]] = sbb4,
        _op: Callable[[int, B4], R] = or_none
    ) -> R:
        """Returns the int at the given index or `None` if the idx is out of
        bounds."""
        ...

# NOTE: `num` CANNOT be explicitly typed: the trick is to let Pyright infer the
#   types, so that `num` takes an int literal and returns its digits as a tuple
#   of int literals.
#   Do you want to put it inside `NList`? Good luck.
#   Do you want to do ALL the computations this way? Yeah, (py)right...
#   (py intended)
def num(x):
    return ((x // 1000) % 10, (x // 100) % 10, (x // 10) % 10, x % 10)
