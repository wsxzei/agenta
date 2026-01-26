"""
Lesson 1: 最简单的装饰器
=================================

目标：理解装饰器的基本概念和执行时机

装饰器本质上是一个函数，它接收另一个函数作为参数，
并返回一个新的函数（或者原函数）。

执行时机：
- 装饰器在**模块导入时**就会执行，而不是在函数被调用时
"""


def my_decorator(func):
    """简单的装饰器"""
    print(f"📌 [导入时] 装饰器正在包装函数: {func.__name__}")

    def wrapper(*args, **kwargs):
        print(f"🔔 [调用时] 函数 {func.__name__} 被调用了！")
        result = func(*args, **kwargs)
        print(f"✅ [调用时] 函数 {func.__name__} 执行完成, 返回结果 {result}")
        return result

    return wrapper


@my_decorator  # Python 会立即执行：my_decorator(say_hello)
def say_hello(name):
    """被装饰的函数"""
    print(f"  👋 你好，{name}！")


@my_decorator
def say_goodbye(name):
    """另一个被装饰的函数"""
    print(f"  👋 再见，{name}！")


print("\n" + "="*60)
print("🚀 模块导入完成！装饰器已经在导入时执行了。")
print("="*60 + "\n")

if __name__ == "__main__":
    print("📞 开始调用函数...\n")

    say_hello("张三")
    print()
    say_goodbye("李四")

    print("\n💡 关键理解点：")
    print("1. 装饰器在模块导入时执行（看到上面的 '📌' 输出）")
    print("2. 函数在调用时执行（看到上面的 '🔔' 输出）")
    print("3. 装饰器返回的 wrapper 函数替换了原函数")

