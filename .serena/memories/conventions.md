# Style and Conventions

## Communication

- **言語**: ユーザーへの最終出力は常に**日本語**。内部的な思考（Thought）は英語でも可。
- **態度**: プロフェッショナルかつ誠実。不確実な場合はハルシネーションを避け、確認を行う。

## Directory & Naming

- 知識型（龍の巻）: `makimono/ryunomaki/` 配下。スネークケース。
- 指示型（虎の巻）: `makimono/toranomaki/` 配下。スネークケース。
- エージェント/スキルSoT: `agents/`, `skills/` 配下。
- スキルの命名: `[type]-[action]-skill` 形式（例: `proc-creating-skills-skill`）。

## Documentation Style (Markdown)

- **ガイドライン**: `makimono/ryunomaki/guidelines/markdown_style.md` を厳守。
- **見出し**: ATX形式（`#`）を使用し、前後に空行。
- **リスト**: ハイフン（`-`）を使用。
- **コード**: 言語識別子を必須とし、フェンスコードブロックを使用。
- **日本語**: 英数字と日本語の間に半角スペースを推奨。

## Git & Commit

- **言語**: コミットメッセージは日本語。
- **形式**: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)。
- **署名**: `Co-Authored-By: gemini-cli <218195315+gemini-cli@users.noreply.github.com>` を必須とする。

## Agent Skill Best Practices

- `makimono/ryunomaki/guidelines/custom_agent_skill_best_practices.md` を参照。
- 認知負荷の最小化、ツール活用、計画と検証、自律性の制御を重視。
