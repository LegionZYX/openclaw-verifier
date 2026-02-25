#!/usr/bin/env python3
"""
测试 OpenClaw Verifier
"""

import pytest
from verify_skill import SkillVerifier
import tempfile
import os

class TestSkillVerifier:
    
    def test_safe_skill(self):
        """测试安全的 Skill"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建安全的 SKILL.md
            skill_md = os.path.join(tmpdir, "SKILL.md")
            with open(skill_md, 'w') as f:
                f.write("""
# Safe Skill

This is a safe skill that only reads from memory/.

## Usage

Use this skill to read files from memory/.
""")
            
            verifier = SkillVerifier(tmpdir)
            result = verifier.scan()
            
            assert result["score"] >= 90
            assert verifier.get_risk_level() == "LOW"
    
    def test_malicious_eval(self):
        """测试包含 eval 的恶意 Skill"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_md = os.path.join(tmpdir, "SKILL.md")
            with open(skill_md, 'w') as f:
                f.write("""
# Malicious Skill

This skill uses eval.

```python
eval(user_input)
```
""")
            
            verifier = SkillVerifier(tmpdir)
            result = verifier.scan()
            
            assert result["score"] < 80
            assert any(i["category"] == "eval_exec" for i in result["issues"])
    
    def test_external_api(self):
        """测试外部 API 调用"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_md = os.path.join(tmpdir, "SKILL.md")
            with open(skill_md, 'w') as f:
                f.write("""
# API Skill

Calls external API.

```python
import requests
response = requests.get("https://malicious-server.com/api")
```
""")
            
            verifier = SkillVerifier(tmpdir)
            result = verifier.scan()
            
            assert any(i["category"] == "external_api" for i in result["issues"])
    
    def test_no_skill_md(self):
        """测试没有 SKILL.md 的情况"""
        with tempfile.TemporaryDirectory() as tmpdir:
            verifier = SkillVerifier(tmpdir)
            result = verifier.scan()
            
            assert result["score"] == 0
            assert verifier.get_risk_level() == "CRITICAL"
    
    def test_crypto_key_detection(self):
        """测试密钥检测"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_md = os.path.join(tmpdir, "SKILL.md")
            with open(skill_md, 'w') as f:
                f.write("""
# API Key Skill

api_key = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
""")
            
            verifier = SkillVerifier(tmpdir)
            result = verifier.scan()
            
            assert any(i["category"] == "crypto_keys" for i in result["issues"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
