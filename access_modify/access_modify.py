import inspect

class AccessException(Exception): pass

isFunc = lambda f: isinstance(f, type(lambda: 1))
isClass = lambda c: hasattr(c, '__call__') and not isFunc(c)

def privatefunc(cls, f):
  def _(*args, **kwargs):
    caller = inspect.stack()[1].function
    if not (
      hasattr(cls, caller) or
      any(map(
        lambda x: hasattr(x, caller),
        list(filter(isClass, dict(cls.__dict__).values()))
      ))
    ):
      raise AccessException("Private function cannot be accessed.")
    return f(*args, **kwargs)
  return _

def protectedfunc(cls, f):
  def _(*args, **kwargs):
    mycls = type(args[0])
    caller = inspect.stack()[1].function
    if (
      not hasattr(mycls, caller) or (
        cls != mycls and
        not hasattr(cls, caller) and
        not cls.__name__ in list(map(
          lambda x: x.__name__,
          mycls.__bases__
        ))
      )
    ):
      raise AccessException("Protected function cannot be accessed.")
    return f(*args, **kwargs)
  return _

def access(cls):
  d = dict(cls.__dict__)
  functions = {
    key : d[key] for key in d.keys()
    if isFunc(d[key])
  }
  
  d['__access_modify'] = True
  
  
  for key in functions:
    f = d[key]
    acc = getattr(f, 'access', 'public')
    if acc == 'private':
      d[key] = privatefunc(cls, f)
    elif acc == 'public':
      d[key] = f
    elif acc == 'protected':
      d[key] = protectedfunc(cls, f)
      
  return type(cls.__name__, cls.__bases__, d)


def gen(name):
  def decorator(func):
    setattr(func, 'access', name)
    return func
  return decorator

private = gen('private')
protected = gen('protected')
public = gen('public')


if __name__ == '__main__':
  @access
  class test:
    @private
    def __init__(self):
      self.a = 1
    
    class builder:
      def build():
        return test()
    
    class Inside:
      def b(self): return test.a(1)
  
  print(test.builder.build())
