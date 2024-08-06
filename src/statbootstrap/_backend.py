# Copyright (C) 2024-Today Michaël Hooreman

import functools
import warnings

import numpy as np
import pandas as pd

from statbootstrap._types import (
    BootstrapResults,
    NotVectorizedBootstrapWarning,
    PropertyNotYetSetError,
    SettingReadOnlyPropertyError,
)


class Bootstrap:
    def __init__(self, x, estimator, n_boot):
        # Declaration of private attributes
        self._x = None
        self._estimator = None
        self._n_boot = None
        self._parallel = None
        # Setting the properties using the setters
        self.x = x
        self.estimator = estimator
        self.n_boot = n_boot

    @property
    def x(self):
        if self._x is None:
            raise PropertyNotYetSetError
        return self._x

    @x.setter
    def x(self, value):
        if self._x is not None:
            raise SettingReadOnlyPropertyError
        try:
            iter(value)
        except TypeError as e:
            msg = "provided samples is not iterable"
            raise ValueError(msg) from e
        self._x = value

    @property
    def n_boot(self):
        if self._n_boot is None:
            raise PropertyNotYetSetError
        return self._n_boot

    @n_boot.setter
    def n_boot(self, value):
        if self._n_boot is not None:
            raise SettingReadOnlyPropertyError
        if not isinstance(value, int):
            msg = f"n_boot must be integer, got {type(value)}"
            raise TypeError(msg)
        if value < 1:
            msg = f"n_boot must be > 0, got {value}"
            raise ValueError(msg)
        self._n_boot = value

    @property
    def estimator(self):
        if self._estimator is None:
            raise PropertyNotYetSetError
        return self._estimator

    @estimator.setter
    def estimator(self, value):
        if not callable(value):
            msg = f"estimator {value} is not callable"
            raise TypeError(msg)
        self._estimator = value

    @functools.cached_property
    def _x_array(self):
        ret = np.array(self.x)
        if ret.ndim != 1:
            msg = f"sample must be 1 dimension, got {ret.ndim}"
            raise ValueError(msg)
        return ret

    @property
    def _boot_samples(self):
        return np.random.default_rng().choice(
            self._x_array,
            size=[self._x_array.shape[0], self.n_boot],
            replace=True,
        )

    @functools.cached_property
    def _estimated_boots(self):
        try:
            return self.estimator(self._boot_samples, axis=0)
        except TypeError:
            warnings.warn(
                (
                    f"{self.estimator}(samples, axis=0) failed; falling back "
                    "to slower pd.DataFrame.apply"
                ),
                NotVectorizedBootstrapWarning,
                stacklevel=2,
            )
            # Most probably that the estimator cannot be called as vectorized
            # on np.array with axis argument. Trying with pd.apply(...).values.
            return np.array(
                pd.DataFrame(self._boot_samples).apply(self.estimator, axis=0),
            )

    @functools.cached_property
    def cdf_boots(self):
        ret = pd.DataFrame({"estimated": self._estimated_boots})
        ret = ret.sort_values(by="estimated")
        ret["boot"] = np.arange(ret.shape[0]) + 1
        ret["cdf"] = ret.boot / ret.boot.max()
        del ret["boot"]
        ret = ret.set_index("estimated", drop=True)
        return ret.cdf

    def _get_cdf_boot_closest_proba(self, cum_proba):
        return np.abs(self.cdf_boots - cum_proba).idxmin()

    def estimate(self, confidence):
        if confidence <= 0 or confidence >= 1:
            msg = f"confidence must be > 0 and < 1, got {confidence}"
            raise ValueError(msg)
        return BootstrapResults(
            confidence=confidence,
            lower=self._get_cdf_boot_closest_proba(1 - confidence),
            higher=self._get_cdf_boot_closest_proba(confidence),
            estimated=self._get_cdf_boot_closest_proba(0.5),
        )
