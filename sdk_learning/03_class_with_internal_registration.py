"""
Lesson 3: 类装饰器在内部注册路由
=================================

目标：理解 Agenta SDK 如何在装饰器执行时自动注册端点

在 serving.py 中，entrypoint 类的 __init__ 方法会：
1. 创建多个包装函数（run_wrapper, test_wrapper）
2. 将这些包装函数注册到全局的 FastAPI app

这一课演示这个原理。
"""


# 模拟一个简单的路由表
class SimpleRouter:
    """
    简单的路由器，模拟 FastAPI
    """
    def __init__(self):
        self.routes = {}  # 存储路径 -> 函数的映射

    def add_route(self, path, method, func):
        """注册路由"""
        key = f"{method.upper()} {path}"
        self.routes[key] = func
        print(f"✅ [导入时] 注册路由: {key} -> {func.__name__}")


# 创建全局路由器实例（相当于 Agenta SDK 的全局 app）
app = SimpleRouter()


class RouteDecorator:
    """
    路由装饰器 - 会自动向全局 app 注册多个端点
    """

    def __init__(self, path="/"):
        self.path = path
        print(f"📌 RouteDecorator.__init__(path='{path}')")

    def __call__(self, func):
        print(f"📌 RouteDecorator.__call__(func='{func.__name__}')")

        # 保存原函数
        self.func = func

        # === 创建 /run 包装函数 ===
        def run_wrapper(*args, **kwargs):
            print(f"  🔵 [/run] 执行: {func.__name__}")
            print(f"  🔵 [/run] 生产模式：需要预先配置")
            result = self.func(*args, **kwargs)
            return result

        # === 创建 /test 包装函数 ===
        def test_wrapper(*args, **kwargs):
            print(f"  🟢 [/test] 执行: {func.__name__}")
            print(f"  🟢 [/test] 测试模式：灵活配置")
            result = self.func(*args, **kwargs)
            return result

        # === 注册到全局 app ===
        run_path = f"{self.path}/run" if self.path != "/" else "/run"
        test_path = f"{self.path}/test" if self.path != "/" else "/test"

        app.add_route(run_path, "POST", run_wrapper)
        app.add_route(test_path, "POST", test_wrapper)

        print(f"  📝 为 {func.__name__} 创建了 2 个端点")

        return func  # 返回原函数


# 使用装饰器
@RouteDecorator("/")
def generate_text(prompt):
    """生成文本的函数"""
    print(f"    📝 生成文本: {prompt}")


@RouteDecorator("/summarize")
def summarize_text(text):
    """摘要文本的函数"""
    print(f"    📄 摘要: {text}")


print("\n" + "="*60)
print("🚀 模块导入完成！路由已自动注册。")
print("="*60)
print(f"\n📋 当前注册的路由:")
for path, func in app.routes.items():
    print(f"  {path} -> {func.__name__}")

print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print("📞 开始调用端点...\n")

    # 模拟调用 /run 端点
    print("🔵 调用 POST /run")
    app.routes["POST /run"]("Hello world")

    print()

    # 模拟调用 /test 端点
    print("🟢 调用 POST /test")
    app.routes["POST /test"]("Hello world")

    print()

    # 模拟调用 /summarize/run 端点
    print("🔵 调用 POST /summarize/run")
    app.routes["POST /summarize/run"]("This is a long text...")

    print()

    # 模拟调用 /summarize/test 端点
    print("🟢 调用 POST /summarize/test")
    app.routes["POST /summarize/test"]("This is a long text...")

    print("\n💡 关键理解点：")
    print("1. 装饰器在导入时自动注册路由（无需手动调用）")
    print("2. 一个函数可以生成多个端点（/run 和 /test）")
    print("3. 每个端点有不同的包装函数（不同的行为）")
    print("4. 这就是 Agenta SDK 的核心机制！")

