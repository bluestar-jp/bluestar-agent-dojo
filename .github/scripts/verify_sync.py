#!/usr/bin/env python3
"""
SoT（agents/, skills/）とアダプター（.claude/, .gemini/）の同期を検証
"""
import re
import sys
from pathlib import Path


def is_draft(content: str) -> bool:
    """
    Frontmatter内のdraft: trueフラグ、またはTODO:マーカーでドラフト状態を判定。
    - Frontmatterがあり draft: true → ドラフト
    - Frontmatterがない かつ TODO:を含む → ドラフト（後方互換）
    - コンテンツ内に「TODO:」が含まれる（Frontmatter外） → ドラフト（後方互換）
    """
    # Frontmatterの抽出
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)

    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        body = content[frontmatter_match.end():]

        # Frontmatter内のdraft: trueをチェック
        if re.search(r'^draft:\s*true\s*$', frontmatter, re.MULTILINE):
            return True

        # 後方互換: 本文内にTODO:があればドラフト
        if "TODO:" in body:
            return True

        return False
    else:
        # Frontmatterがない場合は後方互換でTODO:チェック
        return "TODO:" in content


def verify_sync():
    root = Path(".")
    agents_dir = root / "agents"
    skills_dir = root / "skills"

    gemini_agents = root / ".gemini" / "agents"
    gemini_skills = root / ".gemini" / "skills"
    claude_agents = root / ".claude" / "agents"
    claude_skills = root / ".claude" / "skills"

    errors = []

    # 1. エージェントのチェック
    if agents_dir.exists():
        for sot_file in agents_dir.glob("*.md"):
            if not sot_file.is_file():
                continue
            content = sot_file.read_text()
            if is_draft(content):
                continue

            name = sot_file.name
            ref_string = f"@agents/{name}"

            # Gemini のチェック
            g_adapter = gemini_agents / name
            if not g_adapter.exists():
                errors.append(f"[Missing Gemini Agent Adapter] {g_adapter}")
            elif not g_adapter.is_file():
                errors.append(f"[Invalid Adapter Type (Dir expected File)] {g_adapter}")
            elif ref_string not in g_adapter.read_text():
                errors.append(f"[Invalid Reference in Gemini Agent] {g_adapter} (Expected: {ref_string})")

            # Claude のチェック
            c_adapter = claude_agents / name
            if not c_adapter.exists():
                errors.append(f"[Missing Claude Agent Adapter] {c_adapter}")
            elif not c_adapter.is_file():
                errors.append(f"[Invalid Adapter Type (Dir expected File)] {c_adapter}")
            elif ref_string not in c_adapter.read_text():
                errors.append(f"[Invalid Reference in Claude Agent] {c_adapter} (Expected: {ref_string})")

    # 2. スキルのチェック（ディレクトリ形式）
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            sot_file = skill_dir / "SKILL.md"
            if not sot_file.exists():
                continue
            content = sot_file.read_text()
            if is_draft(content):
                continue

            skill_slug = skill_dir.name
            ref_string = f"@skills/{skill_slug}/SKILL.md"

            # Gemini のチェック (ディレクトリベース)
            g_adapter_dir = gemini_skills / skill_slug
            g_adapter_file = g_adapter_dir / "SKILL.md"
            if not g_adapter_file.exists():
                errors.append(f"[Missing Gemini Skill Adapter] {g_adapter_file}")
            elif not g_adapter_file.is_file():
                errors.append(f"[Invalid Adapter Type (Dir expected File)] {g_adapter_file}")
            elif ref_string not in g_adapter_file.read_text():
                errors.append(f"[Invalid Reference in Gemini Skill] {g_adapter_file} (Expected: {ref_string})")

            # Claude のチェック (ディレクトリベース)
            c_adapter_dir = claude_skills / skill_slug
            c_adapter_file = c_adapter_dir / "SKILL.md"
            if not c_adapter_file.exists():
                errors.append(f"[Missing Claude Skill Adapter] {c_adapter_file}")
            elif not c_adapter_file.is_file():
                errors.append(f"[Invalid Adapter Type (Dir expected File)] {c_adapter_file}")
            elif ref_string not in c_adapter_file.read_text():
                errors.append(f"[Invalid Reference in Claude Skill] {c_adapter_file} (Expected: {ref_string})")

    if errors:
        print("\n❌ Dojo Sync Verification Failed!", flush=True)
        for err in errors:
            print(f"  - {err}", flush=True)
        sys.exit(1)
    else:
        print("\n✅ All active (non-draft) Agents and Skills are perfectly synced.", flush=True)
        sys.exit(0)


if __name__ == "__main__":
    verify_sync()
