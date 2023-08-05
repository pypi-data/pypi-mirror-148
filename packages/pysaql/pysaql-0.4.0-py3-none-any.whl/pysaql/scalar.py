"""Contains definition of a scalar"""

from __future__ import annotations

from abc import ABC, abstractmethod
import operator
from typing import Any, Callable, Optional, Sequence, Union

from .expression import Expression
from .util import escape_identifier, stringify

# Mapping from operator function to its string representation in SAQL
OPERATOR_STRINGS = {
    operator.add: "+",
    operator.and_: "&&",
    operator.contains: "in",
    operator.eq: "==",
    operator.ge: ">=",
    operator.gt: ">",
    operator.inv: "!",
    operator.is_: "is",
    operator.is_not: "is not",
    operator.le: "<=",
    operator.lt: "<",
    operator.mod: "%",
    operator.mul: "*",
    operator.ne: "!=",
    operator.neg: "-",
    operator.or_: "||",
    operator.sub: "-",
    operator.truediv: "/",
}


class Operation:
    """Base operation class

    This establishes inheritance but does not currently implement any functionality.
    """

    pass


class BooleanOperation(Operation):
    """Mixin that defines boolean comparison methods"""

    def __and__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `and` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.and_, self, obj)

    def __or__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `or` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.or_, self, obj, wrap=True)

    def __invert__(self) -> UnaryOperation:
        """Creates a unary operation using the `inv` operator

        Returns:
            unary operation

        """
        return UnaryOperation(operator.inv, self)


class BinaryOperation(BooleanOperation):
    """Represents a binary operation"""

    def __init__(self, op: Callable, left: Any, right: Any, wrap: bool = False) -> None:
        """Initializer

        Args:
            op: Operator function that accepts two operands
            left: Left operand
            right: Right operand
            wrap: Flag that indicates whether the stringified operation should be
                wrapped in parentheses to denote precedence. Defaults to False.

        """
        super().__init__()
        if op not in OPERATOR_STRINGS:
            operators = ", ".join(f"operator.{fn.__name__}" for fn in OPERATOR_STRINGS)
            raise ValueError(f"Operator must be one of: {operators}. Provided: {op}")
        self.op = op
        self.left = left
        self.right = right
        self.wrap = wrap

    def __str__(self) -> str:
        """Cast the binary operation to a string"""
        s = f"{stringify(self.left)} {OPERATOR_STRINGS[self.op]} {stringify(self.right)}"
        if self.wrap:
            s = f"({s})"

        return s


class UnaryOperation(BooleanOperation):
    """Represents a unary operation"""

    def __init__(self, op: Callable, value: Any) -> None:
        """Initializer

        Args:
            op: Operator function that accepts one argument
            value: Value to pass to the operator

        """
        super().__init__()
        self.op = op
        self.value = value

    def __str__(self) -> str:
        """Cast the unary operation to a string"""
        return f"{OPERATOR_STRINGS[self.op]} {stringify(self.value)}"


class Scalar(Expression, BooleanOperation, ABC):
    """Represents a scalar expression"""

    _alias: Optional[str] = None

    def alias(self, name: str) -> Scalar:
        """Set the alias name for a scalar expression

        Args:
            name: Alias name

        Returns:
            self

        """
        self._alias = name
        return self

    @abstractmethod
    def to_string(self) -> str:
        """Cast the scalar to a string"""
        pass

    def __str__(self) -> str:
        """Cast the scalar to a string, including the alias if set

        Returns:
            string

        """
        s = self.to_string()
        if self._alias:
            s += f" as {escape_identifier(self._alias)}"

        return s

    def __eq__(self, obj: Any) -> BinaryOperation:  # type: ignore[override]
        """Creates a binary operation using the `eq` or `is` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        op = operator.is_ if obj is None else operator.eq
        return BinaryOperation(op, self, obj)

    def __ne__(self, obj: Any) -> BinaryOperation:  # type: ignore[override]
        """Creates a binary operation using the `ne` or `is_not` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        op = operator.is_not if obj is None else operator.ne
        return BinaryOperation(op, self, obj)

    def __lt__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `lt` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.lt, self, obj)

    def __le__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `le` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.le, self, obj)

    def __gt__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `gt` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.gt, self, obj)

    def __ge__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `ge` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.ge, self, obj)

    def __add__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `add` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.add, self, obj)

    def __sub__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `sub` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.sub, self, obj)

    def __mul__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `mul` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.mul, self, obj)

    def __truediv__(self, obj: Any) -> BinaryOperation:
        """Creates a binary operation using the `truediv` operator

        Args:
            obj: Object to use for the right operand

        Returns:
            binary operation

        """
        return BinaryOperation(operator.truediv, self, obj)

    def __neg__(self) -> UnaryOperation:
        """Creates a unary operation using the `neg` operator

        Returns:
            unary operation

        """
        return UnaryOperation(operator.neg, self)

    def in_(self, iterable: Union[Sequence, Expression]) -> BinaryOperation:
        """Creates a binary operation using the `contains` operator

        Args:
            iterable: Iterable that may contain the current scalar

        Returns:
            binary operation

        """
        return BinaryOperation(operator.contains, self, iterable)


class field(Scalar):
    """Represents a field (column) in the data stream"""

    name: str

    def __init__(self, name: str) -> None:
        """Initializer

        Args:
            name: Name of the field

        """
        super().__init__()
        self.name = name

    def to_string(self) -> str:
        """Cast the field to a string"""
        return escape_identifier(self.name)
