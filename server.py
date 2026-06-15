"""
MCP Translation Server
满语-中文翻译和文本分析服务器
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="MCP Translation Server",
    description="满语-中文翻译和文本分析服务",
    version="1.0.0"
)

# ==================== Models ====================

class TranslateRequest(BaseModel):
    """翻译请求模型"""
    text: str
    source_lang: str
    target_lang: str

class TranslateResponse(BaseModel):
    """翻译响应模型"""
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    confidence: float

class AnalyzeRequest(BaseModel):
    """分析请求模型"""
    text: str
    type: str

class AnalysisResult(BaseModel):
    """分析结果模型"""
    lemma: str
    pos: str
    tense: Optional[str] = None
    person: Optional[str] = None
    number: Optional[str] = None
    mood: Optional[str] = None

class AnalyzeResponse(BaseModel):
    """分析响应模型"""
    text: str
    analysis_type: str
    result: Dict[str, Any]

# ==================== Configuration ====================

def load_config():
    """加载配置文件"""
    config_path = "config/config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "translation_engine": "mock",
        "supported_languages": ["manchu", "chinese"],
        "max_text_length": 10000
    }

config = load_config()

# ==================== Translation Engine ====================

class TranslationEngine:
    """翻译引擎"""
    
    def __init__(self):
        self.supported_pairs = [
            ("manchu", "chinese"),
            ("chinese", "manchu")
        ]
    
    def is_language_pair_supported(self, source: str, target: str) -> bool:
        """检查语言对是否支持"""
        return (source.lower(), target.lower()) in self.supported_pairs
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """执行翻译"""
        # 这是一个模拟翻译引擎
        # 在实际应用中，应该集成真实的翻译服务
        
        translation_map = {
            ("manchu", "chinese"): {
                "bi bithe arambi": "我 书 来",
                "bi": "我",
                "bithe": "书",
                "arambi": "来",
                "amban": "官员",
                "dergi": "旗",
            },
            ("chinese", "manchu"): {
                "我 书 来": "bi bithe arambi",
                "我": "bi",
                "书": "bithe",
                "来": "arambi",
                "官员": "amban",
                "旗": "dergi",
            }
        }
        
        key = (source_lang.lower(), target_lang.lower())
        
        if text in translation_map.get(key, {}):
            translated_text = translation_map[key][text]
            confidence = 0.95
        else:
            # 默认翻译（如果没有找到精确匹配）
            translated_text = f"[翻译: {text}]"
            confidence = 0.5
        
        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "confidence": confidence
        }

# ==================== Analysis Engine ====================

class AnalysisEngine:
    """文本分析引擎"""
    
    def __init__(self):
        self.supported_types = ["morphology"]
        
        # 形态学分析库
        self.morphology_db = {
            "arambi": {
                "lemma": "ara",
                "pos": "verb",
                "tense": "present",
                "person": "1st",
                "number": "singular",
                "mood": "indicative"
            },
            "bi": {
                "lemma": "bi",
                "pos": "pronoun",
                "tense": None,
                "person": "1st",
                "number": "singular",
                "mood": None
            },
            "bithe": {
                "lemma": "bithe",
                "pos": "noun",
                "tense": None,
                "person": None,
                "number": "singular",
                "mood": None
            },
            "amban": {
                "lemma": "amban",
                "pos": "noun",
                "tense": None,
                "person": None,
                "number": "singular",
                "mood": None
            },
            "dergi": {
                "lemma": "dergi",
                "pos": "noun",
                "tense": None,
                "person": None,
                "number": "singular",
                "mood": None
            }
        }
    
    def is_analysis_type_supported(self, analysis_type: str) -> bool:
        """检查分析类型是否支持"""
        return analysis_type.lower() in self.supported_types
    
    def analyze(self, text: str, analysis_type: str) -> Dict[str, Any]:
        """执行分析"""
        text_lower = text.lower().strip()
        
        if text_lower in self.morphology_db:
            result = self.morphology_db[text_lower]
        else:
            # 默认分析结果
            result = {
                "lemma": text_lower,
                "pos": "unknown",
                "tense": None,
                "person": None,
                "number": "singular",
                "mood": None
            }
        
        return {
            "text": text,
            "analysis_type": analysis_type,
            "result": result
        }

# Initialize engines
translation_engine = TranslationEngine()
analysis_engine = AnalysisEngine()

# ==================== Routes ====================

@app.get("/")
async def root():
    """根端点"""
    return {
        "name": "MCP Translation Server",
        "version": "1.0.0",
        "description": "满语-中文翻译和文本分析服务",
        "endpoints": {
            "root": "GET /",
            "health": "GET /health",
            "languages": "GET /api/v1/languages",
            "analysis_types": "GET /api/v1/analysis-types",
            "translate": "POST /api/v1/translate",
            "analyze": "POST /api/v1/analyze"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/languages")
async def get_languages():
    """获取支持的语言"""
    return {
        "supported_languages": config.get("supported_languages", ["manchu", "chinese"]),
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

@app.get("/api/v1/analysis-types")
async def get_analysis_types():
    """获取支持的分析类型"""
    return {
        "analysis_types": [
            {
                "type": "morphology",
                "description": "形态学分析，包括词性、时态、人称等信息"
            }
        ]
    }

@app.post("/api/v1/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """翻译文本"""
    # 验证输入
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="文本不能为空")
    
    if len(request.text) > config.get("max_text_length", 10000):
        raise HTTPException(status_code=400, detail="文本超过最大长度")
    
    # 检查语言对是否支持
    if not translation_engine.is_language_pair_supported(request.source_lang, request.target_lang):
        raise HTTPException(
            status_code=400,
            detail=f"不支持的语言对: {request.source_lang} -> {request.target_lang}"
        )
    
    # 执行翻译
    result = translation_engine.translate(
        request.text,
        request.source_lang,
        request.target_lang
    )
    
    return result

@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """分析文本"""
    # 验证输入
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="文本不能为空")
    
    if len(request.text) > config.get("max_text_length", 10000):
        raise HTTPException(status_code=400, detail="文本超过最大长度")
    
    # 检查分析类型是否支持
    if not analysis_engine.is_analysis_type_supported(request.type):
        raise HTTPException(
            status_code=400,
            detail=f"不支持的分析类型: {request.type}"
        )
    
    # 执行分析
    result = analysis_engine.analyze(request.text, request.type)
    
    return result

# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP 异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "detail": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    
    # 从配置中读取服务器设置
    host = config.get("host", "0.0.0.0")
    port = config.get("port", 8000)
    debug = config.get("debug", True)
    
    print(f"🚀 Starting MCP Translation Server on {host}:{port}")
    print(f"📚 Swagger UI: http://localhost:{port}/docs")
    print(f"📖 ReDoc: http://localhost:{port}/redoc")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        debug=debug
    )
