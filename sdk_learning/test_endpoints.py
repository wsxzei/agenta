"""
测试脚本 - 测试 Lesson 5 的完整实现
=================================

使用这个脚本来测试 Lesson 5 中创建的端点。
"""

import json

import requests

BASE_URL = "http://localhost:8000"


def print_section(title):
    """打印分隔线"""
    print("\n" + "="*60)
    print(title)
    print("="*60 + "\n")


def test_endpoint(method, path, data=None, headers=None):
    """测试端点"""
    url = f"{BASE_URL}{path}"
    print(f"📡 {method} {url}")

    if data:
        print(f"📦 请求体: {json.dumps(data, indent=2, ensure_ascii=False)}")

    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError(f"不支持的 HTTP 方法: {method}")

        print(f"📊 状态码: {response.status_code}")

        if response.status_code == 200:
            print(f"✅ 响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 错误: {response.text}")

        return response

    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：请确保服务器正在运行")
        print(f"   启动命令: python 05_full_agenta_style.py")
        return None


def main():
    """主测试函数"""

    print_section("🏥 健康检查")
    test_endpoint("GET", "/health")

    print_section("📄 根路径")
    test_endpoint("GET", "/")

    print_section("🟢 测试 /test 端点（不需要配置）")
    test_endpoint(
        "POST",
        "/test",
        data={"prompt": "Hello, Agenta!"}
    )

    print_section("🟢 测试 /test 端点（带配置）")
    test_endpoint(
        "POST",
        "/test",
        data={
            "prompt": "Hello with config",
            "ag_config": {
                "model": "gpt-4",
                "temperature": 0.9
            }
        }
    )

    print_section("🔵 测试 /run 端点（应该成功，有中间件配置）")
    test_endpoint(
        "POST",
        "/run",
        data={"prompt": "Production mode"}
    )

    print_section("🟢 测试 /chat/test 端点")
    test_endpoint(
        "POST",
        "/chat/test",
        data={
            "message": "Let's chat!",
            "ag_config": {
                "model": "gpt-4",
                "history_length": 20
            }
        }
    )

    print_section("🔵 测试 /chat/run 端点")
    test_endpoint(
        "POST",
        "/chat/run",
        data={"message": "Chat in production"}
    )

    print_section("🔐 测试认证中间件")
    test_endpoint(
        "POST",
        "/test",
        data={"prompt": "With auth"},
        headers={"Authorization": "Bearer test-token"}
    )

    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)
    print("\n💡 提示：")
    print("1. 查看 /docs 页面获取完整的 API 文档")
    print("2. 修改代码后观察服务器的 reload 行为")
    print("3. 尝试添加新的端点测试你的理解")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

