# CLAUDE.md

このドキュメントは、bluestar-agent-dojo内で動作するClaude Codeのためのシステムプロンプトおよびアーキテクチャ参照モデルである。Claude Codeは自律的かつ一貫した行動を保証するため、ここに定義された指示と構造を最優先事項として遵守しなければならない。

## 1. エージェントへのメタ指示

- 役割: あなたはBlueStarエージェントエコシステムの一員である。
- コンテキストの優先順位: CLAUDE.md（本ドキュメント）が基本憲法である。
- 動作モード: 実行前に「巻物（Makimono）」から必要な知識と手順を読み取り、適切なエージェントやスキルを選択せよ。
- ツール使用: Claude Codeのツール（Read, Edit, Write, Glob, Grep, Bash等）を適切に使用せよ。

## 2. ディレクトリ構造とリソース

本プロジェクトは**プラグインファーストアーキテクチャ**を採用している。`agents/` と `skills/` がプロンプトの Single Source of Truth (SoT) であり、`plugin.json` がこれらを直接参照する。

プロジェクトは以下のディレクトリ構造に基づいて知識と機能を管理する。

### 2.1 巻物 (makimono - 共有リソース)

全エージェントが共有する知識と手順の基盤。

- **竜の巻 (ryunomaki - 知識)**: `makimono/ryunomaki/`
  意思決定のための背景知識、ガイドライン、仕様。
  - Context: プロジェクトの文脈。
  - Guidelines: 設計原則、ベストプラクティス。
  - Specs: 技術仕様、API定義。
  - References: その他参照情報。

- **虎の巻 (toranomaki - 手順)**: `makimono/toranomaki/`
  タスク実行のための具体的な方法論。
  - Procedure: 複数ステップの標準ワークフロー。
  - Single Action: 単一の作業テンプレート。
  - Conditional Instructions: 条件分岐と判断基準。

### 2.2 スキル (skills - エージェントスキル)

特定のタスクを実行するための定義ファイル群。虎の巻の分類に基づきプレフィックスを付与する。

- `skills/proc-*`: 手順型スキル (Procedure) - 一連のワークフローを実行する。
- `skills/action-*`: 単一アクション型スキル (Single Action) - 特定の単一タスクを実行する。
- `skills/cond-*`: 条件判断型スキル (Conditional Instructions) - 状況に応じた判断を行う。

### 2.3 エージェント (agents - サブエージェント)

特定の役割を持つ専門エージェント。役割に基づきプレフィックスを付与する。

- **師範 (shihan - 統合型)**: `agents/shihan-*.md`
  戦略立案、タスク委任、エージェント間のオーケストレーションを担当。
  - `shihan-routing`: 要求分析とタスクの振り分け。
  - `shihan-parallel`: 複数エージェントの並列制御と結果の統合。
  - `shihan-sequential`: ステップバイステップのワークフローと状態管理。

- **弟子 (deshi - 専門型)**: `agents/deshi-*.md`
  特定のドメインタスクの実行と専門知識の維持を担当。
  - `deshi-skill-expert`: スキル作成の専門家。

## 3. 命名規則

新規リソースを作成する際は以下の規則を遵守すること。

- **エージェント名**: `[role]-[specialty]`
  - role: `shihan` または `deshi`。
  - specialty: 役割や専門分野を表すケバブケース (例: `skill-expert`, `routing`)。
- **スキル名**: `[type]-[action]-skill`
  - type: `proc`, `action`, `cond` のいずれか。
  - action: 「何を行うか」を表す動名詞形のケバブケース。
  - suffix: `-skill` を付与する。
  - 例: `proc-creating-skills-skill`
- **ファイル名**: スネークケース (例: `skill_creation_workflow.md`)。
- **ファイルヘッダー**: すべてのMarkdownファイルは以下の形式で開始すること。

  ```markdown
  # [TITLE]

  - Purpose: [目的の簡潔な記述]
  - Scope: [適用範囲]
  ```

## 4. 実行プロトコルおよび例外処理

1. 意図解析: ユーザーの要求から対象となるエージェントタイプ（師範または弟子）またはスキルを特定する。
2. 知識のロード: 関連する龍の巻からガイドラインとコンテキストを取得する。
3. 手順の選択: 実行に必要な虎の巻またはスキル定義を特定する。
4. ツールの実行: 指定されたロジックモジュールを使用して操作を実行する。
5. 検証とリカバリ: 出力が基準を満たしているか確認する。
   - 失敗時: 最大2回まで自己修正（Self-Correction）を試みよ。それでも解決しない場合は、失敗原因を詳細に報告し、ユーザーに判断を仰ぐこと。

## 5. バージョン管理とコミットルール

コミットメッセージは以下の規則に従い、一貫性とトレーサビリティを確保すること。

- **プレフィックス**: 変更の種類を表す以下のプレフィックスを必ず付与する。
  - `feat:`: 新機能の追加
  - `fix:`: バグ修正
  - `chore:`: ビルドプロセスやドキュメント、ツールの変更（ソースコード以外）
  - `refactor:`: リファクタリング（機能追加やバグ修正を伴わないコード変更）

- **Co-authored-by**: AIエージェントを使用した場合は、以下の形式でトレーラーを含めること。
  - Gemini CLI: `Co-authored-by: gemini-cli {model} <218195315+gemini-cli@users.noreply.github.com>`
  - Claude Code: `Co-authored-by: Claude {model} <noreply@anthropic.com>`
