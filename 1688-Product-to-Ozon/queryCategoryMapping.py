#!/usr/bin/env python3
"""

查询1688的类目映射到Ozon的类目的情况

"""

import json
import sys

import requests

# === 常量 ===
CATEGORY_MAPPING_URL = "https://crossborder-core.1688.com/openclaw/queryCategoryMapping"
CATEGORY_MAPPING_TOKEN = "soisrgd124ghdfnp"


def log(msg: str, level: str = "INFO"):
    print(f"[{level}] {msg}")


def error_exit(msg: str):
    log(msg, "ERROR")
    exit(1)

def success_info(msg: str):
    log(msg, "SUCCESS")

def query_category_mapping(category_id: str) -> dict:
    """调用1688接口查询Ozon类目映射"""
    log(f"查询类目映射: 1688 categoryId={category_id}")
    try:
        resp = requests.post(
            CATEGORY_MAPPING_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CATEGORY_MAPPING_TOKEN}",
            },
            json={"categoryId": str(category_id)},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        log(f"类目映射响应: {json.dumps(data, ensure_ascii=False)[:500]}")
        return data
    except Exception as e:
        error_exit(f"查询类目映射失败: {e}")


def main(category_id: str = None, **kwargs) -> str:
    """
    主入口函数 - OpenClaw SKILL 调用此函数

    OpenClaw 框架会将大模型提取的类目数据作为参数传入。

    Args:
        category_id: 类目数据，是从1688的商品数据中提取出来thirdCategoryId，代表1688的商品的叶子类目，参数是数字的形式

    Returns:
        str: JSON格式的处理结果字符串（OpenClaw要求返回字符串）
    """
    if category_id is None:
        error_exit("类目数据为空")
    result = query_category_mapping(category_id)
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行传参
        result = main(sys.argv[1])
    else:
        # 使用测试数据
        error_exit("该1688商品数据无有效类目数据，执行失败")

    log(f"执行结果:{result}")
