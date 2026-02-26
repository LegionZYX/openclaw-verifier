#!/usr/bin/env python3
"""
OpenClaw Skill Verifier
验证 OpenClaw Skill 的安全性
支持多种 AI 模型
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from enum import Enum

class AIModel(Enum):
    """支持的 AI 模型"""
    LOCAL = "local"           # 本地模式（无 AI）
    GPT4 = "gpt-4"             # OpenAI GPT-4
    GPT4O = "gpt-4o"           # OpenAI GPT-4o
    CLAUDE = "claude"          # Anthropic Claude
    QWEN = "qwen"              # 阿里千问
    QWEN_CODING = "qwen-coding"  # 千问 Coding
    DEEPSEEK = "deepseek"      # DeepSeek

class ModelConfig:
    """模型配置"""
    
    CONFIG = {
        AIModel.LOCAL: {
            "api_key_env": None,
            "api_base": None,
            "model_name": "local",
        },
        AIModel.GPT4: {
            "api_key_env": "OPENAI_API_KEY",
            "api_base": "https://api.openai.com/v1",
            "model_name": "gpt-4",
        },
        AIModel.GPT4O: {
            "api_key_env": "OPENAI_API_KEY",
            "api_base": "https://api.openai.com/v1",
            "model_name": "gpt-4o",
        },
        AIModel.CLAUDE: {
            "api_key_env": "ANTHROPIC_API_KEY",
            "api_base": "https://api.anthropic.com/v1",
            "model_name": "claude-3-sonnet-20240229",
        },
        AIModel.QWEN: {
            "api_key_env": "DASHSCOPE_API_KEY",
            "api_base": "https://dashscope.aliyuncs.com/api/v1",
            "model_name": "qwen-max",
        },
        AIModel.QWEN_CODING: {
            "api_key_env": "DASHSCOPE_API_KEY",
            "api_base": "https://dashscope.aliyuncs.com/api/v1",
            "model_name": "qwen-coder-plus",
        },
        AIModel.DEEPSEEK: {
            "api_key_env": "DEEPSEEK_API_KEY",
            "api_base": "https://api.deepseek.com/v1",
            "model_name": "deepseek-coder",
        },
    }
    
    @classmethod
    def get_config(cls, model: AIModel) -> Dict:
        return cls.CONFIG.get(model, cls.CONFIG[AIModel.LOCAL])
    
    @classmethod
    def get_api_key(cls, model: AIModel) -> Optional[str]:
        config = cls.get_config(model)
        env_var = config.get("api_key_env")
        if env_var:
            return os.environ.get(env_var)
        return None
    
    @classmethod
    def is_available(cls, model: AIModel) -> bool:
        if model == AIModel.LOCAL:
            return True
        return cls.get_api_key(model) is not None
    
    @classmethod
    def list_available(cls) -> List[AIModel]:
        return [m for m in AIModel if cls.is_available(m)]

class AIClient:
    """AI 客户端"""
    
    def __init__(self, model: AIModel = AIModel.LOCAL):
        self.model = model
        self.config = ModelConfig.get_config(model)
    
    def analyze(self, prompt: str, content: str) -> str:
        """使用 AI 分析内容"""
        if self.model == AIModel.LOCAL:
            return self._local_analyze(content)
        elif self.model in [AIModel.GPT4, AIModel.GPT4O]:
            return self._openai_analyze(prompt, content)
        elif self.model == AIModel.CLAUDE:
            return self._claude_analyze(prompt, content)
        elif self.model in [AIModel.QWEN, AIModel.QWEN_CODING]:
            return self._qwen_analyze(prompt, content)
        elif self.model == AIModel.DEEPSEEK:
            return self._deepseek_analyze(prompt, content)
        else:
            return self._local_analyze(content)
    
    def _local_analyze(self, content: str) -> str:
        """本地分析（基于规则）"""
        return "Local analysis only - no AI enhancement"
    
    def _openai_analyze(self, prompt: str, content: str) -> str:
        """OpenAI API 调用"""
        try:
            import openai
            api_key = ModelConfig.get_api_key(self.model)
            if not api_key:
                return "Error: OPENAI_API_KEY not set"
            
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=self.config["model_name"],
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
    
    def _claude_analyze(self, prompt: str, content: str) -> str:
        """Claude API 调用"""
        try:
            import anthropic
            api_key = ModelConfig.get_api_key(self.model)
            if not api_key:
                return "Error: ANTHROPIC_API_KEY not set"
            
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model=self.config["model_name"],
                max_tokens=1000,
                system=prompt,
                messages=[
                    {"role": "user", "content": content}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude Error: {str(e)}"
    
    def _qwen_analyze(self, prompt: str, content: str) -> str:
        """千问 API 调用"""
        try:
            import requests
            api_key = ModelConfig.get_api_key(self.model)
            if not api_key:
                return "Error: DASHSCOPE_API_KEY not set"
            
            url = f"{self.config['api_base']}/services/aigc/text-generation/generation"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.config["model_name"],
                "input": {
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": content}
                    ]
                },
                "parameters": {
                    "max_tokens": 1000
                }
            }
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            return result.get("output", {}).get("text", "No response")
        except Exception as e:
            return f"Qwen Error: {str(e)}"
    
    def _deepseek_analyze(self, prompt: str, content: str) -> str:
        """DeepSeek API 调用"""
        try:
            import openai
            api_key = ModelConfig.get_api_key(self.model)
            if not api_key:
                return "Error: DEEPSEEK_API_KEY not set"
            
            client = openai.OpenAI(
                api_key=api_key,
                base_url=self.config["api_base"]
            )
            response = client.chat.completions.create(
                model=self.config["model_name"],
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"DeepSeek Error: {str(e)}"

class SkillVerifier:
    """Skill 安全验证器"""
    
    # 恶意模式库
    MALICIOUS_PATTERNS = {
        "external_api": {
            "patterns": [
                r"https?://(?!localhost|127\.0\.0\.1)[^'\"\s]+",
                r"fetch\(['\"]https?://",
                r"requests\.(get|post|put|delete)\(['\"]https?://",
            ],
            "severity": "high",
            "description": "External API calls detected"
        },
        "eval_exec": {
            "patterns": [
                r"\beval\s*\(",
                r"\bexec\s*\(",
                r"\bexec\s+",
                r"__import__\s*\(",
            ],
            "severity": "critical",
            "description": "Dynamic code execution"
        },
        "file_access": {
            "patterns": [
                r"open\s*\(['\"](?!memory/)",
                r"\.read\s*\(",
                r"\.write\s*\(",
                r"shutil\.(copy|move|rmtree)",
            ],
            "severity": "medium",
            "description": "File system access outside memory/"
        },
        "network": {
            "patterns": [
                r"socket\.",
                r"subprocess\.",
                r"os\.system\s*\(",
            ],
            "severity": "high",
            "description": "Network/subprocess access"
        },
        "crypto_keys": {
            "patterns": [
                r"[a-zA-Z0-9]{32,}",
                r"(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]+['\"]",
            ],
            "severity": "critical",
            "description": "Potential API keys or secrets"
        }
    }
    
    def __init__(self, skill_path: str, model: str = "local"):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        
        # 解析模型
        self.model = self._parse_model(model)
        self.ai_client = AIClient(self.model)
        
        self.results = {
            "skill": str(skill_path),
            "model": self.model.value,
            "files_scanned": 0,
            "issues": [],
            "score": 100
        }
    
    def _parse_model(self, model_str: str) -> AIModel:
        """解析模型字符串"""
        model_map = {
            "local": AIModel.LOCAL,
            "gpt-4": AIModel.GPT4,
            "gpt-4o": AIModel.GPT4O,
            "gpt4": AIModel.GPT4,
            "gpt4o": AIModel.GPT4O,
            "claude": AIModel.CLAUDE,
            "qwen": AIModel.QWEN,
            "qwen-coding": AIModel.QWEN_CODING,
            "qwen-coder": AIModel.QWEN_CODING,
            "deepseek": AIModel.DEEPSEEK,
        }
        return model_map.get(model_str.lower(), AIModel.LOCAL)
    
    def scan(self) -> Dict:
        """扫描 Skill"""
        if not self.skill_md.exists():
            self.results["issues"].append({
                "severity": "critical",
                "description": "SKILL.md not found",
                "file": str(self.skill_path)
            })
            self.results["score"] = 0
            return self.results
        
        # 扫描 SKILL.md
        self._scan_file(self.skill_md)
        
        # 扫描所有 Python 文件
        for py_file in self.skill_path.rglob("*.py"):
            self._scan_file(py_file)
        
        # 扫描所有脚本文件
        for script_file in self.skill_path.rglob("*.sh"):
            self._scan_file(script_file)
        
        # 计算最终分数
        self._calculate_score()
        
        # 如果有 AI 模型，进行 AI 分析
        if self.model != AIModel.LOCAL and self.results["issues"]:
            self._ai_analyze()
        
        return self.results
    
    def _scan_file(self, file_path: Path):
        """扫描单个文件"""
        self.results["files_scanned"] += 1
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            self.results["issues"].append({
                "severity": "low",
                "description": f"Could not read file: {e}",
                "file": str(file_path)
            })
            return
        
        # 检查恶意模式
        for category, config in self.MALICIOUS_PATTERNS.items():
            for pattern in config["patterns"]:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    self.results["issues"].append({
                        "severity": config["severity"],
                        "category": category,
                        "description": config["description"],
                        "file": str(file_path.relative_to(self.skill_path)),
                        "line": content[:match.start()].count('\n') + 1,
                        "match": match.group(0)[:50]
                    })
    
    def _calculate_score(self):
        """计算安全分数"""
        severity_weights = {
            "critical": 30,
            "high": 15,
            "medium": 5,
            "low": 1
        }
        
        total_penalty = 0
        for issue in self.results["issues"]:
            total_penalty += severity_weights.get(issue["severity"], 1)
        
        self.results["score"] = max(0, 100 - total_penalty)
    
    def _ai_analyze(self):
        """使用 AI 进行深度分析"""
        prompt = """你是安全分析师。分析以下 OpenClaw Skill 的安全问题，
提供：
1. 风险评估
2. 潜在威胁
3. 修复建议"""

        content = f"扫描结果：{json.dumps(self.results['issues'], ensure_ascii=False, indent=2)}"
        
        ai_analysis = self.ai_client.analyze(prompt, content)
        self.results["ai_analysis"] = ai_analysis
    
    def get_risk_level(self) -> str:
        """获取风险等级"""
        score = self.results["score"]
        if score >= 90:
            return "LOW"
        elif score >= 70:
            return "MEDIUM"
        elif score >= 50:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def generate_report(self) -> str:
        """生成报告"""
        report = []
        report.append("=" * 60)
        report.append("OpenClaw Skill Security Report")
        report.append("=" * 60)
        report.append(f"\nSkill: {self.results['skill']}")
        report.append(f"Model: {self.results['model']}")
        report.append(f"Files Scanned: {self.results['files_scanned']}")
        report.append(f"Security Score: {self.results['score']}/100")
        report.append(f"Risk Level: {self.get_risk_level()}")
        report.append("")
        
        if self.results["issues"]:
            report.append("Issues Found:")
            report.append("-" * 60)
            
            for i, issue in enumerate(self.results["issues"], 1):
                report.append(f"\n{i}. [{issue['severity'].upper()}] {issue['description']}")
                report.append(f"   Category: {issue.get('category', 'N/A')}")
                report.append(f"   File: {issue['file']}")
                if 'line' in issue:
                    report.append(f"   Line: {issue['line']}")
                if 'match' in issue:
                    report.append(f"   Match: {issue['match']}")
        else:
            report.append("No issues found!")
        
        if "ai_analysis" in self.results:
            report.append("\n" + "=" * 60)
            report.append("AI Analysis:")
            report.append("-" * 60)
            report.append(self.results["ai_analysis"])
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)


def verify_skill(skill_path: str, model: str = "local") -> Dict:
    """验证 Skill 的便捷函数"""
    verifier = SkillVerifier(skill_path, model)
    return verifier.scan()


def list_models() -> List[str]:
    """列出可用的模型"""
    available = ModelConfig.list_available()
    return [m.value for m in available]


def main():
    """CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python verify_skill.py <skill_path> [model]")
        print("\nAvailable models:")
        for model in list_models():
            print(f"  - {model}")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "local"
    
    print(f"Using model: {model}")
    verifier = SkillVerifier(skill_path, model)
    results = verifier.scan()
    
    # 打印报告
    print(verifier.generate_report())
    
    # 保存 JSON 结果
    json_output = Path(skill_path) / "verification_report.json"
    with open(json_output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nJSON report saved to: {json_output}")
    
    # 退出码
    sys.exit(0 if results["score"] >= 70 else 1)


if __name__ == "__main__":
    main()
