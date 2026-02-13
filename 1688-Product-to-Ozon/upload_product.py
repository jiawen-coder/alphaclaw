#!/usr/bin/env python3
"""
Ozon商品上传器
通过Ozon API v3/product/import接口上传商品
修复版本：直接接受完整的Ozon格式数据，不进行不必要的验证
"""

import os
import json
import sys
import requests
from typing import Dict, Any, Optional


class OzonProductUploader:
    def __init__(self, client_id: str, api_key: str):
        """
        初始化Ozon商品上传器

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

    def import_products(self, ozon_data: Dict[str, Any]) -> Optional[str]:
        """
        调用Ozon v3/product/import接口导入商品
        直接使用完整的Ozon格式数据，不进行额外验证

        Args:
            ozon_data: 完整的Ozon商品数据（包含items数组）

        Returns:
            str: 任务ID，失败时返回None
        """
        url = f"{self.base_url}/v3/product/import"

        try:
            response = requests.post(
                url,
                headers=self.create_headers(),
                json=ozon_data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                task_id = result.get('result', {}).get('task_id')
                if task_id:
                    print(f"✅ 商品上传请求成功，任务ID: {task_id}")
                    return task_id
                else:
                    print("❌ 响应中未找到task_id")
                    print(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    return None
            else:
                print(f"❌ 上传商品失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求错误: {e}")
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
    print("🚀 Ozon商品上传器启动")

    # 加载配置
    client_id, api_key = load_config()

    # 创建上传器实例
    uploader = OzonProductUploader(client_id, api_key)

    # 从标准输入读取完整的Ozon格式商品数据
    print("📥 请提供完整的Ozon商品JSON数据（按Ctrl+D结束输入）:")
    try:
        input_data = sys.stdin.read()
        ozon_data = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 操作已取消")
        sys.exit(0)

    # 验证基本格式
    if 'items' not in ozon_data or not isinstance(ozon_data['items'], list):
        print("❌ 数据格式错误：必须包含'items'数组")
        sys.exit(1)

    # 上传商品
    task_id = uploader.import_products(ozon_data)

    if task_id:
        print(f"🎉 商品上传请求成功！任务ID: {task_id}")
        print("💡 使用 check_status.py 脚本查询任务状态")
        # 输出任务ID到标准输出，便于后续脚本使用
        print(f"task_id_from_upload={task_id}")
        sys.exit(0)
    else:
        print("💥 商品上传失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()