#!/usr/bin/env python3
"""
プラグインマニフェストとSoT（agents/, skills/）のフロントマターを検証
"""
import re
import sys
from pathlib import Path


def is_draft(content: str) -> bool:
    """
    Frontmatter内のdraft: trueフラグ、またはStatus: Draftでドラフト状態を判定。
    - Frontmatterがあり draft: true → ドラフト
    - Frontmatterがない → ドラフト（未完成とみなす）
    - 本文内に「> **Status**: Draft」が含まれる → ドラフト
    """
    # Frontmatterの抽出
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)

    if not frontmatter_match:
        # Frontmatterがない場合はドラフト扱い
        return True

    frontmatter = frontmatter_match.group(1)
    body = content[frontmatter_match.end():]

    # Frontmatter内のdraft: trueをチェック
    if re.search(r'^draft:\s*true\s*$', frontmatter, re.MULTILINE):
        return True

    # 本文内の Draft ステータスをチェック
    if "> **Status**: Draft" in body:
        return True

    return False


def verify_plugin_sync():
    root = Path(".")
    errors = []

    # 1. plugin.json の存在確認
    plugin_json = root / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        errors.append("[Missing] .claude-plugin/plugin.json")
        print("❌ Plugin manifest not found")
        sys.exit(1)

    # 2. agents/ の全ファイルを取得（ドラフト除外）
    agents_dir = root / "agents"
    active_agents = []
    if agents_dir.exists():
        for f in agents_dir.glob("*.md"):
            content = f.read_text()
            if not is_draft(content):
                active_agents.append(f.stem)

    # 3. skills/ の全ディレクトリ/ファイルを取得（ドラフト除外）
    skills_dir = root / "skills"
    active_skills = []
    if skills_dir.exists():
        # ディレクトリ形式
        for d in skills_dir.iterdir():
            if d.is_dir():
                skill_md = d / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text()
                    if not is_draft(content):
                        active_skills.append(d.name)
        # ファイル形式（後方互換）
        for f in skills_dir.glob("*.md"):
            content = f.read_text()
            if not is_draft(content):
                active_skills.append(f.stem)

    # 4. フロントマターの存在確認
    for agent in active_agents:
        agent_file = agents_dir / f"{agent}.md"
        content = agent_file.read_text()
        if not content.startswith("---"):
            errors.append(f"[Missing Frontmatter] agents/{agent}.md")

    for skill in active_skills:
        skill_dir = skills_dir / skill
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
        else:
            skill_file = skills_dir / f"{skill}.md"
        if skill_file.exists():
            content = skill_file.read_text()
            if not content.startswith("---"):
                errors.append(f"[Missing Frontmatter] {skill_file}")

    # 5. 結果出力
    if errors:
        print("❌ Plugin Sync Verification Failed!")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"✅ Plugin sync verified: {len(active_agents)} agents, {len(active_skills)} skills")
        sys.exit(0)


if __name__ == "__main__":
    verify_plugin_sync()
