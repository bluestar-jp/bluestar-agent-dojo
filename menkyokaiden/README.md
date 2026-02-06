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

- `name`: エージェント名（kebab-case）
- `description`: いつ使うか明記

**推奨フィールド:**

- `tools`: 使用可能なツールを制限
- `skills`: プリロードするスキル

### 1.3 スキルのYAMLフロントマター

```yaml
---
name: backend-review
description: バックエンド観点でコード差分をレビューする。バックエンドコードのレビュー時に使用する。
---
```

**必須フィールド:**

- `name`: 簡潔な名前（slash commandになる）
- `description`: 「いつ使うか」を明記

**手順型スキル（proc-*）の追加フィールド:**

```yaml
---
name: creating-skills
description: スキル作成ワークフロー。
disable-model-invocation: true
---
```

- `disable-model-invocation: true`: ワークフロー実行スキルはユーザーが明示的に呼ぶ

### 1.4 ドラフト規約

未完成のエージェント/スキルは以下のいずれかでドラフト状態を表現:

1. **フロントマターで指定**: `draft: true`
2. **本文で明示**: `> **Status**: Draft - [理由]`

ドラフト状態のリソースは検証時にスキップされます。

## 2. 検証コマンド

### ローカル検証

```bash
# プラグイン構造の検証
make validate

# または直接実行
./scripts/validate-plugin.sh
```

### CI検証

```bash
# フロントマター検証
python .github/scripts/verify_plugin_sync.py
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
│   ├── proc-*-skill/            # 手順型
│   └── cond-*-skill/            # 条件判断型
├── .claude-plugin/
│   ├── plugin.json              # プラグインマニフェスト
│   └── marketplace.json         # マーケットプレイス登録情報
├── .claude/
│   ├── settings.json            # フック設定
│   └── settings.local.json      # ローカル開発用設定
├── menkyokaiden/
│   └── README.md                # 本ドキュメント
└── CLAUDE.md                    # Claude Code向けシステムプロンプト
```

## 5. 関連スキル

詳細なワークフローは以下のスキルを参照:

- `/menkyokaiden-claude`: Claude Code プラグインの設定・検証ワークフロー
- `/menkyokaiden-gemini`: Gemini Extensions の設定・検証ワークフロー（将来対応）
