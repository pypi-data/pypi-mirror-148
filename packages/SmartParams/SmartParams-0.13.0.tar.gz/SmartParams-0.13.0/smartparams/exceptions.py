from typing import Set


class ConfigurationError(Exception):
    def __init__(
        self,
        message: str = '',
    ) -> None:
        self.message = message
        super().__init__(self.message)


class DummyError(ConfigurationError):
    pass


class MissingArgument(ConfigurationError):
    def __init__(
        self,
        callable_name: str,
        message: str,
    ) -> None:
        self.callable_name = callable_name
        super().__init__(f"The '{callable_name}' has {message}.")


class MissingArgumentValue(ConfigurationError):
    def __init__(
        self,
        callable_name: str,
        value_name: str,
    ) -> None:
        self.callable_name = callable_name
        self.value_name = value_name
        super().__init__(f"Missing {callable_name}'s argument '{value_name}' value.")


class ArgumentTypeError(ConfigurationError):
    def __init__(
        self,
        message: str,
    ) -> None:
        super().__init__(f"The {message}.")


class ArgumentParserError(ConfigurationError):
    def __init__(
        self,
        param: str,
    ) -> None:
        self.param = param
        super().__init__(f"Param '{param}' has not assigned value. Use {param}=... .")


class UnexpectedArgument(ConfigurationError):
    def __init__(
        self,
        callable_name: str,
        overrides: Set[str],
    ) -> None:
        self.callable_name = callable_name
        self.overrides = overrides
        super().__init__(f"Override {callable_name}'s arguments {overrides}.")


class MissingPath(ConfigurationError):
    def __init__(self) -> None:
        super().__init__("Cannot dump params if path is not specified.")


class ObjectNotFoundError(ConfigurationError):
    def __init__(
        self,
        name: str,
        location: str,
    ) -> None:
        self.name = name
        self.location = location
        super().__init__(f"Object '{name}' in '{location}' does not exist.")


class ObjectNotRegistered(ConfigurationError):
    def __init__(
        self,
        name: str,
        location: str,
    ) -> None:
        self.name = name
        self.location = location
        super().__init__(f"Object '{name}' in '{location}' is not registered.")


class UnexpectedTypeOptionArguments(ConfigurationError):
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        super().__init__(f"Cannot specify any arguments for {name}'s type.")


class ObjectInvalidOptionError(ConfigurationError):
    def __init__(
        self,
        option: str,
        location: str,
    ) -> None:
        self.option = option
        self.location = location
        super().__init__(f"Option '{option}' in '{location}' is not supported.")


class ObjectNotCallableError(ConfigurationError):
    def __init__(
        self,
        name: str,
        location: str,
    ) -> None:
        self.name = name
        self.location = location
        super().__init__(f"Object '{name}' in '{location}' is not callable.")
