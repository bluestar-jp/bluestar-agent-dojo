# Suggested Commands

## Environment & Development

- **環境操作 (container-use)**:
  - 作成: `container-use create --source . --title "Task Name"`
  - ログ: `container-use log <env_id>`
  - 適用: `container-use checkout <env_id>`

## Verification & Linting

- **構成検証**: `python3 scripts/verify-best-practices.py`
- **プラグイン検証**: `sh scripts/validate-plugin.sh`
- **Markdown Lint**: `sh scripts/lint-markdown.sh`
- **バージョン更新**: `sh scripts/bump-version.sh <new_version>`

## Specialized Skill Scripts

- **インポート関連**: `skills/proc-importing-skill/scripts/` 内の各Pythonスクリプト。
- **レビュー関連**: `skills/proc-reviewing-code-skill/scripts/` 内の各スクリプト。

## Git Workflow

- `git status`
- `git diff HEAD`
- `git add .`
- `git commit -m "prefix: message"`
- `git push origin main`

## Entrypoints

- **エージェント**: `agents/` 配下のMarkdown。
- **スキル**: `skills/` 配下の各ディレクトリにある `SKILL.md`。
- **巻物**: `makimono/` 配下。
