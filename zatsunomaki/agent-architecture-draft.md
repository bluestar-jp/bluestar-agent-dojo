# AIエージェント全体設計案 (Draft)

## 1. サブエージェント分類定義

| カテゴリ | 役割概要 | 期待される動作 (Best Practice) | 代表例 (ID) |
| :--- | :--- | :--- | :--- |
| **オーケストレーター** | 戦略・設計・タスク分解 | ユーザーとの対話、Planの作成、他エージェントへのデリゲーション | `tech-lead`, `product-manager`, `editor-in-chief` |
| **スペシャリスト** | 実装・実行・専門解決 | 渡された仕様に基づくコード生成、特定ドメインの深い問題解決 | `coder-frontend`, `coder-backend`, `infra-ops`, `qa-engineer` |
| **ユーティリティ** | 単機能支援・高速処理 | どのレイヤーからも呼び出される汎用的タスク、定型処理の自動化 | `code-reviewer`, `git-operator`, `doc-generator` |

---

## 2. ディレクトリ構成と管理対象

各ディレクトリがAIエージェントの「どの要素」を制御するかを定義します。

| ディレクトリ | 管理対象 | プログレッシブディスクロージャーの観点 | 備考 |
| :--- | :--- | :--- | :--- |
| **`rules/`** | 行動規範・制約 | **[Must Load]** 全エージェントが最初に読み込むべき「掟」。レイヤーに応じて段階的に制約を強化。 | `constitution.md` 等 |
| **`agents/`** | ペルソナ・システムプロンプト | **[On Demand]** 必要になったタイミングで「人格」としてロード。メモリ消費と干渉を防ぐ。 | カテゴリ別にサブフォルダ化 |
| **`skills/`** | 手順(SOP)・ツール操作 | **[Explicit Use]** `activate_skill` 等で、特定の作業フェーズのみに適用される機能。 | Git操作、デプロイ手順等 |
| **`knowledge/`** | 知識ベース・コンテキスト | **[Reference Only]** 必要な時だけ検索・参照されるドメイン知識や用語集。 | `toranomaki/` に昇格あり |

---

## 3. 各AIツールのベストプラクティス適用イメージ

| ツール | 適用のポイント | 本設計での活用法 |
| :--- | :--- | :--- |
| **Gemini CLI** | `activate_skill` による機能のオンデマンド有効化 | `skills/` 配下のドキュメントをスキルとして定義し、必要な時だけ呼び出す。 |
| **Claude Code** | `.clauderc` や `CLAUDE.md` による文脈制御 | `rules/` の内容を `.clauderc` に注入し、エージェントの挙動を厳格に律する。 |
| **Cursor / Copilot** | `.cursorrules` 等によるインライン制約 | `rules/coding-style.md` をプロジェクトルートに配置し、常に開発者の隣で機能させる。 |

---

## 4. プログレッシブディスクロージャーの流れ (ワークフロー例)

| フェーズ | ロードされる情報 (段階的開示) | 主体エージェント |
| :--- | :--- | :--- |
| **1. 相談・要件** | `rules/constitution.md` | `product-manager` |
| **2. 計画・設計** | `rules/orchestrator/` + `toranomaki/grand-design.md` | `tech-lead` |
| **3. 実装・テスト** | `agents/specialist/` + `rules/specialist/` | `coder-xxx`, `qa-engineer` |
| **4. コミット・完了** | `skills/git/` | `git-operator` |