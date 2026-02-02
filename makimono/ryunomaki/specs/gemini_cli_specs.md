# Gemini CLI スキル技術仕様 (Technical Specs)

Gemini CLI環境でスキルを実装するための具体的な技術要件です。

## ディレクトリ構造
```
skill-name/
├── SKILL.md      # エントリーポイント（必須）
├── scripts/      # 実行可能スクリプト（推奨）
├── references/   # 静的ドキュメント
└── assets/       # テンプレート・素材
```

## SKILL.md フォーマット
YAMLフロントマターとMarkdownボディで構成されます。

### フロントマター
```yaml
---
name: skill-name-kebab-case
description: 三人称での簡潔な説明（CLIがスキルを選択する判断基準になります）。
---
```

### 命名規則
- **スキル名**: `[type]-[action]-skill` の形式。
  - type: `proc`, `action`, `cond`
  - action: 動名詞形のケバブケース
  - suffix: `-skill` を必須とする
- **ファイル名**: 小文字、アンダースコアまたはハイフン。
