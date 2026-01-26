"""
Lesson 9: Python vs Java - 并发安全对比
=================================

目标：理解 Python 的全局变量模式在并发环境下的安全性
对比 Java 的类变量（静态变量）的并发行为
"""

import threading
import time
import asyncio


# ========================================
# Python 部分：全局变量并发问题
# ========================================

print("="*60)
print("📘 Python: 全局变量并发问题")
print("="*60 + "\n")


# === 情况 1: 没有并发控制（错误示范）===

print("❌ 情况 1: 全局变量没有并发控制")
print("-"*60 + "\n")

middleware_count_no_control = 0


class BadRouteDecorator:
    """错误的装饰器：没有并发控制"""

    def __call__(self, func):
        global middleware_count_no_control

        # 模拟多个装饰器同时调用
        # 注意：在真实场景中，这可能是多个模块导入
        # 但这里我们用线程模拟并发调用
        middleware_count_no_control += 1
        print(f"  📌 注册中间件 {middleware_count_no_control} 次（无控制）")
        return func


# 模拟并发注册
def simulate_concurrent_registration():
    """模拟并发场景"""
    print("模拟 3 个装饰器并发调用...")

    decorators = [
        BadRouteDecorator("/route1"),
        BadRouteDecorator("/route2"),
        BadRouteDecorator("/route3"),
    ]

    # 在单线程中，count 会递增到 3
    for decorator in decorators:
        decorator(lambda: None)

    print(f"最终计数: {middleware_count_no_control}\n")


# 模拟多线程并发
def simulate_concurrent_threads():
    """模拟多线程并发注册"""
    print("模拟 3 个线程并发注册中间件...")
    print("⚠️  在多线程环境中，可能出现竞态条件！\n")

    # 重置计数
    global middleware_count_no_control
    middleware_count_no_control = 0

    def worker(path):
        time.sleep(0.001)  # 模拟少量延迟
        BadRouteDecorator(path)(lambda: None)

    # 创建多个线程
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"/route{i}",))
        threads.append(t)

    # 同时启动所有线程
    for t in threads:
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    print(f"最终计数（多线程）: {middleware_count_no_control}")
    print("💡 结果：可能 > 3（如果线程交错执行）\n")


# === 情况 2: 有并发控制（正确示范）===

print("✅ 情况 2: 全局变量有并发控制")
print("-"*60 + "\n")

middleware_count_with_control = 0
middleware_lock = threading.Lock()


class GoodRouteDecorator:
    """正确的装饰器：有并发控制"""

    def __call__(self, func):
        global middleware_count_with_control
        global middleware_lock

        # 使用锁保证原子性
        with middleware_lock:
            if middleware_count_with_control == 0:  # 只允许第一个
                print(f"  📌 注册中间件 {middleware_count_with_control + 1} 次（有控制）")
                middleware_count_with_control = 1
            else:
                print(f"  ✅ 中间件已注册，跳过（当前计数: {middleware_count_with_control}）")

        return func


def simulate_safe_concurrent():
    """模拟安全的并发注册"""
    print("模拟 3 个线程并发注册中间件（有锁保护）...")

    # 重置计数
    global middleware_count_with_control
    middleware_count_with_control = 0

    def worker(path):
        time.sleep(0.001)  # 模拟少量延迟
        GoodRouteDecorator(path)(lambda: None)

    # 创建多个线程
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"/route{i}",))
        threads.append(t)

    # 同时启动所有线程
    for t in threads:
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    print(f"最终计数（多线程，有锁）: {middleware_count_with_control}")
    print("✅ 结果：总是 1（线程安全）\n")


# ========================================
# Java 部分：类变量并发问题
# ========================================

print("="*60)
print("☕ Java: 类变量（静态变量）并发问题")
print("="*60 + "\n")

java_code_example = """
// ====================================
// Java 版本：类变量（静态变量）
// ====================================

public class BadRouteDecorator {
    // ❌ 类变量（类似 Python 全局变量）
    private static int middlewareCount = 0;

    public Object decorate(Object func) {
        // 💥 问题：多个线程可能同时执行到这里
        // 可能的执行序列：
        // 线程1: 读取 middlewareCount = 0
        // 线程2: 读取 middlewareCount = 0  (竞态条件！)
        // 线程1: middlewareCount++ (= 1)
        // 线程2: middlewareCount++ (= 2)
        // 线程3: middlewareCount++ (= 3) ❌ 应该是 1

        middlewareCount++;
        System.out.println("注册中间件: " + middlewareCount + " 次");

        return func;
    }
}

// ====================================
// Java 版本：使用锁保证安全
// ====================================

public class GoodRouteDecorator {
    // 类变量 + 锁
    private static int middlewareCount = 0;
    private static final Object lock = new Object();  // 对象锁

    public Object decorate(Object func) {
        // ✅ 使用 synchronized 块保证原子性
        synchronized (lock) {
            if (middlewareCount == 0) {  // 只允许第一个
                middlewareCount++;
                System.out.println("注册中间件: " + middlewareCount);
            } else {
                System.out.println("中间件已注册，跳过");
            }
        }

        return func;
    }
}
"""

print("Java 错误示范：")
print(java_code_example.split("=== Java 版本")[0])
print(java_code_example.split("=== Java 版本")[1].split("// ====================================")[1].strip())
print(java_code_example.split("=== Java 版本")[1].split("// ====================================")[2].strip())
print()


# ========================================
# 对比总结
# ========================================

print("="*60)
print("📊 Python vs Java 并发对比总结")
print("="*60 + "\n")

comparison = """
| 特性 | Python (全局变量） | Java (类变量/静态变量） |
|------|-----------------|------------------------|
| 变量类型 | 模块级全局变量 | 类静态变量（static） |
| 默认可见性 | 模块内全局 | 类内全局 |
| 并发模型 | GIL (全局解释器锁）| 多线程 |
| 竞态条件风险 | ⭐⭐ (GIL 下较低） | ⭐⭐⭐⭐⭐ (高风险） |
| 原子操作 | CPython 中线程安全 | 不安全（需要 synchronized） |
| 读取-修改-写入 | 可能不一致 | 可能不一致 |
| 典型保护机制 | threading.Lock | synchronized 块 |
| 推荐模式 | 布尔标志 + Lock | volatile + synchronized |

并发安全问题详情：

Python 全局变量:
- CPython 有 GIL (全局解释器锁）
- GIL 在某些情况下提供"伪"保护
- 但多线程读写非原子操作仍可能不一致
- 需要显式使用 threading.Lock()

Java 类变量:
- 多个线程可以同时访问
- 没有自动保护机制
- ++ 操作不是原子的
- 必须使用 synchronized 或 volatile
"""

print(comparison)

print("\n" + "="*60)
print("💡 关键理解点")
print("="*60 + "\n")

key_points = """
1️⃣ 并发问题：
   - 多个线程同时检查条件
   - 可能都看到 count == 0
   - 可能都执行 count++
   - 结果：count = N (应该是 1)

2️⃣ 竞态条件：
   - 当多个线程同时修改共享状态时
   - 结果取决于线程调度顺序
   - 导致不可预测的行为

3️⃣ 保护机制：

   Python:
   - threading.Lock() 互斥锁
   - with lock: 块保证原子性
   - 原子操作（+=, -=）在锁内安全

   Java:
   - synchronized 块
   - volatile 关键字（可见性）
   - AtomicInteger (原子操作）

4️⃣ Python GIL 的作用：
   - CPython 有全局解释器锁（GIL）
   - 在某些情况下"保护"全局变量
   - 但不能完全避免竞态条件
   - GIL 主要保护 Python 对象操作
   - 不保证多步操作的原子性
   - 例如：if not count: count += 1 (两步操作）

5️⃣ 为什么 Agenta 模式可行：
   - 模块导入通常是单线程的
   - Python 的 import 机制有锁保护
   - 在模块导入时执行，并发风险低
   - 即使多线程导入，布尔标志 + 检查也较安全
"""

print(key_points)

print("\n" + "="*60)
print("🔄 推荐方案")
print("="*60 + "\n")

print("""
方案 1: 单例模式 + 锁

Python:
    class Singleton:
        _instance = None
        _lock = threading.Lock()

        @classmethod
        def get_instance(cls):
            if cls._instance is None:
                with cls._lock:
                    if cls._instance is None:
                        cls._instance = cls()
            return cls._instance

Java:
    public class Singleton {
        private static volatile Singleton instance;

        public static Singleton getInstance() {
            if (instance == null) {
                synchronized (Singleton.class) {
                    if (instance == null) {
                        instance = new Singleton();
                    }
                }
            }
            return instance;
        }
    }


方案 2: 原子标志（Agenta 模式）

Python:
    _middleware_registered = False  # 👈 简单有效

    # 适用于：
    # - 模块导入通常是单线程
    # - 即使并发，if + 标记也较安全
    # - GIL 提供一定保护

    # 可选增强：
    _middleware_lock = threading.Lock()  # 👈 完全线程安全

Java:
    // 简单标志不够安全，必须用 synchronized
    private static boolean middlewareRegistered = false;

    public void register() {
        synchronized (this.getClass()) {
            if (!middlewareRegistered) {
                // 注册逻辑
                middlewareRegistered = true;
            }
        }
    }
""")


# ========================================
# 实际测试
# ========================================

print("\n" + "="*60)
print("🧪 运行测试")
print("="*60 + "\n")

print("选择要运行的测试：")
print("1. Python 单线程（安全）")
print("2. Python 多线程（错误示范）")
print("3. Python 多线程（正确示范）\n")

choice = input("输入选项 (1/2/3, 默认 1): ").strip() or "1"

if choice == "1":
    print("\n测试 1: Python 单线程")
    simulate_concurrent_registration()

elif choice == "2":
    print("\n测试 2: Python 多线程（无控制）")
    simulate_concurrent_threads()

elif choice == "3":
    print("\n测试 3: Python 多线程（有锁控制）")
    simulate_safe_concurrent()
else:
    print("无效选项，运行测试 1...")
    simulate_concurrent_registration()

print("\n" + "="*60)
print("✅ 测试完成")
print("="*60 + "\n")

print("""
💡 观察 Python GIL 的影响：

CPython (标准 Python 实现) 有 GIL：
- GIL 在单线程中保护全局变量
- GIL 在多线程中提供有限保护
- 但不能完全避免竞态条件

其他实现 (Jython, IronPython) 没有 GIL：
- 多线程访问全局变量完全并发
- 必须使用锁保证安全

Jython/Jython (运行在 JVM):
- 更接近 Java 的行为
- 需要使用显式锁机制

结论：
- Python 全局变量 + GIL > Java 静态变量
- 但最佳实践仍是使用锁
- Agenta 的模式在模块导入场景下是可接受的
""")


if __name__ == "__main__":
    main()

