# MCP Translation Server

满语-中文翻译和文本分析服务器

## 功能特性

✨ **核心功能：**
- 满语 ↔ 中文双向翻译
- 形态学分析（词性、时态、人称等）
- RESTful API 接口
- 错误处理和验证

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/liliya0822/mcp-translation-server.git
cd mcp-translation-server
```

### 2. 创建虚拟环境

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置项目

```bash
# 复制配置模板
cp config/config.example.json config/config.json

# 编辑配置文件（可选）
vim config/config.json
```

### 5. 运行服务器

```bash
python server.py
```

服务器将在 `http://localhost:8000` 启动

### 6. 运行演示

```bash
python demo/comprehensive_demo.py
```

## API 文档

### 获取服务器信息

```http
GET /
```

**响应示例：**
```json
{
  "name": "MCP Translation Server",
  "version": "1.0.0",
  "endpoints": {
    "translate": "POST /api/v1/translate",
    "analyze": "POST /api/v1/analyze",
    "health": "GET /health"
  }
}
```

### 健康检查

```http
GET /health
```

**响应示例：**
```json
{
  "status": "healthy"
}
```

### 获取支持的语言

```http
GET /api/v1/languages
```

**响应示例：**
```json
{
  "supported_languages": ["manchu", "chinese"],
  "language_pairs": [
    {
      "source": "manchu",
      "target": "chinese"
    },
    {
      "source": "chinese",
      "target": "manchu"
    }
  ]
}
```

### 翻译文本

```http
POST /api/v1/translate
Content-Type: application/json

{
  "text": "bi bithe arambi",
  "source_lang": "manchu",
  "target_lang": "chinese"
}
```

**响应示例：**
```json
{
  "original_text": "bi bithe arambi",
  "translated_text": "我 书 来",
  "source_lang": "manchu",
  "target_lang": "chinese",
  "confidence": 0.85
}
```

### 文本分析（形态学）

```http
POST /api/v1/analyze
Content-Type: application/json

{
  "text": "arambi",
  "type": "morphology"
}
```

**响应示例：**
```json
{
  "text": "arambi",
  "analysis_type": "morphology",
  "result": {
    "lemma": "ara",
    "pos": "verb",
    "tense": "present",
    "person": "1st",
    "number": "singular",
    "mood": "indicative"
  }
}
```

### 获取支持的分析类型

```http
GET /api/v1/analysis-types
```

**响应示例：**
```json
{
  "analysis_types": [
    {
      "type": "morphology",
      "description": "形态学分析，包括词性、时态等信息"
    }
  ]
}
```

## 项目结构

```
mcp-translation-server/
├── server.py                    # 主服务器应用
├── demo/
│   └── comprehensive_demo.py    # 综合演示脚本
├── config/
│   └── config.example.json      # 配置模板
├── requirements.txt             # 项目依赖
└── README.md                    # 项目文档
```

## 支持的语言对

| 源语言 | 目标语言 |
|--------|----------|
| manchu | chinese |
| chinese | manchu |

## 支持的分析类型

| 类型 | 描述 |
|------|------|
| morphology | 形态学分析（词性、时态、人称等） |

## 使用示例

### Python 客户端

```python
import requests

# 翻译示例
response = requests.post(
    "http://localhost:8000/api/v1/translate",
    json={
        "text": "bi bithe arambi",
        "source_lang": "manchu",
        "target_lang": "chinese"
    }
)
print(response.json())

# 分析示例
response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json={
        "text": "arambi",
        "type": "morphology"
    }
)
print(response.json())
```

### curl

```bash
# 翻译请求
curl -X POST http://localhost:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "bi bithe arambi",
    "source_lang": "manchu",
    "target_lang": "chinese"
  }'

# 分析请求
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "arambi",
    "type": "morphology"
  }'
```

## 交互式 API 文档

启动服务器后，访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 故障排除

### 无法连接到服务器

```bash
# 检查服务器是否运行
python server.py

# 检查端口是否被占用
# Linux/Mac: lsof -i :8000
# Windows: netstat -ano | findstr :8000
```

### 导入错误

```bash
# 确保虚拟环境已激活
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 重新安装依赖
pip install -r requirements.txt
```

### 配置文件错误

```bash
# 复制示例配置
cp config/config.example.json config/config.json
```

## 开发和贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- 项目主页: https://github.com/liliya0822/mcp-translation-server
- 问题报告: https://github.com/liliya0822/mcp-translation-server/issues
