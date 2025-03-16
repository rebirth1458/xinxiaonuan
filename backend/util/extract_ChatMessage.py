import json

def extract_ChatMessage(json_str):
    """
    从给定的JSON字符串中提取content和type的内容。

    参数:
    - json_str (str): 包含所需数据的JSON格式字符串。

    返回:
    - dict: 包含提取出的content和type的字典。
    """
    data_dict = json.loads(json_str)

    content = data_dict.get('data', {}).get('content')
    type_field = data_dict.get('type')

    return {
        'content': content,
        'type': type_field,
    }


json_str = '{"type": "human", "data": {"content": "你是谁", "additional_kwargs": {}, "response_metadata": {}, "type": "human", "name": null, "id": null, "example": false}}'
result = extract_ChatMessage(json_str)
print(result)