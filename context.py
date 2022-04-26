from dataclasses import dataclass, fields
from typing import Optional

from cute import cute, custom_getters_and_setters, getter


def oleg(cls):
    dcls = cls
    dcls = dataclass(cls)
    return custom_getters_and_setters(cute(dcls))


@oleg
class Spec:
    lang: Optional[str] = None

    def specify(self, language: str):
        self.lang = language
        print(f"Specified spec with language: {language}")


@oleg
class Context:
    original_spec: Spec = Spec()
    lang: Optional[str] = None

    # should be named exactly like original field, but with _ at
    # the beginning
    @getter
    def _lang(self):
        # be careful, if you want to use or set original value you must use
        # reference prefixed with _ otherwise it won't work:
        return self._lang

    @_lang.setter
    def _lang(self, value):
        # be careful, if you want to use or set original value you must use
        # reference prefixed with _ otherwise it won't work:self.original_spec.specify(value)
        self._lang = value


@oleg
class ExtraContext:
    extra: bool = False

    @getter
    def _extra(self):
        print("Always returning True from extra context")
        return True


def test_func(original_spec, lang, extra=False):
    print(original_spec, lang)


def main():
    cont = Context()
    cont.lang = "EN"
    test_func(*cont)
    extra = ExtraContext()
    test_func(**extra._, **cont._)


if __name__ == "__main__":
    main()
