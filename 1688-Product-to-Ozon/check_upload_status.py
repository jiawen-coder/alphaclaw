#!/usr/bin/env python3
"""
Ozon商品上传状态查询器
通过Ozon API v1/product/import/info接口查询上传任务状态
简化版本：只要状态是imported就认为成功，不尝试自动修复问题
"""

import os
import json
import sys
import requests
from typing import Dict, Any, Optional


class OzonStatusChecker:
    def __init__(self, client_id: str, api_key: str):
        """
        初始化Ozon状态查询器

        Args:
            client_id: Ozon API Client ID
            api_key: Ozon API Key
        """
        self.client_id = client_id
        self.api_key = api_key
        self.base_url = "https://api-seller.ozon.ru"

    def create_headers(self) -> Dict[str, str]:
        """
        创建API请求头

        Returns:
            Dict[str, str]: 请求头字典
        """
        return {
            'Client-Id': self.client_id,
            'Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def check_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        查询上传任务状态

        Args:
            task_id: 任务ID

        Returns:
            Dict: 任务状态信息，失败时返回None
        """
        url = f"{self.base_url}/v1/product/import/info"

        payload = {
            "task_id": int(task_id)
        }

        try:
            response = requests.post(
                url,
                headers=self.create_headers(),
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                print(f"❌ 查询任务状态失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求错误: {e}")
            return None
        except ValueError as e:
            print(f"❌ 任务ID格式错误: {e}")
            return None


def load_config() -> tuple:
    """从环境变量加载配置"""
    client_id = os.getenv('OZON_CLIENT_ID')
    api_key = os.getenv('OZON_API_KEY')

    if not client_id or not api_key:
        print("❌ 请设置环境变量 OZON_CLIENT_ID 和 OZON_API_KEY")
        sys.exit(1)

    return client_id, api_key


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("❌ 用法: python check_status.py <task_id>")
        sys.exit(1)

    task_id = sys.argv[1]

    print("🔍 Ozon任务状态查询器启动（简化版）")
    print(f"⏳ 正在查询任务ID {task_id} 的状态...")

    # 加载配置
    client_id, api_key = load_config()

    # 创建查询器实例
    checker = OzonStatusChecker(client_id, api_key)

    # 查询状态
    result = checker.check_task_status(task_id)

    if result:
        print("✅ 任务状态查询成功！")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 检查商品状态 - 只要状态是imported就算成功
        items = result.get('result', {}).get('items', [])
        success_count = 0
        for item in items:
            status = item.get('status')
            offer_id = item.get('offer_id')
            product_id = item.get('product_id')

            if status == 'imported':
                print(f"✅ 商品 {offer_id} 已成功导入！Ozon Product ID: {product_id}")
                success_count += 1

                # 显示存在的错误或警告（但不尝试修复）
                errors = item.get('errors', [])
                if errors:
                    print("⚠️  注意：存在以下问题需要手动处理：")
                    for error in errors:
                        error_msg = error.get('message', '未知错误')
                        attribute_name = error.get('attribute_name', '未知属性')
                        print(f"   - 属性 '{attribute_name}': {error_msg}")
                    print("💡 请在Ozon卖家后台手动修正这些问题")
            else:
                print(f"❌ 商品 {offer_id} 导入失败，状态: {status}")

        if success_count > 0:
            print(f"\n🎉 总共成功导入 {success_count} 个商品！")
            print("📝 记住：如果有字典验证问题，请在Ozon后台手动处理")
        else:
            print("\n💥 所有商品都导入失败！")
            sys.exit(1)

    else:
        print("💥 任务状态查询失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()