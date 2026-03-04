# Python Dataclass 示例

这个目录包含一组实用示例，用来演示如何高效使用 Python 的 `dataclasses` 模块。每个示例都展示了 dataclass 的不同用法，同时覆盖了推荐实践和常见陷阱。

## 概览

Dataclass 是 Python 3.7 引入的特性（PEP 557），它提供了一种更简洁的方式来定义以“存储数据”为主的类。它会根据类字段自动生成 `__init__()`、`__repr__()`、`__eq__()` 等特殊方法，从而减少样板代码，并让代码更易读、更易维护。

## 示例文件

1. **[01_basic_dataclasses.py](01_basic_dataclasses.py)**：dataclass 的基础用法
   - 简单 dataclass 定义
   - 类型注解
   - 默认值
   - 使用 `field()` 处理可变默认值
   - 与传统类的对比

2. **[02_nested_dataclasses.py](02_nested_dataclasses.py)**：嵌套 dataclass 的使用
   - 正确的嵌套结构
   - 序列化为 JSON
   - 扁平结构的常见问题
   - 使用字典代替 dataclass 的问题

3. **[03_inheritance_dataclasses.py](03_inheritance_dataclasses.py)**：dataclass 继承
   - 正确的继承模式
   - 避免继承字段中的类型冲突
   - 继承场景下默认值的问题
   - 普通类与 dataclass 混用的注意点

4. **[04_immutable_dataclasses.py](04_immutable_dataclasses.py)**：`frozen=True` 的不可变 dataclass
   - 创建不可变对象
   - 用工厂方法创建新实例
   - 不可变 dataclass 中仍包含可变对象时的陷阱
   - 使用 `__post_init__` 的初始化技巧

5. **[05_large_data_dataclasses.py](05_large_data_dataclasses.py)**：大数据场景下的 dataclass
   - 高效的 dataclass 设计
   - 使用 `slots` 优化内存
   - 延迟加载模式
   - 性能方面的考虑
   - 什么场景不适合用 dataclass

6. **[06_dataclass_utilities.py](06_dataclass_utilities.py)**：dataclass 的工具函数
   - 使用 `asdict()` 和 `astuple()`
   - `replace()` 函数
   - 使用 `is_dataclass()` 判断对象是否是 dataclass
   - 使用 `fields()` 对 dataclass 做自省

7. **[07_dataclass_with_pydantic.py](07_dataclass_with_pydantic.py)**：结合 Pydantic 的 dataclass 校验
   - Pydantic dataclass
   - 进阶校验模式
   - 标准 dataclass 与 Pydantic 混用
   - 数据转换与序列化

## 最佳实践

### 什么时候适合使用 Dataclass

✅ **适合的场景**：

- 只有少量或几乎没有行为的数据容器
- 值对象和 DTO（Data Transfer Object）
- 配置对象
- API 请求/响应模型
- 不可变数据结构（配合 `frozen=True`）

❌ **不适合的场景**：

- 行为复杂但数据很少的类
- 实例数量巨大且对内存极度敏感的场景（除非配合 `__slots__`）
- 需要完全掌控对象创建流程的场景

### Dataclass 设计指南

1. **使用类型注解**
   - 能提高代码可读性，并支持静态类型检查
   - 有利于 IDE 自动补全和文档生成

2. **正确处理可变默认值**
   - 对可变默认值总是使用 `field(default_factory=list)`
   - 避免把空列表或空字典直接写成默认值

3. **考虑不可变性**
   - 对不可变数据可使用 `frozen=True`
   - 注意 `frozen` dataclass 内部仍可能包含可变对象

4. **保持结构清晰**
   - 对复杂数据优先使用嵌套 dataclass，而不是扁平结构
   - 但也不要过度嵌套，一般控制在 3 到 4 层以内

5. **善用辅助函数**
   - 用 `asdict()` 和 `astuple()` 做序列化
   - 用 `replace()` 生成修改后的副本
   - 用 `fields()` 做字段自省

6. **需要时加入校验**
   - 简单校验可以放在 `__post_init__`
   - 复杂校验可考虑使用 Pydantic

## 性能考虑

- 标准 dataclass 的额外开销很小
- 如果实例数量非常大，可以考虑使用 `__slots__`
- 对极度敏感的性能场景，建议对比 benchmark：dataclass、普通类和 named tuple

## 延伸阅读

- [Python Documentation: dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [PEP 557 -- Data Classes](https://www.python.org/dev/peps/pep-0557/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 运行示例

每个文件都可以直接运行，以查看示例效果：

```bash
python 01_basic_dataclasses.py
python 02_nested_dataclasses.py
# 以此类推
```

## 依赖

- Python 3.7 或更新版本
- Pydantic（用于 Pydantic 示例）：`pip install pydantic`
