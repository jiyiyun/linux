产生偏移和元素
---
python2.x中
``` shell
>>> S ='spam'
>>> offset = 0
>>> for item in S:
...     print(item,'appears at offset',offset)
...     offset += 1
... 
('s', 'appears at offset', 0)
('p', 'appears at offset', 1)
('a', 'appears at offset', 2)
('m', 'appears at offset', 3)
```

Python3.x中
``` shell
>>> S = 'spam'
>>> for (offset,item) in enumerate(S):
...     print(item,'appears at offset',offset)
... 
s appears at offset 0
p appears at offset 1
a appears at offset 2
m appears at offset 3
```

enumerate函数返回一个生成器对象：这种对象支持迭代协议