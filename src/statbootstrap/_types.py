import typing


class PropertyNotYetSetError(RuntimeError):
    pass


class SettingReadOnlyPropertyError(RuntimeError):
    pass


class NotVectorizedBootstrapWarning(UserWarning):
    pass


class BootstrapResults(typing.NamedTuple):
    confidence: float
    lower: float
    estimated: float
    higher: float
