from collections import Iterable
import itertools
import numpy as np


def expspace(vmin, vmax, n, base=2):
  fmax = base ** (n - 1)
  space = ((np.geomspace(1, fmax, n) - 1) * (vmax - vmin) / (fmax-1)) + vmin
  return space

def coalesce(*args):
  valid = [a for a in args if a is not None]
  return valid[0] if valid else None

def getcallable(obj, callable_name, default='_undefined_'):
  method = getattr(obj, callable_name, default)
  if method == '_undefined_':
    raise AttributeError("'%s' object has no attribute '%s'" % (type(obj),callable_name))
  if not callable(method):
    raise AttributeError("'%s' object has attribute but not callable '%s'" % (type(obj), callable_name))
  return method

def isiterable(obj,exclude=(str,)):
  iterable = isinstance(obj, Iterable)
  excluded = isinstance(obj,exclude)
  return iterable and not excluded

def czip(*values):
  maxl = max((len(v) for v in values))
  iters = [(itertools.cycle(v)) for v in values]
  values = [[next(i) for _ in range(maxl)] for i in iters]
  return list(zip(*values))


def to_list(unknown, empty_if=(None,), sep=None):
  if isinstance(unknown,np.ndarray):
    unknown = unknown.tolist()

  if unknown in empty_if:
    return []
  elif isinstance(unknown, list):
    return unknown
  elif isinstance(unknown, str):
    if sep is not None:
      return [s.strip() for s in unknown.split(sep)]
    else:
      tries = [',',' ']
      for t in tries:
        if t in unknown:
          return [s.strip() for s in unknown.split(t)]
      return [unknown.strip()]
  elif isiterable(unknown):
    return list(unknown)
  else:
    return [unknown]


def to_type(value,typ):
    if isinstance(typ,type):
        return typ(value)
    else:
        return [e for e in typ if str(e)==value][0]
