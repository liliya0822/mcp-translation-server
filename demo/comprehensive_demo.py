"""
MCP Translation Server 综合演示
演示翻译和分析功能
"""

import requests
import json
from typing import Dict, Any
import time

# 服务器配置
BASE_URL = "http://localhost:8000"

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(title: str):
    """打印标题"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}")
    print(f"{title.center(60)}")
    print(f"{'=' * 60}{Colors.ENDC}\n")

def print_success(message: str):
    """打印成功消息"""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_error(message: str):
    """打印错误消息"""
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")

def print_info(message: str):
    """打印信息"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.ENDC}")

def print_request(method: str, endpoint: str, data: Dict[str, Any] = None):
    """打印请求信息"""
    print(f"{Colors.BLUE}{method} {endpoint}{Colors.ENDC}")
    if data:
        print(f"Body: {json.dumps(data, indent=2, ensure_ascii=False)}")

def print_response(response: Dict[str, Any], status_code: int = 200):
    """打印响应信息"""
    status_color = Colors.GREEN if 200 <= status_code < 300 else Colors.RED
    print(f"{status_color}Status: {status_code}{Colors.ENDC}")
    print(f"Response:\n{json.dumps(response, indent=2, ensure_ascii=False)}")

def check_server_health():
    """检查服务器健康状态"""
    print_header("服务器健康检查")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("服务器正在运行")
            print_response(response.json())
            return True
        else:
            print_error(f"服务器返回错误状态: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("无法连接到服务器")
        print_info(f"请确保服务器运行在 {BASE_URL}")
        return False
    except Exception as e:
        print_error(f"错误: {str(e)}")
        return False

def demo_root_endpoint():
    """演示根端点"""
    print_header("根端点")
    
    try:
        print_request("GET", "/")
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code == 200:
            print_success("成功获取服务器信息")
            print_response(response.json())
        else:
            print_error(f"请求失败: {response.status_code}")
    except Exception as e:
        print_error(f"错误: {str(e)}")

def demo_translation_examples():
    """演示翻译示例"""
    print_header("翻译示例")
    
    examples = [
        {
            "text": "bi bithe arambi",
            "source_lang": "manchu",
            "target_lang": "chinese",
            "description": "满语短句翻译"
        },
        {
            "text": "bi",
            "source_lang": "manchu",
            "target_lang": "chinese",
            "description": "单词翻译 - 我"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{Colors.YELLOW}示例 {i}: {example['description']}{Colors.ENDC}")
        
        data = {
            "text": example["text"],
            "source_lang": example["source_lang"],
            "target_lang": example["target_lang"]
        }
        
        try:
            print_request("POST", "/api/v1/translate", data)
            response = requests.post(f"{BASE_URL}/api/v1/translate", json=data)
            
            if response.status_code == 200:
                print_success("翻译成功")
                print_response(response.json())
            else:
                print_error(f"翻译失败: {response.status_code}")
                print_response(response.json(), response.status_code)
        except Exception as e:
            print_error(f"错误: {str(e)}")

def demo_analysis_examples():
    """演示分析示例"""
    print_header("文本分析示例")
    
    examples = [
        {
            "text": "arambi",
            "type": "morphology",
            "description": "动词分析"
        },
        {
            "text": "bi",
            "type": "morphology",
            "description": "代词分析"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{Colors.YELLOW}示例 {i}: {example['description']}{Colors.ENDC}")
        
        data = {
            "text": example["text"],
            "type": example["type"]
        }
        
        try:
            print_request("POST", "/api/v1/analyze", data)
            response = requests.post(f"{BASE_URL}/api/v1/analyze", json=data)
            
            if response.status_code == 200:
                print_success("分析成功")
                result = response.json()
                print_response(result)
            else:
                print_error(f"分析失败: {response.status_code}")
                print_response(response.json(), response.status_code)
        except Exception as e:
            print_error(f"错误: {str(e)}")

def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║     MCP Translation Server 综合演示                        ║")
    print("║     满语-中文翻译和文本分析服务                             ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    # 检查服务器状态
    if not check_server_health():
        print_error("演示中止，请先启动服务器")
        return
    
    time.sleep(1)
    demo_root_endpoint()
    time.sleep(1)
    
    demo_translation_examples()
    time.sleep(1)
    
    demo_analysis_examples()
    
    # 结束
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║                    演示完成！                               ║")
    print("║           感谢使用 MCP Translation Server                   ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}演示已中断{Colors.ENDC}\n")
    except Exception as e:
        print_error(f"演示出错: {str(e)}\n")
