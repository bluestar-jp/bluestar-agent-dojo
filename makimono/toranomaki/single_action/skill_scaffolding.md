# スキャフォールディング・テンプレート

新しいスキルを作成する際の初期コマンドセットです。

## ディレクトリ作成

```bash
mkdir -p {skill-name}/{scripts,references,assets}
```

## SKILL.md テンプレート

```markdown
---
name: {skill-name}
description: {A concise third-person description of what the skill does.}
---

# Instructions
{Provide clear, concise instructions for the agent.}

## Workflow
1. **Plan**: Analyze the input and present a plan.
2. **Execute**: Perform the task using available tools and scripts.
3. **Verify**: Validate the output against the requirements.

## Resources
- For detailed specs, see `references/SPEC.md`.
- Use `scripts/helper.py` for complex calculations.
```
