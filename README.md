# Access Modify
Use private, protected class methods in Python!

## Download
`pip install access-modify`

## Example

```Python
from access_modify import *


@access
class Test:
    # Test.a can be used by Test class methods.
    @private
    def a(self): return 1
    
    # Test.b can be used by Test class, or inherited class methods.
    @protected
    def b(self): return self.a()+1

class Inherited(Test):
    @public
    def c(self): return self.b()+1

r = Test()
w = Inherited()
print(r.a()) # raise AccessException
print(r.b()) # raise AccessException
print(w.c()) # 3
```
