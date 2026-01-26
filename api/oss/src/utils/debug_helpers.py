import json
import logging
from pprint import pformat
from typing import Any, Dict

# 获取模块日志记录器
log = logging.getLogger(__name__)


def debug_obj(obj: Any, name: str = "object", max_depth: int = 3, current_depth: int = 0) -> Dict:
    """
    详细的对象调试函数，可以打印对象的详细信息

    Args:
        obj: 要调试的对象
        name: 对象名称
        max_depth: 最大递归深度
        current_depth: 当前深度

    Returns:
        Dict: 包含对象信息的字典
    """
    if current_depth >= max_depth:
        return {"type": "max_depth_reached", "repr": str(obj)}

    obj_info = {
        "name": name,
        "type": type(obj).__name__,
        "module": getattr(type(obj), "__module__", None),
        "attributes": list(dir(obj)),
        "current_depth": current_depth
    }

    try:
        # 处理字典类型
        if isinstance(obj, dict):
            obj_info["size"] = len(obj)
            obj_info["keys"] = list(obj.keys())
            if current_depth < max_depth - 1:
                obj_info["values"] = {k: debug_obj(v, f"{name}.{k}", max_depth, current_depth + 1)
                                     for k, v in list(obj.items())[:10]}  # 限制输出数量
            else:
                obj_info["sample_values"] = {k: type(v).__name__ for k, v in list(obj.items())[:5]}

        # 处理列表类型
        elif isinstance(obj, (list, tuple)):
            obj_info["size"] = len(obj)
            obj_info["sample_types"] = [type(item).__name__ for item in obj[:3]]
            if current_depth < max_depth - 1 and obj:
                obj_info["sample_items"] = [debug_obj(item, f"{name}[{i}]", max_depth, current_depth + 1)
                                          for i, item in enumerate(obj[:2])]

        # 处理Pydantic模型
        elif hasattr(obj, "model_fields") or hasattr(obj, "__fields__"):
            try:
                obj_info["model_fields"] = list(getattr(obj, "model_fields", {}).keys())
                obj_info["model_dump"] = debug_obj(obj.model_dump() if hasattr(obj, "model_dump") else obj.dict(),
                                                   f"{name}.dump", max_depth, current_depth + 1)
            except Exception as e:
                obj_info["model_error"] = str(e)

        # 处理具有__dict__的对象
        elif hasattr(obj, "__dict__"):
            obj_info["attributes"] = list(obj.__dict__.keys())
            if current_depth < max_depth - 1:
                obj_info["attr_sample"] = debug_obj(obj.__dict__, f"{name}.__dict__", max_depth, current_depth + 1)

        # 基础类型
        else:
            try:
                obj_info["value"] = str(obj)
                obj_info["repr"] = repr(obj)
                if isinstance(obj, (str, bytes)):
                    obj_info["length"] = len(obj)
                if isinstance(obj, (int, float)):
                    obj_info["bytes"] = obj.__sizeof__()
            except Exception as e:
                obj_info["value_error"] = str(e)

    except Exception as e:
        obj_info["error"] = f"Failed to analyze object: {e}"

    return obj_info

def log_object(obj: Any, name: str = "object", logger=None, max_depth: int = 3):
    """
    在日志中打印对象的详细信息

    Args:
        obj: 要记录的对象
        name: 对象名称
        logger: 日志记录器实例
        max_depth: 最大递归深度
    """
    if logger is None:
        logger = log

    obj_info = debug_obj(obj, name, max_depth)
    logger.info(f"Object debug info for {name}:\n{pformat(obj_info)}")

def safe_json_serialize(obj: Any, indent: int = 2) -> str:

    """
    安全的JSON序列化，处理复杂的Python对象
    """
    def serialize_fallback(o):
        if hasattr(o, "model_dump"):
            return o.model_dump()
        elif hasattr(o, "dict"):
            return o.dict()
        elif hasattr(o, "__dict__"):
            return str(o.__dict__)
        else:
            return str(o)

    try:
        return json.dumps(obj, default=serialize_fallback, ensure_ascii=False, indent=indent)
    except Exception as e:
        return f"Failed to serialize object: {e}, type: {type(obj)}"

class ObjectDebugger:
    """
    对象调试器类，用于在运行时检查对象
    """
    @staticmethod
    def inspect_response(response_data: Any, context: str = ""):
        """
        专门用于检查API响应的调试函数
        """
        log.info(f"=== API Response Debug {context} ===")

        if isinstance(response_data, dict):
            log.info(f"Response keys: {list(response_data.keys())}")

            # 特别检查常见字段
            for key in ["error", "detail", "message", "data", "trace"]:
                if key in response_data:
                    log.info(f"Response {key}: {safe_json_serialize(response_data[key])}")

        log.info(f"Full response: {safe_json_serialize(response_data)}")
        log.info(f"=== End API Response Debug ===")

    @staticmethod
    def inspect_variables(**kwargs):
        """
        批量检查多个变量

        Usage:
        ObjectDebugger.inspect_variables(
            response=app_response,
            payload=payload,
            status_code=response.status_code
        )
        """
        for name, value in kwargs.items():
            log_object(value, name, max_depth=2)

    @staticmethod
    def inspect_object(obj: Any, name: str = "object", max_depth: int = 3) -> Dict:
        return log_object(obj, name, max_depth=max_depth)
