#!/usr/bin/env python3
"""
OpenClaw Skill Verifier
验证 OpenClaw Skill 的安全性
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

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
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / "SKILL.md"
        self.results = {
            "skill": str(skill_path),
            "files_scanned": 0,
            "issues": [],
            "score": 100
        }
    
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
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)


def verify_skill(skill_path: str) -> Dict:
    """验证 Skill 的便捷函数"""
    verifier = SkillVerifier(skill_path)
    return verifier.scan()


def main():
    """CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python verify_skill.py <skill_path>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    verifier = SkillVerifier(skill_path)
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
