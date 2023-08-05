from decimal import Decimal, DecimalTuple, InvalidOperation
from math import ceil, floor, trunc
from typing import Any, Optional, SupportsRound, Union, overload


Dollarable = Union[float, Decimal, "Dollar"]


class Dollar(SupportsRound):
    """A class for representing dollar values.

    We use the delta attribute to ensure that we're not spuriously rounding
    up remainders from float inaccuracy.
    """

    _val: Decimal
    delta: Decimal = Decimal("0.0000001")

    def __init__(self, val: str | Dollarable) -> None:
        """Initialize by setting internal value."""
        if isinstance(val, Dollar):
            self._val = val.val
        else:
            self._val = self.round_currency(Decimal(val))

    @property
    def val(self) -> Decimal:
        """Return dollar value."""
        if isinstance(self._val, Decimal):
            return self._val
        raise ValueError("Internal value must be a Decimal.")

    def round_currency(self, val: Decimal) -> Decimal:
        """Round val up to the nearest dollar amount."""
        rounded = Decimal(round(val, 2))
        if (val - rounded) > self.delta:
            return Decimal(rounded + Decimal("0.01"))
        return Decimal(rounded).quantize(Decimal("0.00"))

    def __add__(self, other: Dollarable) -> "Dollar":
        """Add values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(self.val + Decimal(other))
        return Dollar(self.val + other.val)

    def __radd__(self, other: Dollarable) -> "Dollar":
        """Add values and convert to Dollar."""
        return self + other

    def __sub__(self, other: Dollarable) -> "Dollar":
        """Subtract values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(self.val - Decimal(other))
        return Dollar(self.val - other.val)

    def __rsub__(self, other: Dollarable) -> "Dollar":
        """Subtract values and convert to Dollar."""
        return -1 * (self - other)

    def __mul__(self, other: Dollarable) -> "Dollar":
        """Multiply values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(self.val * Decimal(other))
        return Dollar(self.val * other.val)

    def __rmul__(self, other: Dollarable) -> "Dollar":
        """Multiply values and convert to Dollar."""
        return self * other

    def __truediv__(self, other: Dollarable) -> "Dollar":
        """Divide values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(self.val / Decimal(other))
        return Dollar(self.val / other.val)

    def __rtruediv__(self, other: Dollarable) -> "Dollar":
        """Divide values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(Decimal(other) / self.val)
        return Dollar(other.val / self.val)

    def __floordiv__(self, other: Dollarable) -> "Dollar":
        """Floor divide values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(self.val // Decimal(other))
        return Dollar(self.val // other.val)

    def __rfloordiv__(self, other: Dollarable) -> "Dollar":
        """Floor divide values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(Decimal(other) // self.val)
        return Dollar(other.val // self.val)

    def __mod__(self, other: Dollarable) -> "Dollar":
        """Modulo values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(self.val % Decimal(other))
        return Dollar(self.val % other.val)

    def __rmod__(self, other: Dollarable) -> "Dollar":
        """Modulo values and convert to Dollar."""
        if not isinstance(other, Dollar):
            return Dollar(Decimal(other) % self.val)
        return Dollar(other.val % self.val)

    def __divmod__(
        self, other: Dollarable
    ) -> tuple[Union["Dollar", int], Union["Dollar", Any]]:
        """Return quotient and remainder."""
        return self // other, self % other

    def __rdivmod__(
        self, other: Dollarable
    ) -> tuple[Union["Dollar", int], Union["Dollar", Any]]:
        """Return quotient and remainder."""
        return other // self, other % self

    def __pow__(
        self, other: Dollarable, modulo: Optional[int] = None
    ) -> "Dollar":
        """Return exponent."""
        if modulo is not None:
            return NotImplemented
        if not isinstance(other, Dollar):
            return Dollar(self.val ** Decimal(other))
        return Dollar(self.val**other.val)

    def __rpow__(
        self, other: Dollarable, modulo: Optional[int] = None
    ) -> "Dollar":
        """Return exponent."""
        if modulo is not None:
            return NotImplemented
        if not isinstance(other, Dollar):
            return Dollar(Decimal(other) ** self.val)
        return Dollar(other.val**self.val)

    def __eq__(self, other: Any) -> bool:
        """Compare if dollar values are equal."""
        if not isinstance(other, Dollar):
            try:
                return self == Dollar(other)
            except (InvalidOperation, TypeError):
                return False
        return self.val == other.val

    def __ne__(self, other: Any) -> bool:
        """Compare if dollar values are not equal."""
        return not (self == other)

    def __lt__(self, other: Dollarable) -> bool:
        """Compare if dollar values are less than."""
        if not isinstance(other, Dollar):
            return self < Dollar(other)
        return self.val < other.val

    def __le__(self, other: Dollarable) -> bool:
        """Compare if dollar values are less than or equal to."""
        return (self < other) or (self == other)

    def __gt__(self, other: Dollarable) -> bool:
        """Compare if dollar value is greater than."""
        if not isinstance(other, Dollar):
            return self > Dollar(other)
        return self.val > other.val

    def __ge__(self, other: Dollarable) -> bool:
        """Compare if dollar value is greater than or equal to."""
        if not isinstance(other, Dollar):
            return self >= Dollar(other)
        return self.val >= other.val

    def __neg__(self) -> "Dollar":
        """Return negative self."""
        return -1 * self

    def __pos__(self) -> "Dollar":
        """Return positive self."""
        return self

    def __abs__(self) -> "Dollar":
        """Return absolute value of self."""
        return Dollar(abs(self.val))

    def __int__(self) -> int:
        """Return self as integer."""
        return int(self.val)

    def __float__(self) -> float:
        """Return self as float."""
        return float(self.val)

    def __bool__(self) -> bool:
        """Return self as a boolean value."""
        return bool(self.val)

    @overload
    def __round__(self) -> int:
        """Round to nearest integer."""
        ...

    @overload
    def __round__(self, ndigits: int) -> "Dollar":
        """Round to nearest Dollar with ndigits of precision."""
        ...

    def __round__(self, ndigits: Optional[int] = None) -> Union["Dollar", int]:
        """Round self to nearest power of ten."""
        if ndigits is None:
            return round(self.val)
        return Dollar(round(self.val, ndigits))

    def __trunc__(self) -> "Dollar":
        """Truncate self."""
        return Dollar(trunc(self.val))

    def __floor__(self) -> "Dollar":
        """Round down to nearest whole number."""
        return Dollar(floor(self.val))

    def __ceil__(self) -> "Dollar":
        """Round up to nearest whole numer."""
        return Dollar(ceil(self.val))

    def __str__(self) -> str:
        """Return string representation of dollar amount."""
        return f"${self.val}"

    def __repr__(self) -> str:
        """Return internal representation of class."""
        return f"<Dollar: {self}>"

    def as_tuple(self) -> DecimalTuple:
        """Return DecimalTuple (for validation)."""
        return self.val.as_tuple()
