# statbootstrap
Implementation of statistical boostrap

## Documentation

TODO. Please find example code below

```
>>> from statbootstrap import bootstrap
>>> import numpy as np
>>> x = np.random.normal(0, 1, 1000)
>>> bootstrap(x, np.mean)
BootstrapResults(confidence=0.95, lower=-0.05015053758760554, estimated=-0.0010207366081064339, higher=0.05001335040444442)
>>> x = np.arange(10)
>>> bootstrap(x, lambda x: sum(list(x)))
C:\Users\Michael.Hooreman\AppData\Local\Programs\Python\Python312\Lib\functools.py:995: NotVectorizedBootstrapWarning: <function <lambda> at 0x000002D80FD5E2A0>(samples, axis=0) failed; falling back to slower pd.DataFrame.apply
  val = self.func(instance)
BootstrapResults(confidence=0.95, lower=30, estimated=45, higher=60)
>>>
```
