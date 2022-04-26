from collections.abc import Mapping

from dataclasses import dataclass
from dataclasses import fields, is_dataclass


def cute(cls):
    """
    Decorator for supporting iteration over values of dataclass.
    See examples in main.
    """
    if not is_dataclass(cls):
        raise TypeError(f"Passed class is not dataclass but: {cls}")

    def names(dcls_or_obj):
        return (field_.name for field_ in fields(dcls_or_obj))

    def __iter__(self):
        return (getattr(self, name) for name in names(cls))

    # whoohoo
    class _:
        def __get__(self, inst=None, owner=None):
            if inst is None:
                raise AttributeError
            return dict(zip(names(inst), inst))

    cls.__iter__ = __iter__
    cls._ = _()
    return cls


def custom_getters_and_setters(cls):
    """
    Special decorator to have property deco applied to dataclass fields.

    Otherwise it would be needed to declare classes like that:
    >>> @dataclass
    >>> class Test:
    >>>     name: str = 'foo'

    >>>     @property
    >>>     def _name(self):
    >>>         print("on get")
    >>>         return self._my_str_rev[::-1]

    >>>     @_name.setter
    >>>     def _name(self, value):
    >>>         print("on set: ", value)
    >>>         self._my_str_rev = value[::-1]


    >>> # --- has to be called at module level ---
    >>> Test.name = Test._name

    See https://stackoverflow.com/a/61480946 for more information.
    """
    def __init__(self, *args, **kwargs):
        cls_annotations = getattr(cls, '__annotations__', {})
        for name, type in cls_annotations.items():
            hidden_attr_name = f"_{field_.name}"
            candidate = getattr(self, hidden_attr_name, None)
            if candidate is not None:
                setattr(self, hidden_attr_name, getattr(cls, field_.name, None))
                setattr(self, field_.name, candidate.prop)

    setattr(cls, "__init__", __init__)

    return cls


def getter(meth):
    class Internal:
        def __init__(self, prop):
            self.prop = prop
        def setter(self, fset):
            return Internal(self.prop.setter(fset))
        def deleter(self, fdel):
            return Internal(self.prop.deleter(fdel))

    return Internal(property(meth))


@cute
@dataclass
class A:
    a: int
    b: int


@cute
@dataclass
class B:
    c: int


@cute
@custom_getters_and_setters
@dataclass
class C:
    f: str

    @getter
    def _f(self):
        return "always_prefixed :> " + self._f

    @_f.setter
    def _f(self, value):
        self._f = value


def foo(a, b, c):
    return a + b + c


def main():
    a = A(1, 2)
    b = B(3)
    print(foo(*a, *b))
    print(foo(**b._, **a._))

    a_, b_, c_ = *a, *b
    print(a_, b_, c_)

    c = C("AAAA")
    c, *_ = c
    print(c)


if __name__ == "__main__":
    main()

