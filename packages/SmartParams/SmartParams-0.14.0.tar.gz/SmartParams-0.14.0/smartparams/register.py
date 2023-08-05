import inspect
import warnings
from typing import Callable, Dict, Mapping, Sequence, Union

import smartparams.utils.string as strutil
import smartparams.utils.typing as typeutil


class SmartRegister:
    def __init__(self) -> None:
        self._aliases: Dict[str, str] = dict()
        self._origins: Dict[str, str] = dict()

    @property
    def aliases(self) -> Dict[str, str]:
        return self._aliases.copy()

    @property
    def origins(self) -> Dict[str, str]:
        return self._origins.copy()

    def __call__(
        self,
        classes: Union[
            Sequence[Union[str, Callable]],
            Mapping[str, str],
            Mapping[Callable, str],
            Mapping[Union[str, Callable], str],
        ],
        prefix: str = '',
        strict: bool = False,
    ) -> None:
        if isinstance(classes, Sequence):
            self._register_classes(
                classes=classes,
                prefix=prefix,
                strict=strict,
            )
        elif isinstance(classes, Mapping):
            self._register_aliases(
                aliases=classes,
                prefix=prefix,
                strict=strict,
            )
        else:
            raise TypeError(f"Register classes type '{type(classes)}' is not supported.")

    def reset(self) -> None:
        self._aliases.clear()
        self._origins.clear()

    def _register_classes(
        self,
        classes: Sequence[Union[str, Callable]],
        prefix: str = '',
        strict: bool = False,
    ) -> None:
        self._register_aliases(
            aliases={c: c if isinstance(c, str) else typeutil.get_name(c) for c in classes},
            prefix=prefix,
            strict=strict,
        )

    def _register_aliases(
        self,
        aliases: Union[
            Mapping[str, str],
            Mapping[Callable, str],
            Mapping[Union[str, Callable], str],
        ],
        prefix: str = '',
        strict: bool = False,
    ) -> None:
        for origin, alias in aliases.items():
            origin = origin if isinstance(origin, str) else inspect.formatannotation(origin)
            alias = strutil.join_keys(prefix, alias)

            if origin in self._aliases:
                message = f"Origin '{origin}' has been overridden."
                if strict:
                    raise ValueError(message)
                warnings.warn(message)
                self._origins.pop(self._aliases.pop(origin))

            if alias in self._origins:
                message = f"Alias '{alias}' has been overridden."
                if strict:
                    raise ValueError(message)
                warnings.warn(message)
                self._aliases.pop(self._origins.pop(alias))

            self._aliases[origin] = alias
            self._origins[alias] = origin
