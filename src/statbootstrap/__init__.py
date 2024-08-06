"""Implementation of statistical bootstrap."""

# Copyright (C) 2024-Today Michaël Hooreman

from statbootstrap._frontend import bootstrap
from statbootstrap._types import (
    BootstrapResults,
    NotVectorizedBootstrapWarning,
    PropertyNotYetSetError,
    SettingReadOnlyPropertyError,
)

__all__ = [
    "BootstrapResults",
    "NotVectorizedBootstrapWarning",
    "PropertyNotYetSetError",
    "SettingReadOnlyPropertyError",
    "bootstrap",
]

__version__ = "0.2.0"
