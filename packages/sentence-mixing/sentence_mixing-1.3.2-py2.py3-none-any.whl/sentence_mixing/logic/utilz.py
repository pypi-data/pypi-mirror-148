import functools


CACHED_FUNCTIONS = []
def lru_cache(*args, **kwargs):
  def decorator(f):
    fa = functools.lru_cache(*args, **kwargs)(f)
    CACHED_FUNCTIONS.append(fa)
    return fa
  return decorator