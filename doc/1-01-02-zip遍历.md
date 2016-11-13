并行遍历
---
``` shell
>>> L1 = [1,2,3,4,5]
>>> L2 = [6,7,8,9,0]
>>> z =(L1,L2)
>>> z
([1, 2, 3, 4, 5], [6, 7, 8, 9, 0])
>>> list(z(L1,L2))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object is not callable
>>> zip(L1,L2)
<zip object at 0x1029e90c8>
>>> list(zip(L1,L2))
[(1, 6), (2, 7), (3, 8), (4, 9), (5, 0)]
```
我们可以用zip来创建一个元组对列表，(和range一样，zip在python3中也是一个可以迭代的对象，我们必须将其包含在list调用中以便一次性显示出所有结果来)
``` shell
>>> for (x,y) in zip(L1,L2):
...     print(x,'+',y,"=" ,x +y)
... 
1 + 6 = 7
2 + 7 = 9
3 + 8 = 11
4 + 9 = 13
5 + 0 = 5

>>> T1,T2,T3 =(1,2,3),(4,5,6),(7,8,9)
>>> T3
(7, 8, 9)
>>> list(zip(T1,T2,T3))
[(1, 4, 7), (2, 5, 8), (3, 6, 9)]
>>> 

>>> S1 ='abc'
>>> S2 ='xyz123'
>>> list(zip(S1,S2))
[('a', 'x'), ('b', 'y'), ('c', 'z')]
```