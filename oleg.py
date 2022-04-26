from typing import Any, Dict, Iterator


class Context:
    def __init__(self, name=None):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # doing something here
        print("Name is set")
        self._name = value

    def __iter__(self) -> Iterator[Any]:
        yield self._name

    @property
    def _(self) -> Dict[str, Any]:
        return {
            'name': self.name
        }


class ExtraContext:
    def __init__(self, lang=None):
        self._lang = lang

    @property
    def lang(self):
        return self._lang

    def __iter__(self) -> Iterator[Any]:
        yield self._lang

    @property
    def _(self) -> Dict[str, Any]:
        return {
            'lang': self.lang
        }


def foo_with_args(name, lang="RU"):
    return name + " " + lang


def main():
    c = Context()
    c.name = "Some name"

    e = ExtraContext(lang="EN")
    # e.lang = "EN" # impossible

    # possible call because of iter
    print(foo_with_args(*c, *e))
    # combining
    print(foo_with_args(**c._, **e._))
    print(foo_with_args(**e._, **c._))
    print(foo_with_args(**c._))


if __name__ == "__main__":
    main()
