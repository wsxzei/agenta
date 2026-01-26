# Agenta SDK 学习教程

这是一个循序渐进的学习系列，帮助你理解 Agenta SDK 中装饰器和端点生成机制。

## 课程目录

### 📚 Lesson 1: 最简单的装饰器 (`01_simple_decorator.py`)
**学习目标：**
- 理解装饰器的基本概念
- 掌握装饰器的执行时机（导入时 vs 调用时）
- 理解函数包装的原理

**运行方式：**
```bash
python 01_simple_decorator.py
```

### 📚 Lesson 2: 类装饰器 (`02_class_decorator.py`)
**学习目标：**
- 理解类作为装饰器的工作原理
- 掌握 `__init__` 和 `__call__` 方法的执行顺序
- 理解 `@ag.route("/")` 这种语法背后的机制

**运行方式：**
```bash
python 02_class_decorator.py
```

### 📚 Lesson 3: 类装饰器在内部注册路由 (`03_class_with_internal_registration.py`)
**学习目标：**
- 理解如何在装饰器执行时自动注册端点
- 掌握一个函数如何生成多个端点
- 理解包装函数的不同行为

**运行方式：**
```bash
python 03_class_with_internal_registration.py
```

### 📚 Lesson 4: 集成 FastAPI (`04_fastapi_integration.py`)
**学习目标：**
- 使用真实的 FastAPI 框架
- 理解中间件的作用
- 掌握 `/run` 和 `/test` 端点的不同行为

**运行方式：**
```bash
# 启动服务器
python 04_fastapi_integration.py

# 或使用 uvicorn
uvicorn 04_fastapi_integration:app --reload
```

**测试端点：**
```bash
# /run 端点（需要配置）
curl -X POST http://localhost:8000/run

# /test 端点（不需要配置）
curl -X POST http://localhost:8000/test

# 查看文档
open http://localhost:8000/docs
```

### 📚 Lesson 5: 完整的 Agenta 风格实现 (`05_full_agenta_style.py`)
**学习目标：**
- 最接近 serving.py 的完整实现
- 理解中间件注册机制（只注册一次）
- 掌握配置 Schema 的定义和使用
- 理解完整的请求流程

**运行方式：**
```bash
# 启动服务器
python 05_full_agenta_style.py

# 或使用 uvicorn
uvicorn 05_full_agenta_style:app --reload
```

**测试端点：**
```bash
# /test 端点（传递配置）
curl -X POST http://localhost:8000/test \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "ag_config": {"model": "gpt-4"}}'

# /chat/test 端点
curl -X POST http://localhost:8000/chat/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi", "ag_config": {"model": "gpt-4"}}'

# 查看文档
open http://localhost:8000/docs
```

## 关键概念总结

### 1. 装饰器执行时机
```python
# 装饰器在**模块导入时**执行，而不是在函数调用时
@decorator
def func():
    pass

# 等价于：
# func = decorator(func)
# 这发生在 Python 解释器读取文件的瞬间
```

### 2. 类装饰器的工作原理
```python
@RouteDecorator("/")
def func():
    pass

# 执行流程：
# 1. RouteDecorator("/") 创建实例
# 2. 实例.__call__(func) 被调用
# 3. __call__ 返回的函数替换原函数
```

### 3. 多端点生成
```python
class RouteDecorator:
    def __call__(self, func):
        # 创建多个包装函数
        run_wrapper = ...
        test_wrapper = ...

        # 注册到全局 app
        app.post("/run")(run_wrapper)
        app.post("/test")(test_wrapper)

        return func

# 一个函数生成了两个端点！
```

### 4. 中间件管理
```python
_middleware_registered = False

def __call__(self, func):
    global _middleware_registered
    if not _middleware_registered:
        app.add_middleware(...)
        _middleware_registered = True
```

### 5. `/run` vs `/test` 的区别
| 特性 | `/run` | `/test` |
|------|--------|---------|
| 配置来源 | 预先配置的 deployment | 请求体中的 `ag_config` |
| 验证要求 | 必须验证配置 | 灵活，不严格验证 |
| 使用场景 | 生产环境 | 测试、评估、Playground |

## 与 serving.py 的对应关系

| 教程代码 | serving.py 代码 |
|---------|---------------|
| `app = FastAPI()` | 第 54 行：`app = FastAPI(...)` |
| `_middleware_registered` | 第 129 行：`_middleware = False` |
| `run_wrapper` | 第 164-185 行：`run_wrapper` |
| `test_wrapper` | 第 211-221 行：`test_wrapper` |
| `app.post("/run")` | 第 190-194 行：`app.post(run_route)` |
| `app.post("/test")` | 第 226-230 行：`app.post(test_route)` |
| `AuthMiddleware` | 第 25 行：`AuthHTTPMiddleware` |
| `ConfigMiddleware` | 第 26 行：`ConfigMiddleware` |

## 下一步

完成这些教程后，你应该能够：
1. ✅ 理解装饰器的基本概念和执行时机
2. ✅ 掌握类装饰器的工作原理
3. ✅ 理解如何在装饰器中自动注册端点
4. ✅ 理解 `/run` 和 `/test` 端点的不同行为
5. ✅ 理解 Agenta SDK 的整体架构

建议你：
1. 按顺序运行每个示例，观察输出
2. 修改代码，添加新的端点
3. 尝试添加新的包装函数（如 `/debug`）
4. 阅读真实的 `serving.py` 代码，对比理解

## 依赖安装

```bash
pip install fastapi uvicorn pydantic

