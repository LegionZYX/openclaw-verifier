# OpenClaw Verifier Skill 版本

## 定位
Agent 原生安全扫描 Skill

## 架构

```
openclaw-verifier/
├── SKILL.md              # 主入口
├── skills/
│   ├── verify-skill/     # 扫描单个 skill
│   ├── batch-verify/     # 批量扫描
│   ├── auto-fix/         # 自动修复
│   └── risk-check/       # 快速决策
└── rules/
    └── patterns.json     # 检测规则
```

## 核心功能

### 1. verify-skill
扫描单个 skill，返回结构化结果

### 2. batch-verify
扫描所有已安装 skills

### 3. auto-fix
自动修复检测到的问题

### 4. risk-check
快速判断 safe/unsafe

## 版本计划

- v0.3.0: Skill 化重构
- v0.4.0: Hook 集成
- v1.0.0: Agent 自动化

---

开始实现？
