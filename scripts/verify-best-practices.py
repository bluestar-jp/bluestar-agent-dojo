#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def is_draft(content):
    # Check for draft status in frontmatter or body
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        if re.search(r'^draft:\s*true\s*$', frontmatter, re.MULTILINE):
            return True
    
    if "> **Status**: Draft" in content:
        return True
    return False

def has_japanese(text):
    # Check if string contains Japanese characters
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text))

def validate_frontmatter(content, file_path):
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        return False, "フロントマターが見つかりません。"
    
    frontmatter_text = frontmatter_match.group(1)
    
    # Simple regex-based YAML parser for key-value pairs
    data = {}
    for line in frontmatter_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    
    if not data:
        return False, "フロントマターが空、または解析可能なキーが見つかりません。"
    
    required = ['name', 'description']
    missing = [field for field in required if field not in data]
    if missing:
        return False, f"必須フィールドが不足しています: {', '.join(missing)}"
    
    return True, data

def validate_common(content, errors):
    # Check for Purpose and Scope (often as bullet points or headers)
    if not re.search(r'(Purpose|目的)', content, re.IGNORECASE):
        errors.append("目的 (Purpose) の記述が見つかりません。")
    if not re.search(r'(Scope|範囲)', content, re.IGNORECASE):
        errors.append("範囲 (Scope) の記述が見つかりません。")
    
    # Check for Workflow/Procedure sections (flexible matching)
    workflow_patterns = [
        r'##\s+(?:\d+\.\s*)?ワークフロー',
        r'##\s+(?:\d+\.\s*)?実行手順',
        r'##\s+(?:\d+\.\s*)?手順',
        r'##\s+(?:\d+\.\s*)?手順策定',
        r'##\s+(?:\d+\.\s*)?レビュー観点',
        r'##\s+(?:\d+\.\s*)?レビュー手順',
        r'##\s+(?:\d+\.\s*)?ライフサイクル',
        r'##\s+(?:\d+\.\s*)?Workflow',
        r'##\s+(?:\d+\.\s*)?Procedure',
        r'##\s+(?:\d+\.\s*)?Lifecycle'
    ]
    if not any(re.search(pattern, content, re.IGNORECASE) for pattern in workflow_patterns):
        errors.append("ワークフローまたは手順のセクション (## ワークフロー 等) が見つかりません。")

    # Check for Japanese content
    if not has_japanese(content):
        errors.append("日本語が含まれていません。")

def validate_agent(file_path):
    errors = []
    name = file_path.name
    
    # 1. Naming convention
    if not re.match(r'^(shihan|deshi)-[a-z-]+\.md$', name):
        errors.append("命名規則違反: (shihan|deshi)-[a-z-]+.md に一致させる必要があります。")
    
    content = file_path.read_text(encoding='utf-8')
    
    if is_draft(content):
        print(f"⚠️  {file_path} is a draft, skipping validation.")
        return []

    # 2. Frontmatter
    success, result = validate_frontmatter(content, file_path)
    if not success:
        errors.append(result)
    
    # 3. Common content checks
    validate_common(content, errors)
        
    return errors

def validate_skill(dir_path):
    errors = []
    name = dir_path.name
    
    # 1. Naming convention
    if not re.match(r'^(proc|action)-[a-z-]+-skill$', name):
        errors.append("命名規則違反: (proc|action)-[a-z-]+-skill に一致させる必要があります。")
    
    skill_md = dir_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md が見つかりません。")
        return errors
    
    content = skill_md.read_text(encoding='utf-8')
    
    if is_draft(content):
        print(f"⚠️  {dir_path.name} is a draft, skipping validation.")
        return []

    # 2. Frontmatter
    success, result = validate_frontmatter(content, skill_md)
    if not success:
        errors.append(result)
    
    # 3. Common content checks
    validate_common(content, errors)
        
    return errors

def main():
    root = Path(".")
    agents_dir = root / "agents"
    skills_dir = root / "skills"
    
    total_errors = 0
    
    print("--- 構成検証開始 (Claude Code Best Practices) ---")
    
    if agents_dir.exists():
        print(f"\n[Agents] {agents_dir}")
        for agent_file in sorted(agents_dir.glob("*.md")):
            errors = validate_agent(agent_file)
            if errors:
                print(f"❌ {agent_file}")
                for err in errors:
                    print(f"  - {err}")
                total_errors += len(errors)
            else:
                print(f"✅ {agent_file}")
                
    if skills_dir.exists():
        print(f"\n[Skills] {skills_dir}")
        for skill_path in sorted(skills_dir.iterdir()):
            if skill_path.is_dir():
                errors = validate_skill(skill_path)
                if errors:
                    print(f"❌ {skill_path.name}")
                    for err in errors:
                        print(f"  - {err}")
                    total_errors += len(errors)
                else:
                    print(f"✅ {skill_path.name}")

    print("\n--- 検証結果 ---")
    if total_errors > 0:
        print(f"合計 {total_errors} 個のエラーが見つかりました。")
        sys.exit(1)
    else:
        print("すべての構成がベストプラクティスに準拠しています。")
        sys.exit(0)

if __name__ == "__main__":
    main()
