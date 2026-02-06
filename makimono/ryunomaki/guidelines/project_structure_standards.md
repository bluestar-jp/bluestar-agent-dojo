# プロジェクト構造化標準 (Project Structure Standards)

本プロジェクトにおける `agents/`, `skills/`, `makimono/` の役割定義と記載フォーマットの標準仕様です。
一貫性を保ち、AIエージェントと人間双方にとって理解しやすいナレッジベースを構築することを目的とします。

## 1. サブエージェント (Agents)

**ディレクトリ**: `agents/`

エージェントは「特定の専門性を持った人格（ペルソナ）」であり、自律的に思考し、スキルやツールを組み合わせてタスクを遂行します。

### 1.1 命名規則

- **ファイル名**: `(shihan|deshi)-[role].md`
  - `shihan`: 計画、判断、統合を行う指揮官・上級者。
  - `deshi`: 特定領域の作業を実行する専門家・実務者。
  - 例: `shihan-code-review.md`, `deshi-frontend-reviewer.md`

### 1.2 ファイルフォーマット

Frontmatter によるメタデータ定義と、本文による振る舞いの定義が必要です。

```markdown
---
name: [agent-name] (ファイル名から拡張子を除いたもの)
description: [概要] 1-2文でエージェントの役割を説明。
tools: [Tool1, Tool2, ...] (使用可能な基本ツール)
skills: 
  - [skill-name] (使用するカスタムスキル)
---

# [Agent Name]

- **Purpose**: [目的] 何のために存在するのか。
- **Scope**: [範囲] 何を担当し、何を担当しないのか。

## ワークフロー (Workflow)

エージェントが実行すべき思考・行動プロセス。
1. **認知**: 入力を分析する。
2. **計画**: 方針を立てる。
3. **実行**: ツールやスキルを使用する。
4. **検証**: 結果を確認する。

## 知識ソース (Knowledge Sources)

参照すべき `makimono` や外部ドキュメント。
```

---

## 2. エージェントスキル (Skills)

**ディレクトリ**: `skills/[type]-[action]-skill/`

スキルは「特定のタスクを遂行するための手順とツールのパッケージ」です。エージェントによって呼び出されます。

### 2.1 命名規則

- **ディレクトリ名**: `(proc|action)-[action]-skill`
  - `proc` (Procedure): 複数の工程を含む複合プロセス（例：開発フロー全体、インポート作業）。
  - `action` (Action): 単一の明確なタスク（例：コードレビュー、テスト実行、差分抽出）。
  - 例: `proc-structured-dev-skill`, `action-git-delivery-skill`

### 2.2 ディレクトリ構造

```text
skills/my-skill/
├── SKILL.md          (必須: 定義本体)
├── README.md         (推奨: 人間向け説明)
├── scripts/          (任意: 実行スクリプト)
└── references/       (任意: 参照資料)
```

### 2.3 ファイルフォーマット (`SKILL.md`)

```markdown
---
name: [skill-name] (ディレクトリ名から -skill を除いたもの推奨)
description: [概要] スキルの機能を簡潔に記述。
disable-model-invocation: [true/false] (任意: モデル呼び出し制限)
---

# [Skill Title]

- **Purpose**: [目的]
- **Scope**: [範囲]

## ワークフロー (Workflow) / 実行手順 (Procedure)

ステップバイステップの実行手順。
1. Step 1
2. Step 2

## 使用例 (Usage)

エージェントやユーザーがこのスキルをどう呼び出すか。
```

---

## 3. 巻物 (Makimono)

**ディレクトリ**: `makimono/`

プロジェクトの知識ベースです。目的に応じて3つのサブディレクトリに分類されます。

### 3.1 分類

| 分類 | ディレクトリ | 役割 | 内容の例 |
| :--- | :--- | :--- | :--- |
| **竜の巻** | `ryunomaki/` | **概念・方針 (Why/What)** | ガイドライン、ベストプラクティス、設計思想、仕様書 |
| **虎の巻** | `toranomaki/` | **手順・手法 (How)** | 具体的な手順書、ワークフロー、テンプレート、判断基準 |
| **免許皆伝** | `menkyokaiden/` | **メタ情報・公開 (Meta)** | プロジェクト外部向け情報、公開ガイド、README |

### 3.2 ファイルフォーマット

標準的な Markdown 形式を使用します。ファイル名のプレフィックス等の厳格な規則はありませんが、ディレクトリによる整理を推奨します。

```markdown
# [Title]

冒頭にドキュメントの概要・目的を記述する。

## [Section]

本文。
```

### 3.3 記載のポイント

- **Ryunomaki**: 抽象度を高く保ち、頻繁に変更されない普遍的なルールを書く。
- **Toranomaki**: 具体的かつ実行可能（Actionable）に書く。「これを読めば作業ができる」状態を目指す。
- **Menkyokaiden**: 第三者が読んでも理解できるように書く。

## 4. 共通ルール

- **言語**: 日本語を主言語とする。
- **文字コード**: UTF-8。
- **改行コード**: LF。
- **Markdown**: GitHub Flavored Markdown (GFM) 準拠。
