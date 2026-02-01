# BlueStar Agent Dojo

BlueStar社におけるAIエージェントの定義、設計、および設定を一元管理するリポジトリ（道場）です。
特定のAIツール（Gemini CLI, Claude Code, Cursor, GitHub Copilot等）に依存しない「コア定義」を管理し、そこから各ツールへの適用を行います。

## ディレクトリ構造

### `core/` (Single Source of Truth)
特定のツールに依存しない、エージェントの「人格」「役割」「ルール」のマスターデータです。
- **prompts/**: 各エージェントのシステムプロンプト（Markdown形式）。
- **rules/**: 全エージェントが遵守すべき共通憲法（Constitution）。
- **context/**: 会社情報、用語集、プロジェクト背景などの共通コンテキスト。

### `integrations/` (Adapters)
`core` の定義を各AIツールの仕様に合わせて変換・配置するための設定ファイル群です。
- **gemini-cli/**: `.gemini/` ディレクトリ用の設定。
- **claude-code/**: Claude Code用の設定。
- **cursor/**: Cursorエディタ用の `.cursorrules` など。
- **vscode-copilot/**: GitHub Copilot用のInstructions。

### `design/`
人間向けの設計ドキュメント、アーキテクチャ図、要件定義書。

## 運用フロー
1. **設計**: `design/` でエージェントの役割を定義する。
2. **実装**: `core/prompts/` に自然言語でプロンプトを作成する。
3. **適用**: `integrations/` 以下の各ツール設定に反映させる（将来的にスクリプトで自動化予定）。
