# Style and Conventions

## Communication

- **言語**: ユーザーへの最終出力は常に**日本語**。内部的な思考（Thought）は英語でも可。
- **態度**: プロフェッショナルかつ誠実。不確実な場合はハルシネーションを避け、確認を行う。

## Directory & Naming

- **エージェント名**: `[role]-[specialty]` (例: `shihan-routing`, `deshi-skill-expert`)
- **スキル名**: `[type]-[action]-skill` (例: `proc-creating-skills-skill`)
- **ファイル名**: スネークケース (例: `skill_creation_workflow.md`)。
- **巻物**: `makimono/ryunomaki/` (知識), `makimono/toranomaki/` (手順)。

## Documentation Style (Markdown)

- すべてのMarkdownファイルは `# [TITLE]`、`- Purpose: ...`、`- Scope: ...` で開始する。
- `makimono/ryunomaki/guidelines/markdown_style.md` を厳守。
- ATX形式（`#`）の見出し、ハイフン（`-`）のリストを使用。
- 言語識別子付きのフェンスコードブロックを使用。

## Git & Commit

- **形式**: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`)。
- **言語**: コミットメッセージは日本語。
- **Co-authored-by**: AIエージェント使用時は以下を含める。
  - Gemini CLI: `Co-authored-by: gemini-cli {model} <218195315+gemini-cli@users.noreply.github.com>`
  - Claude Code: `Co-authored-by: Claude {model} <noreply@anthropic.com>`

## Agent Skill Best Practices

- `makimono/ryunomaki/guidelines/custom_agent_skill_best_practices.md` を参照。
- 認知負荷の最小化、ツール活用、計画と検証、自律性の制御。
