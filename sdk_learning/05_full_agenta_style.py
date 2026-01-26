"""
Lesson 5: 完整的 Agenta 风格实现
=================================

目标：最接近 serving.py 的实现，包括：
1. 全局 FastAPI app
2. 中间件管理（确保只注册一次）
3. OpenAPI schema 生成
4. 多个端点生成
5. 配置处理

这是最完整的教学示例！
"""

from functools import wraps
from typing import Dict, Optional

from fastapi import FastAPI, Request, HTTPException, Body
from pydantic import BaseModel, Field

# === 全局 FastAPI 应用 ===
app = FastAPI(
    title="Agenta SDK 学习示例 - 完整版",
    description="模拟 Agenta SDK 的装饰器和端点生成机制"
)


# === 中间件标志（确保只注册一次）===
_middleware_registered = False


class RouteDecorator:
    """
    路由装饰器 - Agenta 风格
    """

    def __init__(self, path="/", config_schema=None):
        self.path = path
        self.config_schema = config_schema
        print(f"📌 RouteDecorator.__init__(path='{path}')")

    def __call__(self, func):
        print(f"📌 RouteDecorator.__call__(func='{func.__name__}')")

        self.func = func

        # === 注册中间件（只注册一次）===
        global _middleware_registered
        if not _middleware_registered:
            print(f"  🔧 注册中间件...")
            self._register_middleware()
            _middleware_registered = True

        # === 创建包装函数 ===
        run_wrapper = self._create_run_wrapper(func)
        test_wrapper = self._create_test_wrapper(func)

        # === 注册端点 ===
        run_path = f"{self.path}/run" if self.path != "/" else "/run"
        test_path = f"{self.path}/test" if self.path != "/" else "/test"

        app.post(run_path)(run_wrapper)
        app.post(test_path)(test_wrapper)

        print(f"  ✅ 注册端点: POST {run_path}")
        print(f"  ✅ 注册端点: POST {test_path}\n")

        return func

    def _create_run_wrapper(self, func):
        """创建 /run 包装函数（生产模式）"""

        @wraps(func)
        async def wrapper(request: Request, **kwargs):
            print(f"\n🔵 [/run] 请求到达: {self.path}")

            # 生产模式：必须有配置
            config = getattr(request.state, 'config', None)
            if config is None:
                raise HTTPException(
                    status_code=400,
                    detail="生产模式(/run)需要预先配置的 deployment"
                )

            print(f"  🔵 配置: {config}")
            print(f"  🔵 参数: {kwargs}")
            result = await func(**kwargs)
            return result

        return wrapper

    def _create_test_wrapper(self, func):
        """创建 /test 包装函数（测试模式）"""

        @wraps(func)
        async def wrapper(request: Request, ag_config: Optional[Dict] = Body(None), **kwargs):
            print(f"\n🟢 [/test] 请求到达: {self.path}")

            # 测试模式：使用请求中的配置
            config = ag_config or {}
            request.state.config = config
            request.state.inline = True  # 标记为测试模式

            print(f"  🟢 配置: {config}")
            print(f"  🟢 参数: {kwargs}")
            result = await func(**kwargs)
            return result

        return wrapper

    def _register_middleware(self):
        """注册中间件"""
        app.add_middleware(AuthMiddleware)
        app.add_middleware(ConfigMiddleware)


# === 中间件实现 ===


class AuthMiddleware:
    """认证中间件"""

    async def __call__(self, request: Request, call_next):
        # 简单的认证检查
        auth_header = request.headers.get("authorization")

        if auth_header:
            request.state.auth = {"user": "test-user", "token": auth_header}
        else:
            request.state.auth = {"user": "anonymous"}

        print(f"    🔑 认证中间件: {request.state.auth['user']}")
        response = await call_next(request)
        return response


class ConfigMiddleware:
    """配置中间件"""

    async def __call__(self, request: Request, call_next):
        # /run 端点：从数据库或其他来源加载配置
        if request.url.path.endswith("/run"):
            # 模拟从 deployment 加载配置
            request.state.config = {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 1000
            }
            print(f"    ⚙️ 配置中间件: 加载生产配置")

        # /test 端点：配置由 test_wrapper 设置
        # 这里不做任何操作

        response = await call_next(request)
        return response


# === 配置 Schema 示例 ===


class GenerateConfig(BaseModel):
    """生成文本的配置"""
    model: str = Field(default="gpt-3.5-turbo", description="模型名称")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="温度参数")


class ChatConfig(BaseModel):
    """聊天的配置"""
    model: str = Field(default="gpt-4", description="模型名称")
    history_length: int = Field(default=10, ge=1, le=100, description="历史消息长度")


# === 使用装饰器定义端点 ===


@RouteDecorator("/", config_schema=GenerateConfig)
async def generate(prompt: str):
    """生成文本的入口点"""
    print(f"    📝 执行 generate: {prompt}")
    return {
        "message": f"Generated: {prompt}",
        "mode": "production",
        "status": "success"
    }


@RouteDecorator("/chat", config_schema=ChatConfig)
async def chat(message: str):
    """聊天的入口点"""
    print(f"    💬 执行 chat: {message}")
    return {
        "message": f"Chat reply: {message}",
        "mode": "production",
        "status": "success"
    }


# === 健康检查 ===


@app.get("/health")
def health():
    return {
        "status": "ok",
        "endpoints": ["/run", "/test", "/chat/run", "/chat/test"],
        "mode": "learning"
    }


@app.get("/")
def root():
    return {
        "message": "Agenta SDK 学习示例",
        "docs": "/docs",
        "endpoints": {
            "run": "/run (生产模式)",
            "test": "/test (测试模式)",
            "chat_run": "/chat/run (生产模式)",
            "chat_test": "/chat/test (测试模式)"
        }
    }


print("\n" + "="*60)
print("🚀 模块导入完成！FastAPI 应用已配置")
print("="*60)
print(f"\n📋 已注册的端点:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        methods = ', '.join(sorted(route.methods))
        print(f"  {methods:<10} {route.path}")

print("\n" + "="*60)
print("💡 启动服务器:")
print("   uvicorn 05_full_agenta_style:app --reload")
print("="*60)
print("📖 访问 http://localhost:8000/docs 查看完整 API 文档")
print("="*60 + "\n")


if __name__ == "__main__":
    import uvicorn

    print("🚀 启动 Uvicorn 服务器...\n")

    uvicorn.run(
        "05_full_agenta_style:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

