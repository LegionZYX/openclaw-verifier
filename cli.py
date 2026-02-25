#!/usr/bin/env python3
"""
OpenClaw Verifier CLI
命令行工具
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List

# 导入核心验证器
from verify_skill import SkillVerifier

class VerifierCLI:
    """CLI 接口"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self):
        parser = argparse.ArgumentParser(
            description="OpenClaw Skill Security Verifier"
        )
        
        subparsers = parser.add_subparsers(dest="command")
        
        # scan 命令
        scan_parser = subparsers.add_parser("scan", help="Scan a skill")
        scan_parser.add_argument("skill_path", help="Path to skill directory")
        scan_parser.add_argument("--json", action="store_true", help="Output JSON")
        scan_parser.add_argument("--quiet", action="store_true", help="Minimal output")
        
        # batch 命令
        batch_parser = subparsers.add_parser("batch", help="Scan multiple skills")
        batch_parser.add_argument("directory", help="Directory containing skills")
        batch_parser.add_argument("--output", "-o", help="Output file")
        
        # report 命令
        report_parser = subparsers.add_parser("report", help="Generate report")
        report_parser.add_argument("skill_path", help="Path to skill directory")
        report_parser.add_argument("--format", choices=["text", "json", "html"], default="text")
        
        return parser
    
    def run(self, args=None):
        args = self.parser.parse_args(args)
        
        if args.command == "scan":
            return self._scan_skill(args)
        elif args.command == "batch":
            return self._batch_scan(args)
        elif args.command == "report":
            return self._generate_report(args)
        else:
            self.parser.print_help()
            return 1
    
    def _scan_skill(self, args):
        verifier = SkillVerifier(args.skill_path)
        results = verifier.scan()
        
        if args.json:
            print(json.dumps(results, indent=2))
        elif args.quiet:
            print(f"{results['score']} - {verifier.get_risk_level()}")
        else:
            print(verifier.generate_report())
        
        return 0 if results["score"] >= 70 else 1
    
    def _batch_scan(self, args):
        directory = Path(args.directory)
        skills = [d for d in directory.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        
        results = []
        for skill in skills:
            verifier = SkillVerifier(str(skill))
            result = verifier.scan()
            results.append({
                "skill": skill.name,
                "score": result["score"],
                "risk": verifier.get_risk_level(),
                "issues": len(result["issues"])
            })
        
        # 排序
        results.sort(key=lambda x: x["score"])
        
        # 输出
        print(f"Scanned {len(results)} skills\n")
        print(f"{'Skill':<30} {'Score':<10} {'Risk':<10} {'Issues':<10}")
        print("-" * 60)
        for r in results:
            print(f"{r['skill']:<30} {r['score']:<10} {r['risk']:<10} {r['issues']:<10}")
        
        # 保存
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.output}")
        
        # 返回码
        critical = sum(1 for r in results if r["score"] < 50)
        return 1 if critical > 0 else 0
    
    def _generate_report(self, args):
        verifier = SkillVerifier(args.skill_path)
        results = verifier.scan()
        
        if args.format == "json":
            print(json.dumps(results, indent=2))
        elif args.format == "html":
            html = self._generate_html_report(results, verifier)
            print(html)
        else:
            print(verifier.generate_report())
        
        return 0
    
    def _generate_html_report(self, results, verifier):
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>OpenClaw Skill Security Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .score {{ font-size: 48px; font-weight: bold; }}
        .low {{ color: green; }}
        .medium {{ color: orange; }}
        .high {{ color: red; }}
        .critical {{ color: darkred; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>OpenClaw Skill Security Report</h1>
    
    <h2>Summary</h2>
    <p>Skill: {results['skill']}</p>
    <p>Files Scanned: {results['files_scanned']}</p>
    <p class="score {verifier.get_risk_level().lower()}">Score: {results['score']}/100</p>
    <p>Risk Level: {verifier.get_risk_level()}</p>
    
    <h2>Issues ({len(results['issues'])})</h2>
    <table>
        <tr>
            <th>Severity</th>
            <th>Category</th>
            <th>Description</th>
            <th>File</th>
            <th>Line</th>
        </tr>
        {self._generate_issue_rows(results['issues'])}
    </table>
</body>
</html>
"""
    
    def _generate_issue_rows(self, issues):
        rows = []
        for issue in issues:
            rows.append(f"""
        <tr>
            <td class="{issue['severity']}">{issue['severity']}</td>
            <td>{issue.get('category', 'N/A')}</td>
            <td>{issue['description']}</td>
            <td>{issue['file']}</td>
            <td>{issue.get('line', 'N/A')}</td>
        </tr>
""")
        return "".join(rows)


def main():
    cli = VerifierCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
