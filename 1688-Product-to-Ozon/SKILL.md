---
name: 1688-Product-to-Ozon
version: 1.0.12
description: 将1688的商品铺货到俄罗斯电商平台Ozon（上架），通过Ozon官方API实现商品信息的上传和状态查询。适用于需要将单个1688的商品上架到Ozon的场景。
author: 红淼
created: 2026-02-12
metadata:
  openclaw:
    primaryEnv: OZON_API_KEY, OZON_CLIENT_ID, OZON_CURRENCY
    requires:
      env:
        - OZON_API_KEY
        - OZON_CLIENT_ID
        - OZON_CURRENCY
---

# 1688到Ozon商品转换技能

## 技能描述

本技能用于将1688的商品转化为对应的俄罗斯电商平台Ozon的商品数据，产出一个可以用于操作Ozon的上架API的JSON结构化数据。
之后再通过Ozon的开放平台的接口将商品信息上传到Ozon平台并查询上传结果。可以把1688的商品铺货到Ozon，上架到Ozon，上传到Ozon、上架Ozon、Ozon商品发布、Ozon产品上传、查询Ozon上传结果、铺货、1688商品铺货。

触发词：上传到Ozon、上架Ozon、Ozon商品发布、Ozon产品上传、查询Ozon上传结果、铺货、1688商品铺货。


## 什么时候使用

用户说需要铺货到Ozon，上架到Ozon，上传到Ozon、上架Ozon、Ozon商品发布、Ozon产品上传、查询Ozon上传结果、铺货、1688商品铺货。
用户说需要铺货到Ozon，上架到Ozon，上传到Ozon、上架Ozon、Ozon商品发布、Ozon产品上传、查询Ozon上传结果、铺货、1688商品铺货。
用户说需要铺货到Ozon，上架到Ozon，上传到Ozon、上架Ozon、Ozon商品发布、Ozon产品上传、查询Ozon上传结果、铺货、1688商品铺货。

以上的关键词都需要使用这个SKILL。

## 前置配置

使用前必须获取三个参数：

| 参数 | 说明 | 必填 |
|------|------|------|
| OZON_API_KEY | Ozon卖家后台的API Key  | ✅ |
| OZON_CLIENT_ID | Ozon卖家后台的Client ID| ✅ |
| 货币代码 | 必须与Ozon个人中心设置的币种匹配。默认RUB（卢布），如设了人民币选CNY | ✅ |

如果用户没提供这些参数，**必须先询问**。货币不匹配会导致API报错。

## 核心功能

### 1. **1688到Ozon类目映射**
- 调用1688 OpenClaw API获取商品对应的Ozon类目
- 输入：1688商品类目ID，从结构信息中获取，优先取thirdCategoryId的值，如果没有，获取categoryId的值，传递的应当是类目的值！！是数字
- 输出：对应的Ozon类目信息

### 2. **获取Ozon类目属性要求**
- 查询Ozon API获取目标类目的所有属性要求
- 输入：Ozon类目ID（多个用逗号分隔）、用户认证信息（OZON_API_KEY、OZON_CLIENT_ID）
- 输出：属性列表和详细要求
- 注意：直接使用上一步骤中获取到的externalCategoryId，这个值一般有两个，由逗号分隔，不要只取其中一个作为类目ID

### 3. **商品数据结构转换**
- 这一步非常重要，要使用上述两部分能力产出的数据！！！
- 由AI大模型接收1688商品信息和Ozon属性要求
- 智能映射和转换商品属性
- 输入：Ozon的类目属性要求、1688的商品数据（JSON格式）
- 输出：符合Ozon上架结构的商品结构（JSON格式）

#### Ozon的结构要求
这个是Ozon的结构实例，你需要按照这样的结构规范生成Ozon的商品数据，严格保持这个数据结构

```
{
    "items": [
        {
            "attributes": [
                {
                    "complex_id": 0,
                    "id": 5076,
                    "values": [
                        {
                            "dictionary_value_id": 971082156,
                            "value": "麦克风架"
                        }
                    ]
                },
                {
                    "complex_id": 0,
                    "id": 9048,
                    "values": [
                        {
                            "value": "一套X3NFC保护膜。 深色棉质"
                        }
                    ]
                },
                {
                    "complex_id": 0,
                    "id": 8229,
                    "values": [
                        {
                            "dictionary_value_id": 95911,
                            "value": "一套X3NFC保护膜。深色棉质"
                        }
                    ]
                },
                {
                    "complex_id": 0,
                    "id": 85,
                    "values": [
                        {
                            "dictionary_value_id": 5060050,
                            "value": "Samsung"
                        }
                    ]
                },
                {
                    "complex_id": 0,
                    "id": 10096,
                    "values": [
                        {
                            "dictionary_value_id": 61576,
                            "value": "灰色的"
                        }
                    ]
                }
            ],
            "barcode": "112772873170",
            "description_category_id": 17028922,
            "new_description_category_id": 0,
            "color_image": "",
            "complex_attributes": [],
            "currency_code": "RUB",
            "depth": 10,
            "dimension_unit": "mm",
            "height": 250,
            "images": [],
            "images360": [],
            "name": "一套X3NFC的保护膜。深色棉质",
            "offer_id": "143210608",
            "old_price": "1100",
            "pdf_list": [],
            "price": "1000",
            "primary_image": "",
            "promotions": [
                {
                    "operation": "UNKNOWN",
                    "type": "REVIEWS_PROMO"
                }
            ],
            "type_id": 91565,
            "vat": "0.1",
            "weight": 100,
            "weight_unit": "g",
            "width": 150
        }
    ]
}
```

#### 定制化规则
- 标题一定要翻译成俄语！标题一定要翻译成俄语！标题一定要翻译成俄语！
- items代表SKU列表，和1688的SKU是一一对应的
- vat的值固定为0
- offer_id的生成规则：使用1688的SKU_ID
- attributes代表属性列表,需要按照前序步骤获取到的“Ozon类目属性要求”来生成，只处理必须填写的属性！只处理必须填写的属性！
- 重量需要注意单位，都转化成为克（g）来处理
- 长度单位（dimension_unit）固定使用mm来处理，1688的数据都是cm为单位的数据
- 所有非数字、单位类型的值都需要翻译成俄语，例如商品的标题
- "23487"这个属性 固定值为中国
- "9048" 这个属性 使用随机生成的数字作为货号，1个1688的商品使用相同的值
- "4389" 这个属性 固定值为中国

#### 数据存储
创建你的商品数据文件，存储生成的Ozon的结构数据 my_products.json

### 4. **商品上架**
- 使用Ozon API的POST `/v3/product/import`端点上传商品数据。需要提供有效的ClientId和API Key进行认证。
- 输入：Ozon格式的商品JSON结构
- 输出：商品上架任务ID

```bash
python publish_product.py --product-data my_products.json
```

### 5. **查询商品上架结果**
- 使用Ozon API的POST `/v1/product/import/info`端点查询上传任务的状态和详细结果。
- 输入：任务ID
- 输出：商品上架状态和结果
- 注意：如果结果是imported就代表上传成功了，存在的问题可以让用户去商家后台修改

```bash

python check_status.py <task_id>

```

## 工作流程

注意：如果有任意一个步骤失败了，都直接返回错误，不要想象，不要想象，不要想象

```
1. 用户输入1688商品信息
         ↓
2. AI模型：解析出1688的叶子类目
         ↓
3. Python脚本`queryCategoryMapping.py`：查询类目映射 (1688类目ID → Ozon类目ID) 
         ↓
4. AI模型：从上一步的结果中解析出来Ozon的类目（externalCategoryId）
         ↓
5. Python脚本`queryOzonProperties.py`：通过externalCategoryId参数获取Ozon类目属性列表，得到Ozon的类目属性要求
         ↓
6. AI模型：将1688的商品数据结构转换为符合Ozon的上架规则的商品结构数据
         ↓
7. Python脚本`upload_product.py`：上传商品信息到Ozon
         ↓
8. Python脚本`check_upload_status.py`：查询商品上传状态，如果结果是imported就代表上传成功了
         ↓
9. 输出：Ozon的上传结果
```

## 包含的脚本

### `queryCategoryMapping.py`
查询1688到Ozon的类目映射
### `queryOzonProperties.py`
查询Ozon类目属性要求
### `upload_product.py`
上传商品信息到Ozon
### `check_upload_status.py`
查询商品上传状态


## 使用说明

1. 提供1688商品的基本信息
2. 提供Ozon认证信息（ClientId, API Key, 货币）
3. SKILL将自动调用python脚本完成转换，把1688的商品结构转化成适合Ozon的上架的结构数据
4. SKILL将会自动调用python脚本完成上传

---

**最后更新**: 2026-02-13