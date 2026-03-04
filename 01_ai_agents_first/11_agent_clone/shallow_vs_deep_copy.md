# Python 中的浅拷贝与深拷贝（结合 dataclasses）

在 Python 中复制对象时，你可能以为自己得到的是一个完全独立的新版本，但实际上复制分成两种：

---

## 1. 什么是浅拷贝（Shallow Copy）？
- 会创建一个新的外层对象。
- 不会完整复制内部嵌套的可变对象（如列表、字典）。
- 嵌套对象会被共享，原对象和副本指向同一份内部数据。

### 示例
```python
import copy

list1 = [[1, 2], [3, 4]]
shallow_copy = copy.copy(list1)  # Shallow copy

shallow_copy[0].append(99)

print("Original:", list1)   # Both changed!
print("Copy:    ", shallow_copy)
````

原因是这两个列表共享相同的内部子列表。

---

## 2. 什么是深拷贝（Deep Copy）？

* 会创建一个新的外层对象。
* 会递归复制所有嵌套的可变对象。
* 没有共享引用，彼此完全独立。

### 示例

```python
deep_copy = copy.deepcopy(list1)
deep_copy[0].append(100)

print("Original:", list1)   # Unchanged
print("Copy:    ", deep_copy)
```

---

## 3. 浅拷贝 vs 深拷贝 对比表

| 特性 | 浅拷贝 | 深拷贝 |
| --------------------- | ------------ | --------- |
| 复制外层对象 | 是 | 是 |
| 复制嵌套对象 | 否（共享） | 是 |
| 内存消耗 | 低 | 更高 |
| 独立性 | 部分独立 | 完全独立 |

---

## 4. `dataclasses.replace` 中的浅拷贝

```python
from dataclasses import dataclass, field, replace
from typing import List

@dataclass
class Agent:
    name: str
    instructions: str
    tools: List[str] = field(default_factory=list)

agent1 = Agent(name="Original", instructions="Follow the plan", tools=["Hammer", "Wrench"])
agent2 = replace(agent1, name="Cloned")  # Shallow copy

print(agent1.tools is agent2.tools)  # True -> same list object
```

如果修改 `agent2.tools`，`agent1.tools` 也会变化：

```python
agent2.tools.append("Screwdriver")
print("Agent1 tools:", agent1.tools)  # Uh-oh, also changed!
```

---

## 5. 如何避免浅拷贝中的共享列表

你可以主动传入一个复制后的列表，避免共享引用：

```python
agent3 = replace(agent1, name="Safe Clone", tools=agent1.tools.copy())
agent3.tools.append("Pliers")

print("Agent1 tools:", agent1.tools)  # unchanged
print("Agent3 tools:", agent3.tools)
```

这会创建一个独立的列表容器，但如果列表内部元素本身还是可变对象，那么内部元素仍可能共享。

---

## 6. 用深拷贝实现彻底独立

使用 `copy.deepcopy()` 可以切断所有引用关系：

```python
import copy

agent4 = copy.deepcopy(agent1)
agent4.tools.append("Drill")

print("Agent1 tools:", agent1.tools)  # unchanged
print("Agent4 tools:", agent4.tools)
```

---

## 7. 添加一个 `clone()` 方法

我们还可以通过添加 `clone()` 方法让复制更方便：

```python
@dataclass
class Agent:
    name: str
    instructions: str
    tools: List[str] = field(default_factory=list)

    def clone(self, **changes):
        return replace(self, **changes)

# Example usage
a = Agent("A", "Test", ["tool1"])
b = a.clone(name="B", tools=a.tools.copy())

print(a.tools is b.tools)  # False -> different lists
```

---

## 8. 关键结论

* **浅拷贝**：快、节省内存，但会共享嵌套数据。
* **深拷贝**：完全独立，但会占用更多内存。
* 在 `dataclasses.replace` 中，可变字段默认是浅拷贝语义。
* 想避免 bug，可以：

  * 手动复制列表/字典（`.copy()`）
  * 或在需要完全独立时使用 `copy.deepcopy()`
