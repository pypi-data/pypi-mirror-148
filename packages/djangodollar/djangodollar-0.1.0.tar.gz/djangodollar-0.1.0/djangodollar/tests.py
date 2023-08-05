from decimal import Decimal
from math import ceil, floor, trunc

from django.test import TestCase

from djangodollar import Dollar


class TestDollar(TestCase):
    """Test Dollar arithmetic."""

    int_dollar = Dollar(10)
    float_dollar = Dollar(1.52562153263)
    decimal_dollar = Dollar(Decimal("3.1415926"))

    def test_dollar_val(self) -> None:
        """Test that internal value is properly rounded."""
        self.assertEqual(Decimal("10.00"), self.int_dollar.val)
        self.assertEqual(Decimal("1.53"), self.float_dollar.val)
        self.assertEqual(Decimal("3.15"), self.decimal_dollar.val)

    def test_dollar_add(self) -> None:
        """Test that we can add dollars."""
        self.assertEqual(
            Dollar(11.53), self.int_dollar + self.float_dollar
        )
        self.assertEqual(Dollar(4.15), self.decimal_dollar + 1.0)
        self.assertEqual(Dollar(4.15), 1.0 + self.decimal_dollar)

    def test_dollar_sub(self) -> None:
        """Test that we can subtract dollars."""
        self.assertEqual(
            Dollar(8.47), self.int_dollar - self.float_dollar
        )
        self.assertEqual(Dollar(2.15), self.decimal_dollar - 1)
        self.assertEqual(Dollar(0.00), 10 - self.int_dollar)

    def test_dollar_mul(self) -> None:
        """Test that we can multiply dollars."""
        self.assertEqual(
            Dollar(31.50), self.int_dollar * self.decimal_dollar
        )
        self.assertEqual(Dollar(0.77), 0.5 * self.float_dollar)

    def test_dollar_true_div(self) -> None:
        """Test that we can divide dollars."""
        self.assertEqual(Dollar(5.00), self.int_dollar / 2)
        self.assertEqual(Dollar(1.00), 3.15 / self.decimal_dollar)

    def test_dollar_floor_div(self) -> None:
        """Test dollar floor division."""
        self.assertEqual(Dollar(5.00), self.int_dollar // 1.8)
        self.assertEqual(Dollar(2), 4 // self.float_dollar)

    def test_dollar_mod(self) -> None:
        """Test modulo for dollars."""
        self.assertEqual(Dollar(0), self.int_dollar % 2)
        self.assertEqual(Dollar(3), 13 % self.int_dollar)

    def test_dollar_divmod(self) -> None:
        """Test divmod for dollars."""
        self.assertEqual((Dollar(5), Dollar(1)), divmod(self.int_dollar, 1.8))
        self.assertEqual((Dollar(1), Dollar(3)), divmod(13, self.int_dollar))

    def test_dollar_exp(self) -> None:
        """Test that we can raise dollars to powers and vice versa."""
        self.assertEqual(Dollar(10.00), self.int_dollar**1)
        self.assertEqual(Dollar(8.88), 2**self.decimal_dollar)

    def test_dollar_gt(self) -> None:
        """Test that a dollar is greater than a value."""
        self.assertGreater(self.int_dollar, 9)
        self.assertGreater(11, self.float_dollar)
        self.assertGreater(self.decimal_dollar, self.float_dollar)

    def test_dollar_lt(self) -> None:
        """Test that a dollar is less than a value."""
        self.assertLess(self.int_dollar, 11)
        self.assertLess(2, self.decimal_dollar)
        self.assertLess(self.float_dollar, self.decimal_dollar)

    def test_dollar_gte(self) -> None:
        """Test that a dollar is greater than or equal to a value."""
        self.assertGreaterEqual(self.int_dollar, 10)
        self.assertGreaterEqual(self.decimal_dollar, 0)
        self.assertGreaterEqual(0, -1 * self.float_dollar)

    def test_dollar_lte(self) -> None:
        """Test that a dollar is less than or equal to a value."""
        self.assertLessEqual(10, self.int_dollar)
        self.assertLessEqual(0, self.decimal_dollar)
        self.assertLessEqual(-1 * self.float_dollar, 12)

    def test_dollar_eq(self) -> None:
        """Test that a dollar is equal to a value."""
        self.assertEqual(10, self.int_dollar)
        self.assertEqual(1.53, self.float_dollar)
        self.assertEqual(Dollar(3.15), self.decimal_dollar)

    def test_dollar_ne(self) -> None:
        """Test that a dollar is NOT equal to a value."""
        self.assertNotEqual(9, self.int_dollar)
        self.assertNotEqual(None, self.float_dollar)
        self.assertNotEqual("foo", self.decimal_dollar)
        self.assertNotEqual(Dollar(9), self.int_dollar)

    def test_dollar_neg(self) -> None:
        """Test that we can negate dollar amounts."""
        self.assertEqual(Dollar(-10), -self.int_dollar)
        self.assertEqual(Dollar(-1.53), -self.float_dollar)
        self.assertEqual(Dollar(-3.15), -self.decimal_dollar)

    def test_dollar_pos(self) -> None:
        """Test that we can use the positive unary operator with dollars."""
        self.assertEqual(Dollar(10), +self.int_dollar)
        self.assertEqual(Dollar(1.53), +self.float_dollar)
        self.assertEqual(Dollar(3.15), +self.decimal_dollar)

    def test_dollar_abs(self) -> None:
        """Test that we can find the absolute value of a dollar amount."""
        self.assertEqual(Dollar(10), abs(-self.int_dollar))
        self.assertEqual(Dollar(1.53), abs(self.float_dollar))

    def test_dollar_int(self) -> None:
        """Test converting dollars to integers."""
        self.assertEqual(10, int(self.int_dollar))
        self.assertEqual(1, int(self.float_dollar))
        self.assertEqual(3, int(self.decimal_dollar))

    def test_dollar_float(self) -> None:
        """Test converting dollars to floats."""
        self.assertEqual(10.0, float(self.int_dollar))
        self.assertEqual(1.53, float(self.float_dollar))
        self.assertEqual(3.15, float(self.decimal_dollar))

    def test_dollar_bool(self) -> None:
        """Test converting dollars to booleans."""
        self.assertTrue(bool(Dollar(10)))
        self.assertFalse(bool(Dollar(0)))

    def test_dollar_round(self) -> None:
        """Test rounding dollars."""
        self.assertEqual(10, round(self.int_dollar))
        self.assertEqual(2, round(self.float_dollar))
        self.assertEqual(3, round(self.decimal_dollar))
        self.assertEqual(Dollar(10), round(self.int_dollar, 0))
        self.assertEqual(Dollar(2), round(self.float_dollar, 0))
        self.assertEqual(Dollar(3.2), round(self.decimal_dollar, 1))

    def test_dollar_trunc(self) -> None:
        """Test truncating dollars."""
        self.assertEqual(Dollar(10), trunc(self.int_dollar))
        self.assertEqual(Dollar(1), trunc(self.float_dollar))
        self.assertEqual(Dollar(3), trunc(self.decimal_dollar))

    def test_dollar_floor(self) -> None:
        """Test floor for dollars."""
        self.assertEqual(Dollar(10), floor(self.int_dollar))
        self.assertEqual(Dollar(1), floor(self.float_dollar))
        self.assertEqual(Dollar(3), floor(self.decimal_dollar))

    def test_dollar_ceiling(self) -> None:
        """Test ceiling for dollars."""
        self.assertEqual(Dollar(10), ceil(self.int_dollar))
        self.assertEqual(Dollar(2), ceil(self.float_dollar))
        self.assertEqual(Dollar(4), ceil(self.decimal_dollar))

    def test_dollar_str(self) -> None:
        """Test strings for dollars."""
        self.assertEqual("$10.00", str(self.int_dollar))
        self.assertEqual("$1.53", str(self.float_dollar))
        self.assertEqual("$3.15", str(self.decimal_dollar))

    def test_dollar_repr(self) -> None:
        """Test repr strings for dollars."""
        self.assertEqual("<Dollar: $10.00>", repr(self.int_dollar))
        self.assertEqual("<Dollar: $1.53>", repr(self.float_dollar))
        self.assertEqual("<Dollar: $3.15>", repr(self.decimal_dollar))

    def test_dollar_tuple(self) -> None:
        """Test decimal tuples for dollars."""
        self.assertEqual(Decimal("10.00").as_tuple(), self.int_dollar.as_tuple())
        self.assertEqual(Decimal("1.53").as_tuple(), self.float_dollar.as_tuple())
        self.assertEqual(Decimal("3.15").as_tuple(), self.decimal_dollar.as_tuple())
