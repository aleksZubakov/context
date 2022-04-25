from collections.abc import Mapping

from dataclasses import dataclass
from dataclasses import fields, is_dataclass


def cute(cls):
    if not is_dataclass(cls):
        raise TypeError(f"Passed class is not dataclass but: {cls}")

    def names(dcls_or_obj):
        return (field_.name for field_ in fields(dcls_or_obj))

    def __iter__(self):
        return (getattr(self, name) for name in names(cls))

    class _:
        def __get__(self, inst=None, owner=None):
            if inst is None:
                raise AttributeError
            return dict(zip(names(inst), inst))

    cls.__iter__ = __iter__
    cls._ = _()
    return cls


@cute
@dataclass
class A:
    a: int
    b: int


@cute
@dataclass
class B:
    c: int


def foo(a, b, c):
    return a + b + c


def main():
    a = A(1, 2)
    b = B(3)
    print(foo(*a, *b))
    print(foo(**b._, **a._))

    a_, b_, c_ = *a, *b
    print(a_, b_, c_)


if __name__ == "__main__":
    main()

