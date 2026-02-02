# Suggested Commands

## Environment & Development

- **環境操作**:
  - 作成: `container-use create --source . --title "Task Name"`
  - ログ: `container-use log <env_id>`
  - 適用: `container-use checkout <env_id>`

## Verification & Linting

- **同期検証**: `python3 scripts/verify_sync.py`
- **Markdown Lint**: `markdownlint "**/*.md"` (または GitHub Actions による自動チェック)

## File Operations (Darwin)

- **検索**: `grep -r "pattern" .`
- **構造**: `ls -R`
- **ファイル作成**: `touch path/to/file`

## Git Workflow

- **状態**: `git status`
- **差分**: `git diff HEAD`
- **コミット**: `git add . && git commit -m "prefix: message"`
- **プッシュ**: `git push origin main`

## Entrypoints

- エージェントの起点: `agents/` 内の各Markdownファイル。
- スキルの起点: `skills/` 内の各Markdownファイル。
