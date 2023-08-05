from decimal import Decimal
from typing import Any

from django.db import models

from djangodollar.dollar import Dollar


class DollarField(models.DecimalField):
    """A custom field for representing dollar amounts."""

    def __init__(self, *args, **kwargs):
        """Set decimal places to 2."""
        kwargs["decimal_places"] = 2
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection) -> Dollar | None:
        """Convert from DB value to Dollar."""
        if value is None:
            return value
        return Dollar(value)

    def to_python(self, value: Any) -> Decimal | None:
        """Round value to correct dollar amount."""
        if isinstance(value, Dollar):
            return value.val
        value = super().to_python(value)
        if value is None:
            return value
        return Dollar(value).val

    def value_from_object(self, obj: models.Model) -> Decimal | None:
        """Return value as a Decimal."""
        value = super().value_from_object(obj)
        if isinstance(value, Dollar):
            return abs(value.val)
        return None

    def get_default(self) -> Any:
        """Return decimal if default is a dollar."""
        if self.has_default() and isinstance(self.default, Dollar):
            return lambda: self.default.val
        return super().get_default()

    def deconstruct(self) -> tuple[str, str, list[Any], dict[str, Any]]:
        """Deconstruct DollarField."""
        name, path, args, kwargs = super().deconstruct()
        del kwargs["decimal_places"]
        return name, path, args, kwargs
