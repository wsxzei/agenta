"""
Lesson 2: 类装饰器
=================================

目标：理解 Agenta SDK 中使用 @ag.route 这样的类装饰器

在 serving.py 中：
    @ag.route("/")
    async def generate(...):

这里 ag.route 是一个类，而不是函数！
类作为装饰器时，需要实现 __call__ 方法。
"""


class RouteDecorator:
    """
    类装饰器 - 类似 Agenta SDK 中的 @ag.route
    """

    def __init__(self, path="/"):
        """
        当 @RouteDecorator("/") 执行时，会调用 __init__
        参数是装饰器的括号中的内容
        """
        self.path = path
        print(f"📌 [导入时] RouteDecorator.__init__ 被调用，path = '{path}'")

    def __call__(self, func):
        """
        当装饰器应用到函数时，会调用 __call__
        参数是被装饰的函数
        """
        print(f"📌 [导入时] RouteDecorator.__call__ 被调用，函数 = '{func.__name__}'")

        # 保存被装饰的函数
        self.func = func

        # 返回包装后的函数（或原函数）
        def wrapper(*args, **kwargs):
            print(f"\n🔔 [调用时] 调用端点: {self.path}")
            print(f"🔔 [调用时] 执行函数: {self.func.__name__}")
            result = self.func(*args, **kwargs)
            print(f"✅ [调用时] 函数执行完成\n")
            return result

        return wrapper


# 使用类装饰器
@RouteDecorator("/hello")
def hello_world():
    """被装饰的函数"""
    print("  👋 Hello, World!")


@RouteDecorator("/user/create")
def create_user(name):
    """另一个被装饰的函数"""
    print(f"  👤 创建用户: {name}")


print("\n" + "="*60)
print("🚀 模块导入完成！")
print("="*60 + "\n")

if __name__ == "__main__":
    print("📞 开始调用函数...\n")

    hello_world()
    create_user("张三")

    # print("\n💡 关键理解点：")
    # print("1. @RouteDecorator('/hello') 执行流程：")
    # print("   a. RouteDecorator('/') 创建实例")
    # print("   b. 实例.__call__(hello_world) 装饰函数")
    # print("   c. 返回的 wrapper 替换原函数")
    # print("2. 这就是 Agenta SDK 中 @ag.route 的原理！")

