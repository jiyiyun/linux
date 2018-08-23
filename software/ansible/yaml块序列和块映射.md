yaml块序列和块映射
---

块序列就是把元素序列映射到python 列表中

```yaml
- 
 - hesperiidae
 - papilionidae
 - Apstelodidae
 - Epiplemidae

-
 - China
 - USA
 - Japan

```
对应的python结果为

```python
[['hesperiidae','papilionidae','Apstelodidae','Epiplemidae'],['China','USA','Japan']]
```

块映射描述
---

块映射就是将描述映射到python的字典dictionary中去，格式为key:value

```yaml
- hero:
    hp:34
    sp:8
    level:4
- orc:
    hp: 
     - 12
     - 30
    sp: 0
    level: 2
```
对应的python结果为：

{{'hero':{'hp':34,'sp':8,'level':4}},{'orc':{'hp':[12,30],'sp':0,'level':2}}}