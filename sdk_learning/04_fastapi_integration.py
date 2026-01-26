"""
Lesson 4: 集成 FastAPI - 完整示例
=================================

目标：使用真实的 FastAPI，模拟 Agenta SDK 的完整机制

这个示例最接近 serving.py 的实际实现！
"""

from functools import wraps

from fastapi import FastAPI, Request, HTTPException

# === 创建全局 FastAPI 应用 ===
app = FastAPI(title="Agenta SDK 学习示例")


class RouteDecorator:
    """
    路由装饰器 - 完整版本
    """

    def __init__(self, path="/"):
        self.path = path
        print(f"📌 RouteDecorator.__init__(path='{path}')")

    def __call__(self, func):
        print(f"📌 RouteDecorator.__call__(func='{func.__name__}')")

        self.func = func

        # === 创建 /run 包装函数（生产模式）===
        # 💡 @wraps(func) 解释：
        #    - wraps 是 functools 模块的一个装饰器
        #    - 它会将被装饰函数（func）的元数据（如 __name__, __doc__）复制到包装函数
        #    - 这样包装函数看起来就像原函数一样
        #    - 示例：
        #        @wraps(func)
        #        def wrapper():
        #            # wrapper.__name__ == func.__name__ (不是 'wrapper')
        @wraps(func)
        async def run_wrapper(request: Request):
            print(f"  🔵 [/run] 请求到达: {self.path}")

            # 模拟：检查是否配置了 deployment
            if not hasattr(request.state, 'deployment_config'):
                raise HTTPException(
                    status_code=400,
                    detail="生产模式需要预先配置 deployment"
                )

            print(f"  🔵 [/run] 使用配置: {request.state.deployment_config}")
            result = await func(request)
            return result

        # === 创建 /test 包装函数（测试模式）===
        @wraps(func)
        async def test_wrapper(request: Request):
            print(f"  🟢 [/test] 请求到达: {self.path}")
            print(f"  🟢 [/test] 测试模式：接受任意配置")
            result = await func(request)
            return result

        # === 注册到 FastAPI app ===
        run_path = f"{self.path}/run" if self.path != "/" else "/run"
        test_path = f"{self.path}/test" if self.path != "/" else "/test"

        # 💡 app.post(run_path)(run_wrapper) 解释：
        #    这是 FastAPI 的链式调用语法，可以分解为两个步骤：
        #
        #    步骤 1: app.post(run_path) 创建一个装饰器
        #        - 返回一个装饰器函数 Callable[[DecoratedCallable], DecoratedCallable]
        #        - 这个装饰器会为指定路径注册路由
        #
        #    步骤 2: (run_wrapper) 应用装饰器到函数
        #        - 将 run_wrapper 函数作为处理函数
        #        - 完成 POST {run_path} -> run_wrapper 的映射
        #
        #    等价写法：
        #        decorator = app.post(run_path)
        #        decorator(run_wrapper)
        #
        #    这意味着：当收到 POST 请求到 {run_path} 时，调用 run_wrapper
        #
        #    示例：
        #        app.post("/run")(run_wrapper)
        #        # 请求: POST http://localhost:8000/run
        #        # 处理: run_wrapper(request)
        app.post(run_path)(run_wrapper)
        app.post(test_path)(test_wrapper)

        print(f"  ✅ 注册端点: POST {run_path}")
        print(f"  ✅ 注册端点: POST {test_path}\n")

        return func


# === 使用装饰器定义端点 ===


@RouteDecorator("/")
async def generate(request: Request):
    """生成文本的入口点"""
    return {"message": "Hello from generate!", "status": "success"}


@RouteDecorator("/chat")
async def chat(request: Request):
    """聊天的入口点"""
    return {"message": "Hello from chat!", "status": "success"}


# === 添加中间件（模拟配置处理）===


@app.middleware("http")
async def add_config_middleware(request: Request, call_next):
    """
    中间件：根据请求路径添加不同的配置
    """
    # /run 端点需要预先配置的 deployment
    if request.url.path.endswith("/run"):
        # request.state是一个property装饰的方法，返回State对象
        request.state.deployment_config = {
            "model": "gpt-4",
            "temperature": 0.7
        }
    # /test 端点不需要预设配置
    # request.state 保持为空

    response = await call_next(request)
    return response


# === 健康检查端点 ===


@app.get("/health")
def health():
    return {"status": "ok"}


print("\n" + "="*60)
print("🚀 模块导入完成！FastAPI 应用已配置")
print("="*60)
print(f"\n📋 可用端点:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        methods = ', '.join(route.methods)
        print(f"  {methods} {route.path}")

print("\n" + "="*60)
print("💡 启动服务器:")
print("   uvicorn 04_fastapi_integration:app --reload")
print("="*60 + "\n")


if __name__ == "__main__":
    import uvicorn

    print("🚀 启动 Uvicorn 服务器...")
    print("🌐 访问 http://localhost:8000/docs 查看 API 文档\n")

    # 💡 uvicorn.run("04_fastapi_integration:app", ...) 解释：
    #    这是 Python 的"模块导入语法"，格式为："模块名:对象名"
    #
    #    1. "04_fastapi_integration:app" 的含义：
    #       - "04_fastapi_integration" 是 Python 模块名（文件名，不带 .py）
    #       - "app" 是该模块中要导入的对象名（全局 FastAPI 实例）
    #       - 冒号 ":" 分隔模块名和对象名
    #
    #    2. 为什么不直接传递 app 对象？
    #       - uvicorn.run("04_fastapi_integration:app") 允许 uvicorn 自动重新加载
    #       - 当文件修改时，uvicorn 会重新导入模块，获取最新的 app
    #       - 如果直接传 app 对象，无法实现热重载
    #
    #    3. 执行流程：
    #       a. uvicorn 读取字符串 "04_fastapi_integration:app"
    #       b. 导入模块: import 04_fastapi_integration
    #       c. 获取对象: module.app
    #       d. 使用 app 启动 ASGI(Asynchronous Server Gateway Interface) 服务器
    #
    #    4. 等价写法：
    #       uvicorn.run(app, host="0.0.0.0", port=8000)  # ❌ 无热重载
    #       uvicorn.run("04_fastapi_integration:app", ...)  # ✅ 支持热重载
    #
    #    5. 常见格式：
    #       - "文件名:变量名"
    #       - "包名.模块名:变量名"
    #       - 示例: "myapp.main:app"
    uvicorn.run(
        "04_fastapi_integration:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

