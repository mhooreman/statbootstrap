# Copyright (C) 2024-Today Michaël Hooreman

from statbootstrap._backend import Bootstrap


def bootstrap(x, estimator, confidence=0.95, *, n_boot=10000):
    return Bootstrap(x, estimator, n_boot=n_boot).estimate(confidence)
