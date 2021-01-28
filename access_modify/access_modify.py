import inspect

class AccessException(Exception): pass

isFunc = lambda f: isinstance(f, type(lambda: 1))
isClass = lambda c: hasattr(c, '__call__') and not isFunc(c)
hasAttribute = \
  lambda cls, caller: \
    hasattr(cls, caller) or any(map(
      lambda x: hasattr(x, caller),
      list(filter(isClass, dict(cls.__dict__).values()))
    ))

def privatefunc(cls, f):
  def _(*args, **kwargs):
    caller = inspect.stack()[1].function
    if not hasAttribute(cls, caller):
      raise AccessException("Private function cannot be accessed.")
    return f(*args, **kwargs)
  return _

def protectedfunc(cls, f):
  def _(*args, **kwargs):
    mycls = type(args[0])
    caller = inspect.stack()[1].function
    if not (
      hasAttribute(mycls, caller) and (
        cls == mycls or
        hasAttribute(cls, caller) or
        cls.__name__ in list(map(
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
    @protected
    def __init__(self):
      self.a = 1
    
    class builder:
      def build():
        return test()
    
    class Inside:
      def b(self): return test.a(1)
  
  print(test.builder.build())

  @access
  class asdf:
    @protected
    def a(self): return 1

  class qwer(asdf):
    def b(self): return self.a()+1
  
  print(qwer().b())
