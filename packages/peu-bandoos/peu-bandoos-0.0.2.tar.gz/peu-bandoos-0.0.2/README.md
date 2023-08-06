# peu
Python experiment utils

Utilities for software experimentation in python.
Here I publish small utilities I recurrently use in experimental projects.
This is also a pretext to publish my first package on PyPi.

This is a work in progress, and by now only includes a few
meaningful functions.
- `peu.core:dict_product` perfroming the a dictiionary flavoured
  cartesian product, useful to generate parameter combination for
  software experiments.

- `peu.multi:tracked_multproc_unordered` perfroming application of
  function in parallel (via multiprocessing Pool) over a sequence of
  inputs, using `tqdm` to monitor progress

# Examples

## dict_product
```python
from peu.core import dict_product

params = {'a': [1,2,3],
          'b': {True, False}}

fixed = {'max_epochs':100,
         'scoring': 'accuracy'}

configs = dict_product (params, fixed=fixed)

# =>
# [{'a': 1, 'b': False, 'max_epochs': 100, 'scoring': 'accuracy'},
#  {'a': 1, 'b': True, 'max_epochs': 100, 'scoring': 'accuracy'},
#  {'a': 2, 'b': False, 'max_epochs': 100, 'scoring': 'accuracy'},
#  {'a': 2, 'b': True, 'max_epochs': 100, 'scoring': 'accuracy'},
#  {'a': 3, 'b': False, 'max_epochs': 100, 'scoring': 'accuracy'},
#  {'a': 3, 'b': True, 'max_epochs': 100, 'scoring': 'accuracy'}]

```

## tracked\_multiproc\_unordered
```python

from peu.multi import tracked_multiproc_unordered
import time


def f(x):
    time.sleep(0.1)
    return (x + 1)**2

tracked_multiproc_unordered(f, range(100))

# 100%|████████████████████████████████████████████████████████████████| 100/100 [00:01<00:00, 76.71it/s]

```



# Installation

The package is published on pypi @ https://pypi.org/project/peu-bandoos/0.0.2/

`$ pip install peu-bandoos==0.0.2`
