import inspect
import os
import re
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

import smartparams.utils.dictionary as dictutil
import smartparams.utils.string as strutil
import smartparams.utils.typing as typeutil
from smartparams.exceptions import (
    ConfigurationError,
    DummyError,
    MissingPath,
    ObjectInvalidOptionError,
    ObjectNotRegistered,
    UnexpectedTypeOptionArguments,
)
from smartparams.lab import SmartLab
from smartparams.register import SmartRegister
from smartparams.utils.cli import (
    Arguments,
    Print,
    create_argument_parser,
    parse_arguments,
)
from smartparams.utils.enums import Option
from smartparams.utils.io import load_data, print_data, save_data

T = TypeVar('T')


class Smart(Generic[T]):
    """Creates a partial wrapper for a class that can be configurable from a file or a cli.

    Smart class has functionality of both partial and dict classes. It allows creating
    objects with lazy instantiating. This makes possible injecting values from config
    file or command line.

    Examples:
        # script.py
        from dataclasses import dataclass
        from pathlib import Path

        from smartparams import Smart


        @dataclass
        class Params:
            value: str


        def main(smart: Smart[Params]) -> None:
            params = smart()
            # do some stuff ...


        if __name__ == '__main__':
            Smart.strict = True
            Smart(Params).run(
                function=main,
                path=Path('params.yaml'),
            )

        #  Run in command line:
        #    $ python script.py value="Some value"
        #    $ python script.py --dump
        #    $ python script.py
        #    $ python script.py --print keys
        #    $ python script.py --help


    Attributes:
        keyword: Name of the key containing the value with the path of the class to be imported.
            Can be set by env variable SMARTPARAMS_KEYWORD, default 'class'.
        missing_value: Value assigned to unknown types when creating a representation.
            Can be set by env variable SMARTPARAMS_MISSING_VALUE, default '???'.
        check_missings: Whether to check missing values before instantiating object.
            Can be set by env variable SMARTPARAMS_CHECK_MISSINGS, default 'yes'.
        check_typings: Whether to check arguments type before instantiating object.
            Can be set by env variable SMARTPARAMS_CHECK_TYPINGS, default 'yes'.
        check_overrides: Whether to check override arguments before instantiating object.
            Can be set by env variable SMARTPARAMS_CHECK_OVERRIDES, default 'yes'.
        allow_only_registered_classes: Whether to allow import only registered classes.
            Can be set by env variable SMARTPARAMS_ALLOW_ONLY_REGISTERED_CLASSES, default 'no'.
        strict: Whether to raise exceptions instead of warnings.
            Can be set by env variable SMARTPARAMS_STRICT, default 'no'.
        debug: Whether to print exception stack trace instead of cli error message.
            Can be set by env variable SMARTPARAMS_DEBUG, default 'no'.

    """

    keyword: str = os.getenv('SMARTPARAMS_KEYWORD', default='class')
    missing_value: str = os.getenv('SMARTPARAMS_MISSING_VALUE', default='???')

    check_missings: bool = strutil.to_bool(os.getenv('SMARTPARAMS_CHECK_MISSINGS', default='yes'))
    check_typings: bool = strutil.to_bool(os.getenv('SMARTPARAMS_CHECK_TYPINGS', default='yes'))
    check_overrides: bool = strutil.to_bool(os.getenv('SMARTPARAMS_CHECK_OVERRIDES', default='yes'))

    allow_only_registered_classes: bool = strutil.to_bool(
        os.getenv('SMARTPARAMS_ALLOW_ONLY_REGISTERED_CLASSES', default='no'),
    )

    strict: bool = strutil.to_bool(os.getenv('SMARTPARAMS_STRICT', default='no'))
    debug: bool = strutil.to_bool(os.getenv('SMARTPARAMS_DEBUG', default='no'))

    lab = SmartLab()
    register = SmartRegister()

    def __init__(
        self,
        _callable: Callable[..., T] = cast(Callable[..., T], dict),
        /,
        **kwargs: Any,
    ) -> None:
        """Creates instance of Smart class.

        Args:
            _callable: Callable object to be wrapped.
            **kwargs: Partial keyword arguments to be passed to the callable object.

        """
        if not callable(_callable):
            raise TypeError("Object is not callable.")

        self._location: str = ''

        self._callable = _callable
        self._params: Dict[str, Any] = dict()

        for key, value in kwargs.items():
            self.set(key, value)

        if callable(smart_init := getattr(self._callable, '__smart_init__', None)):
            smart_init(self)

    @property
    def type(self) -> Type[T]:
        return typeutil.get_return_type(self._callable)

    @property
    def dict(self) -> Dict[str, Any]:
        return self._params.copy()

    def __call__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """Creates instance of given type.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            An class instance.

        """
        callable_name = strutil.join_objects(self._location, typeutil.get_name(self._callable))
        params = self.dict

        if self.check_overrides:
            typeutil.check_overrides(
                params=params,
                kwargs=kwargs,
                callable_name=callable_name,
                raise_error=self.strict,
            )

        params.update(kwargs)

        return self._init(
            callable_name=callable_name,
            callable_=self._callable,
            location=self._location,
            args=args,
            kwargs=params,
        )

    def __str__(self) -> str:
        callable_string = "" if self._callable is dict else f"[{typeutil.get_name(self._callable)}]"
        params_string = ", ".join((f"{k}={v}" for k, v in self._params.items()))
        return f"{Smart.__name__}{callable_string}({params_string})"

    def __repr__(self) -> str:
        return str(self)

    def keys(
        self,
        flatten: bool = False,
        pattern: Optional[str] = None,
    ) -> Iterable[str]:
        """Generates keys existing in the dictionary.

        Args:
            flatten: Whether to return the flattened keys in the nested dictionaries.
            pattern: Regex pattern for filtering keys.

        Yields:
            Keys from dictionary.

        """
        keys = dictutil.flatten_keys(self._params) if flatten else self._params
        if pattern is None:
            yield from keys
        else:
            yield from (key for key in keys if re.fullmatch(pattern, key))

    def values(
        self,
        flatten: bool = False,
        pattern: Optional[str] = None,
    ) -> Iterable[Any]:
        """Generates values existing in the dictionary.

        Args:
            flatten: Whether to return the values in the nested dictionaries.
            pattern: Regex pattern for filtering values by key.

        Yields:
            Values from dictionary.

        """
        yield from (self.get(k) for k in self.keys(flatten, pattern))

    def items(
        self,
        flatten: bool = False,
        pattern: Optional[str] = None,
    ) -> Iterable[Tuple[str, Any]]:
        """Generates items existing in the dictionary.

        Args:
            flatten: Whether to return the items in the nested dictionaries.
            pattern: Regex pattern for filtering items by key.

        Yields:
            Items from dictionary.

        """
        yield from ((k, self.get(k)) for k in self.keys(flatten, pattern))

    def isin(
        self,
        key: str,
    ) -> bool:
        """Checks if key is in dictionary.

        Args:
            key: The key to be checked.

        Returns:
            True if key is in dictionary, otherwise False.

        """
        return dictutil.check_key_is_in(
            key=key,
            dictionary=self._params,
        )

    def get(
        self,
        key: str,
        default: Optional[Any] = ...,
    ) -> Any:
        """Returns value of given key from dictionary.

        Args:
            key: The key of value.
            default: Value returned if key doesn't exist.

        Returns:
            Value matched with given key.

        Raises:
            ValueError if key doesn't exist and default value not specified.

        """
        dictionary, last_key = dictutil.find_nested(
            dictionary=self._params,
            key=key,
            required=default is ...,
        )
        return dictionary.get(last_key, default)

    def set(
        self,
        key: str,
        value: Any,
    ) -> Any:
        """Sets new value of given key in dictionary.

        Args:
            key: The key of value.
            value: Value to be set.

        Returns:
            The given value.

        """
        dictionary, last_key = dictutil.find_nested(
            dictionary=self._params,
            key=key,
            set_mode=True,
        )
        dictionary[last_key] = value
        return value

    def pop(
        self,
        key: str,
        default: Optional[Any] = ...,
    ) -> Any:
        """Removes and returns value of given key from dictionary.

        Args:
            key: The key of value.
            default: Value returned if key doesn't exist.

        Returns:
            Removed value.

        Raises:
            ValueError if key doesn't exist and default value not specified.

        """
        dictionary, last_key = dictutil.find_nested(
            dictionary=self._params,
            key=key,
            required=default is ...,
        )
        return dictionary.pop(last_key, default)

    def map(
        self,
        key: str,
        function: Callable,
    ) -> Any:
        """Applies value of given key to given function.

        Args:
            key: Key of value to be mapped.
            function: A function to which map passes a value.

        Returns:
            Mapped value.

        Raises:
            ValueError if key doesn't exist.

        """
        dictionary, last_key = dictutil.find_nested(
            dictionary=self._params,
            key=key,
            required=True,
        )
        dictionary[last_key] = value = function(dictionary[last_key])
        return value

    def update(
        self,
        **kwargs: Any,
    ) -> 'Smart':
        """Updates existing items with given keyword arguments.

        Args:
            kwargs: New items to update.

        Returns:
            Smart instance.

        """
        return self.update_from(kwargs)

    def update_from(
        self,
        source: Union['Smart', Mapping[str, Any], Sequence[str], str, Path],
        source_key: Optional[str] = None,
        target_key: Optional[str] = None,
        override: bool = True,
        required: bool = True,
    ) -> 'Smart':
        """Updates existing items from given source.

        Args:
            source: Smart object, dictionary, list or path of new items to update.
            source_key: Key of source object to update.
            target_key: Key of smart object to be updated.
            override: Whether to override existing items.
            required: Whether the source_key is required to exist.

        Returns:
            Smart instance.

        Raises:
            TypeError if given source is not supported.

        """
        smart: Smart
        if isinstance(source, Smart):
            smart = source
        elif isinstance(source, (str, Path)):
            smart = Smart(**load_data(Path(source)))
        elif isinstance(source, Mapping):
            smart = Smart(**source)
        elif isinstance(source, Sequence):
            smart = Smart(**dict(map(strutil.parse_param, source)))
        else:
            raise TypeError(f"Source type '{type(source)}' is not supported.")

        if source_key is None:
            for key in smart.keys(flatten=True):
                new_key = strutil.join_keys(target_key, key) if target_key else key
                if override or not self.isin(new_key):
                    self.set(new_key, smart.get(key))
        else:
            try:
                self.update_from(
                    source=smart.get(source_key, default=... if required else dict()),
                    target_key=target_key,
                    override=override,
                )
            except Exception as e:
                raise RuntimeError(
                    f"Cannot update with source key '{source_key}'. " + ' '.join(e.args)
                )

        return self

    @classmethod
    def load_from(
        cls,
        source: Union['Smart', Mapping[str, Any], Sequence[str], str, Path],
        key: Optional[str] = None,
    ) -> Any:
        """Loads object from the given source.

        Args:
            source: Smart object, dictionary, list or path of object to load.
            key: Key of source dictionary.

        Returns:
            Instance of loaded source.

        Raises:
            TypeError if given source is not supported.

        """
        return cls().update_from(source=source, source_key=key).init()

    def init(
        self,
        key: Optional[str] = None,
        persist: bool = True,
    ) -> Any:
        """Instantiates dictionary with given key.

        Args:
            key: Key of dictionary to be instantiated.
            persist: Whether to keep instantiated object in dictionary.

        Returns:
            Object of instantiated class.

        """
        if key is None:
            obj = self._init_object(
                obj=self._params,
                location=self._location,
            )
        else:
            obj = self._init_object(
                obj=self.get(key),
                location=strutil.join_keys(self._location, key),
            )

            if persist:
                return self.set(key, obj)

        return obj

    def representation(
        self,
        skip_defaults: bool = False,
        merge_params: bool = False,
    ) -> Dict[str, Any]:
        """Creates representation of Smart object.

        Args:
            skip_defaults: Whether to skip arguments with default values.
            merge_params: Whether to join items from dictionary.

        Returns:
            Dictionary with Smart representation.

        """
        smart: Smart = Smart()

        if merge_params:
            smart.update_from(self)

        smart.update_from(
            source=self._object_representation(
                obj=self._callable,
                skip_default=skip_defaults,
            ),
            override=False,
        )

        return typeutil.convert_to_primitive_types(
            obj=smart.dict,
            missing_value=self.missing_value,
        )

    def metadata(
        self,
        save_to: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Returns most important metadata of platform and project versions.

        Args:
            save_to: Path to save metadata.

        Returns:
            Dictionary with metadata.

        """
        metadata = dict(
            **self.lab.metadata(),
            params=typeutil.convert_to_primitive_types(
                obj=self.dict,
                missing_value=self.missing_value,
            ),
        )

        if save_to:
            metadata_history = load_data(save_to) if save_to.exists() else dict()
            metadata_history[f'run{len(metadata_history) + 1:03d}'] = metadata
            save_data(
                data=metadata_history,
                path=save_to,
            )

        return metadata

    def run(
        self,
        function: Optional[Callable[['Smart'], Any]] = None,
        path: Optional[Path] = None,
    ) -> 'Smart':
        """Runs main function.

        Args:
            function: Main function to be run.
            path: Path of params file.

        Returns:
            Smart object.

        """
        parser = create_argument_parser(
            default_path=path,
        )
        args = parse_arguments(parser)

        try:
            self._run(
                function=function,
                args=args,
            )
        except DummyError if self.debug else ConfigurationError as e:
            parser.error(e.message)

        return self

    def _run(
        self,
        function: Optional[Callable[['Smart'], Any]],
        args: Arguments,
    ) -> None:
        Smart.strict = Smart.strict or args.strict
        Smart.debug = Smart.debug or args.debug

        if args.path and args.path.exists():
            self.update_from(args.path)

        self.update_from(args.params)

        if args.dump:
            if not args.path:
                raise MissingPath()

            save_data(
                data=self.representation(
                    skip_defaults=args.skip_defaults,
                    merge_params=args.merge_params,
                ),
                path=args.path,
            )
        elif args.print:
            if args.print == Print.PARAMS:
                print_data(
                    data=self.representation(
                        skip_defaults=args.skip_defaults,
                        merge_params=args.merge_params,
                    ),
                    fmt=args.format,
                )
            elif args.print == Print.DICT:
                print_data(
                    data=typeutil.convert_to_primitive_types(
                        obj=self._params,
                        missing_value=self.missing_value,
                    ),
                    fmt=args.format,
                )
            elif args.print == Print.KEYS:
                print_data(
                    data=tuple(self.keys(flatten=True)),
                    fmt=args.format,
                )
            else:
                raise NotImplementedError(f"Print '{args.print}' has not been implemented yet.")
        elif function is None:
            self()
        else:
            function(self)

    def _init_object(
        self,
        obj: Any,
        location: str,
    ) -> Any:
        if isinstance(obj, dict):
            if self.keyword in obj:
                return self._init_from_dict(
                    dictionary=obj,
                    location=location,
                )

            return self._init_dict(
                dictionary=obj,
                location=location,
            )

        if isinstance(obj, list):
            return self._init_list(
                lst=obj,
                location=location,
            )

        return obj

    def _init_dict(
        self,
        dictionary: Dict[str, Any],
        location: str,
    ) -> Dict[str, Any]:
        return {
            key: self._init_object(
                obj=value,
                location=strutil.join_keys(location, key),
            )
            for key, value in dictionary.items()
        }

    def _init_list(
        self,
        lst: List[Any],
        location: str,
    ) -> List[Any]:
        return [
            self._init_object(
                obj=element,
                location=strutil.join_keys(location, str(index)),
            )
            for index, element in enumerate(lst)
        ]

    def _init_from_dict(
        self,
        dictionary: Dict[str, Any],
        location: str,
    ) -> Any:
        kwargs, name, option = typeutil.parse_object(
            dictionary=dictionary,
            keyword=self.keyword,
        )

        if name == Smart.__name__:
            return self._init(
                callable_name=strutil.join_objects(location, Smart.__name__),
                callable_=Smart,
                location=location,
                kwargs=kwargs,
            )

        if name in self.register.origins:
            name = self.register.origins[name]
        elif self.allow_only_registered_classes:
            raise ObjectNotRegistered(name, location)

        callable_ = typeutil.import_callable(name, location=location)
        callable_name = strutil.join_objects(location, typeutil.get_name(callable_))

        if option:
            if option == Option.SMART:
                return self._init(
                    callable_name=callable_name,
                    callable_=Smart,
                    location=location,
                    args=(callable_,),
                    kwargs=kwargs,
                )

            if option == Option.TYPE:
                if kwargs:
                    raise UnexpectedTypeOptionArguments(callable_name)

                return callable_

            raise ObjectInvalidOptionError(option, location)

        return self._init(
            callable_name=callable_name,
            callable_=callable_,
            location=location,
            kwargs=kwargs,
        )

    def _init(
        self,
        callable_name: str,
        callable_: Callable,
        location: str,
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        args = args or tuple()
        kwargs = kwargs or dict()

        kwargs = self._init_dict(
            dictionary=kwargs,
            location=location,
        )

        if self.check_missings:
            typeutil.check_missings(
                kwargs=kwargs,
                missing_value=self.missing_value,
                callable_name=callable_name,
                raise_error=self.strict,
            )

        if self.check_typings:
            typeutil.check_typings(
                callable_=callable_,
                args=args,
                kwargs=kwargs,
                callable_name=callable_name,
                raise_error=self.strict,
            )

        try:
            obj = callable_(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Error during instantiate '{callable_name}'; {e}") from e
        else:
            if isinstance(obj, Smart):
                obj._location = location

            return obj

    def _object_representation(
        self,
        obj: Any,
        skip_default: bool,
    ) -> Dict[str, Any]:
        representation: Dict[str, Any] = dict()
        try:
            signature = inspect.signature(obj)
        except ValueError:
            return representation

        for i, param in enumerate(signature.parameters.values()):
            name = param.name
            kind = param.kind
            annotation = param.annotation
            default = param.default

            if not (default is not param.empty and skip_default) and (
                not (i == 0 and annotation is param.empty and default is param.empty)
                or kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
            ):
                if annotation is Smart:
                    representation[name] = {
                        self.keyword: Smart.__name__,
                    }
                elif get_origin(annotation) is Smart:
                    param_type, *_ = get_args(annotation)

                    keyword = inspect.formatannotation(param_type)
                    keyword = self.register.aliases.get(keyword, keyword)
                    keyword = strutil.join_objects(keyword, Option.SMART.value)

                    representation[name] = {
                        self.keyword: keyword,
                        **self._object_representation(
                            obj=param_type,
                            skip_default=skip_default,
                        ),
                    }
                elif isinstance(default, (bool, float, int, str, type(None))):
                    representation[name] = default
                elif annotation is not param.empty and isinstance(annotation, type):
                    if annotation in (bool, float, int, str):
                        representation[name] = annotation.__name__ + self.missing_value
                    else:
                        keyword = inspect.formatannotation(annotation)
                        keyword = self.register.aliases.get(keyword, keyword)
                        representation[name] = {
                            self.keyword: keyword,
                            **self._object_representation(
                                obj=annotation,
                                skip_default=skip_default,
                            ),
                        }
                else:
                    representation[name] = self.missing_value

        return representation
