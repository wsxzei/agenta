"""
Lesson 6: uvicorn.run 的 app 参数类型
=================================

目标：理解 uvicorn.run 方法支持的所有 app 参数类型及其用法

uvicorn.run 是一个非常灵活的方法，支持多种方式传入应用对象。
"""

from fastapi import FastAPI, APIRouter

# === 方式 1: 字符串格式（推荐）===

app1 = FastAPI(title="方式1: 字符串格式")

print("✅ 方式 1: 字符串格式")
print("   uvicorn.run('06_uvicorn_app_types:app1')")
print("   特点: 支持热重载，最佳实践\n")


# === 方式 2: ASGI 应用对象 ===

app2 = FastAPI(title="方式2: ASGI 对象")

print("✅ 方式 2: 直接传入 ASGI 对象")
print("   uvicorn.run(app2, ...)")
print("   特点: 简单直接，但无热重载\n")


# === 方式 3: ASGI 可调用对象（Callable）===

async def asgi_callable(scope, receive, send):
    """自定义 ASGI 应用（可调用对象）
    scope: 字典包含请求的元数据，包含类型、路径、headers等关键信息, 应用需要能处理不同类型的 scope
    receive: 异步接收端，用于获取客户端发送的数据
    send: 异步发送端，用于向客户端发送响应数据
    """
    # ASGI 协议的三个参数
    print(f"ASGI 请求: {scope['type']}")

    # 简单响应
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'text/plain']],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello from ASGI callable!',
    })


print("✅ 方式 3: ASGI 可调用对象（Callable）")
print("   uvicorn.run(asgi_callable, ...)")
print("   特点: 原生 ASGI 应用，无需框架\n")


# === 方式 4: 导入的模块应用 ===

# 注意：这个应用会在运行时导入
module_app = None

def get_module_app():
    """延迟导入的应用"""
    global module_app
    if module_app is None:
        from fastapi import FastAPI
        module_app = FastAPI(title="方式4: 模块导入")
    return module_app


print("✅ 方式 4: 导入的模块应用")
print("   app = importlib.import_module('module').app")
print("   uvicorn.run(app, ...)")
print("   特点: 动态导入，灵活控制加载时机\n")


# === 方式 5: 工厂函数（返回 ASGI 应用）===

def app_factory():
    """应用工厂函数"""
    app = FastAPI(title="方式5: 工厂函数")

    @app.get("/")
    def root():
        return {"message": "Factory app created"}

    return app


print("✅ 方式 5: 工厂函数")
print("   uvicorn.run(app_factory, ...)")
print("   特点: 支持应用创建时的参数配置\n")


# === 方式 6: APIRouter 对象 ===

router = APIRouter(prefix="/api")

@router.get("/test")
def test_route():
    return {"message": "Router app"}


print("✅ 方式 6: APIRouter 对象")
print("   uvicorn.run(router, ...)")
print("   特点: 可以直接使用 Router 作为应用\n")


# === 对比示例 ===

print("\n" + "="*60)
print("📊 uvicorn.run 的 app 参数类型对比")
print("="*60 + "\n")

examples = [
    {
        "类型": "字符串 (String)",
        "示例": "uvicorn.run('main:app')",
        "热重载": "✅ 支持",
        "说明": "最佳实践，自动重新加载模块",
        "使用场景": "开发环境、生产部署"
    },
    {
        "类型": "ASGI 对象 (ASGI Instance)",
        "示例": "uvicorn.run(app)",
        "热重载": "❌ 不支持",
        "说明": "直接传入应用实例",
        "使用场景": "简单脚本、测试"
    },
    {
        "类型": "ASGI 可调用 (ASGI Callable)",
        "示例": "async def app(scope, receive, send): ...",
        "热重载": "❌ 不支持",
        "说明": "原生 ASGI 协议实现",
        "使用场景": "自定义 ASGI 中间件"
    },
    {
        "类型": "工厂函数 (Factory Function)",
        "示例": "def create_app(): return FastAPI()",
        "热重载": "❌ 不支持",
        "说明": "每次调用返回新的应用实例",
        "使用场景": "测试、多实例"
    },
    {
        "类型": "模块引用 (Module Reference)",
        "示例": "import main; uvicorn.run(main.app)",
        "热重载": "❌ 不支持",
        "说明": "预导入的模块对象",
        "使用场景": "多应用管理"
    },
]

# 打印对比表格
max_type_len = max(len(ex["类型"]) for ex in examples)
max_example_len = max(len(ex["示例"]) for ex in examples)

print(f"{'类型':<{max_type_len}} | {'示例':<{max_example_len}} | 热重载 | 说明")
print("-" * (max_type_len + max_example_len + 50))

for ex in examples:
    print(
        f"{ex['类型']:<{max_type_len}} | "
        f"{ex['示例']:<{max_example_len}} | "
        f"{ex['热重载']:<8} | "
        f"{ex['说明']}"
    )

print("\n" + "="*60)
print("💡 推荐使用方式")
print("="*60 + "\n")

print("1️⃣  开发环境:")
print("   ✅ 使用字符串格式: uvicorn.run('main:app', reload=True)")
print("   原因: 支持热重载，代码修改自动生效\n")

print("2️⃣  生产环境:")
print("   ✅ 使用字符串格式: uvicorn.run('main:app')")
print("   或使用 Gunicorn: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker")
print("   原因: 标准部署方式，易于监控和管理\n")

print("3️⃣  测试环境:")
print("   ✅ 使用工厂函数或直接对象: uvicorn.run(app)")
print("   原因: 简单直接，无需模块导入\n")

print("4️⃣  Docker 部署:")
print("   ✅ 使用字符串格式:")
print('   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]')
print("   原因: 与开发环境一致，支持多进程\n")

print("\n" + "="*60)
print("📚 其他 uvicorn.run 参数示例")
print("="*60 + "\n")

print("基本的 uvicorn.run 使用:")
print("""
uvicorn.run(
    app="main:app",              # 应用对象
    host="0.0.0.0",            # 监听地址
    port=8000,                   # 监听端口
    reload=True,                  # 开发模式：热重载
    log_level="info",             # 日志级别
    access_log=True,             # 访问日志
    use_colors=True,             # 彩色日志
    loop="uvloop",              # 事件循环类型（可选）
    http="httptools",           # HTTP 实现类型（可选）
    workers=4,                  # 工作进程数（生产环境）
)
""")

print("🚀 要测试不同的方式，请运行:")
print("   python 06_uvicorn_app_types.py")
print("\n   然后取消注释下面的某个方式来启动服务器\n")

# print("\n" + "="*60)
# print("🔥 启动服务器（测试方式 1: 字符串格式）")
# print("="*60 + "\n")
#
# uvicorn.run(
#     "06_uvicorn_app_types:app1",
#     host="0.0.0.0",
#     port=8000,
#     reload=True
# )

