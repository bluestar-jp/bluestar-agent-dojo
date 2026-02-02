import sys
from pathlib import Path

def verify_sync():
    root = Path(".")
    agents_dir = root / "agents"
    skills_dir = root / "skills"
    
    gemini_agents = root / ".gemini" / "agents"
    gemini_skills = root / ".gemini" / "skills"
    claude_agents = root / ".claude" / "agents"
    claude_skills = root / ".claude" / "skills"
    
    errors = []

    # 1. Check Agents
    if agents_dir.exists():
        for sot_file in agents_dir.glob("*.md"):
            if not sot_file.is_file():
                continue
            content = sot_file.read_text()
            if "TODO:" in content:
                continue
                
            name = sot_file.name
            ref_string = f"@agents/{name}"
            
            # Gemini check
            g_adapter = gemini_agents / name
            if not g_adapter.exists():
                errors.append(f"[Missing Gemini Agent Adapter] {g_adapter}")
            elif not g_adapter.is_file():
                errors.append(f"[Invalid Adapter Type (Dir expected File)] {g_adapter}")
            elif ref_string not in g_adapter.read_text():
                errors.append(f"[Invalid Reference in Gemini Agent] {g_adapter} (Expected: {ref_string})")

            # Claude check
            c_adapter = claude_agents / name
            if not c_adapter.exists():
                errors.append(f"[Missing Claude Agent Adapter] {c_adapter}")
            elif not c_adapter.is_file():
                errors.append(f"[Invalid Adapter Type (Dir expected File)] {c_adapter}")
            elif ref_string not in c_adapter.read_text():
                errors.append(f"[Invalid Reference in Claude Agent] {c_adapter} (Expected: {ref_string})")

    # 2. Check Skills
    if skills_dir.exists():
        for sot_file in skills_dir.glob("*.md"):
            if not sot_file.is_file():
                continue
            content = sot_file.read_text()
            if "TODO:" in content:
                continue

            name = sot_file.name
            skill_slug = sot_file.stem # e.g. proc-creating-skills-skill
            ref_string = f"@skills/{name}"
            
            # Gemini check (Directory based)
            g_adapter_dir = gemini_skills / skill_slug
            g_adapter_file = g_adapter_dir / "SKILL.md"
            if not g_adapter_file.exists():
                errors.append(f"[Missing Gemini Skill Adapter] {g_adapter_file}")
            elif not g_adapter_file.is_file():
                errors.append(f"[Invalid Adapter Type (Dir expected File)] {g_adapter_file}")
            elif ref_string not in g_adapter_file.read_text():
                errors.append(f"[Invalid Reference in Gemini Skill] {g_adapter_file} (Expected: {ref_string})")

            # Claude check
            c_adapter = claude_skills / name
            if not c_adapter.exists():
                errors.append(f"[Missing Claude Skill Adapter] {c_adapter}")
            elif not c_adapter.is_file():
                errors.append(f"[Invalid Adapter Type (Dir expected File)] {c_adapter}")
            elif ref_string not in c_adapter.read_text():
                errors.append(f"[Invalid Reference in Claude Skill] {c_adapter} (Expected: {ref_string})")

    if errors:
        print("\n❌ Dojo Sync Verification Failed!", flush=True)
        for err in errors:
            print(f"  - {err}", flush=True)
        sys.exit(1)
    else:
        print("\n✅ All active (non-TODO) Agents and Skills are perfectly synced.", flush=True)
        sys.exit(0)

if __name__ == "__main__":
    verify_sync()
