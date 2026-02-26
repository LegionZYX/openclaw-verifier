#!/usr/bin/env python3
"""
模型切换工具
快速切换 OpenClaw Verifier 使用的 AI 模型
"""

import os
import sys
from pathlib import Path

# 支持的模型
MODELS = {
    "local": {
        "name": "本地模式",
        "env_var": None,
        "description": "不使用 AI，仅基于规则分析"
    },
    "gpt-4": {
        "name": "GPT-4",
        "env_var": "OPENAI_API_KEY",
        "description": "OpenAI GPT-4 模型"
    },
    "gpt-4o": {
        "name": "GPT-4o",
        "env_var": "OPENAI_API_KEY",
        "description": "OpenAI GPT-4o 模型"
    },
    "claude": {
        "name": "Claude",
        "env_var": "ANTHROPIC_API_KEY",
        "description": "Anthropic Claude 模型"
    },
    "qwen": {
        "name": "千问",
        "env_var": "DASHSCOPE_API_KEY",
        "description": "阿里千问通用模型"
    },
    "qwen-coding": {
        "name": "千问 Coding",
        "env_var": "DASHSCOPE_API_KEY",
        "description": "阿里千问编程专用模型 (推荐)"
    },
    "deepseek": {
        "name": "DeepSeek",
        "env_var": "DEEPSEEK_API_KEY",
        "description": "DeepSeek 编程模型"
    }
}

# 配置文件路径
CONFIG_FILE = Path.home() / ".openclaw-verifier" / "config.json"

def get_current_model():
    """获取当前模型"""
    if CONFIG_FILE.exists():
        import json
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return config.get("current_model", "local")
    return "local"

def set_current_model(model):
    """设置当前模型"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    import json
    config = {"current_model": model}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print(f"✅ 已切换到: {MODELS[model]['name']}")

def check_model_available(model):
    """检查模型是否可用"""
    info = MODELS.get(model)
    if not info:
        return False, "未知模型"
    
    if info["env_var"] is None:
        return True, "可用"
    
    api_key = os.environ.get(info["env_var"])
    if api_key:
        return True, "可用"
    else:
        return False, f"未设置 {info['env_var']}"

def list_models():
    """列出所有模型"""
    current = get_current_model()
    print("\n可用模型:")
    print("-" * 50)
    
    for key, info in MODELS.items():
        available, status = check_model_available(key)
        marker = "👉 " if key == current else "   "
        status_icon = "✅" if available else "❌"
        
        print(f"{marker}{key:15} {status_icon} {info['name']:10} - {info['description']}")
        if not available and info["env_var"]:
            print(f"                  需要设置: {info['env_var']}")

def set_api_key(env_var, api_key):
    """设置 API Key"""
    # 写入到用户环境变量（临时）
    os.environ[env_var] = api_key
    
    # 写入到配置文件（永久）
    env_file = Path.home() / ".openclaw-verifier" / ".env"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取现有内容
    existing = {}
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                existing[k.strip()] = v.strip()
    
    # 更新
    existing[env_var] = api_key
    
    # 写入
    with open(env_file, "w") as f:
        for k, v in existing.items():
            f.write(f"{k}={v}\n")
    
    print(f"✅ 已保存 {env_var}")

def main():
    if len(sys.argv) < 2:
        print("OpenClaw Verifier 模型管理工具")
        print()
        list_models()
        print()
        print("用法:")
        print("  python model_manager.py list          列出所有模型")
        print("  python model_manager.py use <model>   切换模型")
        print("  python model_manager.py set-key <env_var> <api_key>   设置 API Key")
        print()
        print("示例:")
        print("  python model_manager.py use qwen-coding")
        print("  python model_manager.py set-key DASHSCOPE_API_KEY sk-xxx")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_models()
    
    elif command == "use":
        if len(sys.argv) < 3:
            print("请指定模型: python model_manager.py use <model>")
            return
        
        model = sys.argv[2]
        if model not in MODELS:
            print(f"❌ 未知模型: {model}")
            list_models()
            return
        
        available, status = check_model_available(model)
        if not available:
            print(f"❌ 模型不可用: {status}")
            return
        
        set_current_model(model)
    
    elif command == "set-key":
        if len(sys.argv) < 4:
            print("用法: python model_manager.py set-key <env_var> <api_key>")
            return
        
        env_var = sys.argv[2]
        api_key = sys.argv[3]
        set_api_key(env_var, api_key)
    
    elif command == "current":
        current = get_current_model()
        print(f"当前模型: {MODELS[current]['name']} ({current})")
    
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
