import requests
import yaml
class aitools:
    def __init__(self) -> None:
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)

    

    # 自定义处理函数
    def implement(self, input_text, taskindex=0):
        url = "https://api.siliconflow.cn/v1/chat/completions"
        # 构建请求体，这里需要根据 API 文档正确设置请求体结构，以下是示例
        payload = {
            "model": "Qwen/Qwen2.5-VL-32B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": "".join([str(value) for value in self.config["tasks"][int(taskindex)].values()])+input_text
                }
            ]
        }
        # 你需要根据 API 要求添加正确的请求头，例如 API 密钥等
        headers = {
            "Content-Type": "application/json",
            # 如果有 API 密钥，添加在这里
            "Authorization": self.config.get("aksk")
        }
        try:
            # 发送 POST 请求
            response = requests.post(url, json=payload, headers=headers)
            # 检查响应状态码
            response.raise_for_status()
            result = response.json()
            # 假设 API 返回的结果中，回复内容在特定字段中，需要根据实际 API 文档调整
            # 这里只是示例，可能需要修改
            reply = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            return reply
        except requests.RequestException as e:
            # 处理请求异常
            error_message = f"请求发生错误: {str(e)}"
            print(error_message)
            return error_message