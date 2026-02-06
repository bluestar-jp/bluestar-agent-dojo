# 免許皆伝 (Menkyokaiden) - プラグイン公開ガイド

このドキュメントは、bluestar-agent-dojo をAIエージェントプラグインとして公開・管理するための運用ガイドです。

## 概要

bluestar-agent-dojo は **プラグインファーストアーキテクチャ** を採用しています。

- `agents/` と `skills/` がプロンプトの Single Source of Truth (SoT)
- `plugin.json` がプラグインマニフェストとしてこれらを直接参照
- 各AIツール固有のアダプターレイヤーは不要

## 1. Claude Code Plugin の要件

### 1.1 plugin.json の必須フィールド

```json
{
  "name": "bluestar-dojo",
  "version": "1.0.0",
  "description": "自律型AIエージェントの道場プラグイン",
  "agents": "agents/",
  "skills": "skills/"
}
```

### 1.2 エージェントのYAMLフロントマター

```yaml
---
name: deshi-skill-expert
description: カスタムエージェントスキル作成を専門とする弟子エージェント。
tools: Read, Write, Edit, Glob, Grep, Bash
---
```

**必須フィールド:**

- `name`: エージェント名（ファイル名から拡張子を除いたものと一致させること）
- `description`: エージェントの役割と使用場面を明記

**推奨フィールド:**

- `tools`: 使用可能なツールを制限
- `skills`: プリロードするスキル

### 1.3 スキルのYAMLフロントマター

```yaml
---
name: action-backend-review-skill
description: バックエンド観点でコード差分をレビューする。
---
```

**必須フィールド:**

- `name`: スキル名（**ディレクトリ名と完全一致させること**）
- `description`: スキルの機能と使用場面を明記

**手順型スキル（proc-*）の追加フィールド:**

```yaml
---
name: proc-creating-skills-skill
description: スキル作成ワークフロー。
disable-model-invocation: true
---
```

- `disable-model-invocation: true`: ワークフロー実行スキルはユーザーが明示的に呼ぶ場合に設定

### 1.4 ドラフト規約

未完成のエージェント/スキルは以下のいずれかでドラフト状態を表現:

1. **フロントマターで指定**: `draft: true`
2. **本文で明示**: `> **Status**: Draft - [理由]`

ドラフト状態のリソースは検証時にスキップされます。

## 2. 検証コマンド

### 自動検証 (Lefthook)

コミット時に以下の検証が自動実行されます:

- Markdown Lint (`markdownlint`)
- 構成・ベストプラクティス検証 (`verify-best-practices.py`)
- プラグイン構造検証 (`validate-plugin.sh`)
- コミットメッセージ規約 (`feat:`, `fix:` 等)

### 手動検証

```bash
# 全体の構成検証 (ベストプラクティス準拠確認)
python3 scripts/verify-best-practices.py

# プラグイン構造の検証
sh scripts/validate-plugin.sh
# または
make validate
```

## 3. バージョン管理・リリース手順

### バージョン更新

```bash
# パッチバージョン (1.0.0 → 1.0.1)
make patch

# マイナーバージョン (1.0.0 → 1.1.0)
make minor

# メジャーバージョン (1.0.0 → 2.0.0)
make major
```

### リリース

```bash
make release
```

## 4. ディレクトリ構成

```text
bluestar-agent-dojo/
├── agents/                      # エージェント定義（SoT）
│   ├── deshi-*.md               # 弟子エージェント
│   └── shihan-*.md              # 師範エージェント
├── skills/                      # スキル定義（SoT）
│   ├── action-*-skill/          # 単一アクション型
│   └── proc-*-skill/            # 手順型
├── .claude-plugin/
│   ├── plugin.json              # プラグインマニフェスト
│   └── marketplace.json         # マーケットプレイス登録情報
├── menkyokaiden/
│   └── README.md                # 本ドキュメント
└── CLAUDE.md                    # Claude Code向けシステムプロンプト
```

## 5. 関連スキル

詳細なワークフローは以下のスキルを参照:

- `proc-menkyokaiden-claude-skill`: Claude Code プラグインの設定・検証ワークフロー
- `proc-menkyokaiden-gemini-skill`: Gemini Extensions の設定・検証ワークフロー
