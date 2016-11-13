map
---
``` shelll
>>> S1 = 'abc'
>>> S2 = 'xyz123'
>>> list(zip(S1,S2))
[('a', 'x'), ('b', 'y'), ('c', 'z')]
>>> map(None,S1,S2)
[('a', 'x'), ('b', 'y'), ('c', 'z'), (None, '1'), (None, '2'), (None, '3')]
>>> 
```