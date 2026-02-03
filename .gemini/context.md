# bluestar-agent-dojo プロジェクトコンテキスト

## プロジェクト概要

AIエージェントとスキルのためのプロンプト管理リポジトリ（道場）。Claude CodeとGemini CLIの両方に対応した、Source of Truth（SoT）原則に基づくエージェント/スキルフレームワークを提供します。

## 技術スタック

- **言語**: Markdown, Python, Bash
- **AIツール**: Claude Code, Gemini CLI
- **バージョン管理**: Git

## アーキテクチャ原則

### SoT原則（Source of Truth）

- **実体とアダプターの分離**: 実体は `skills/`, `agents/` に配置し、アダプターは `.gemini/`, `.claude/` に配置
- **参照による統一**: アダプターは `@path/to/sot.md` で実体を参照
- **重複排除**: 同じ内容を複数箇所に書かない

### 命名規則

- **エージェント**: `[role]-[specialty]` （例: `deshi-code-reviewer`, `shihan-routing`）
- **スキル**: `[type]-[action]-skill` （例: `proc-reviewing-code-skill`, `action-format-output-skill`）
  - type: `proc` (Procedure), `action` (Single Action), `cond` (Conditional Instructions)
- **ファイル**: スネークケース （例: `security_review.md`, `parallel_review.sh`）

### ディレクトリ構造

```
bluestar-agent-dojo/
├── makimono/                    # 共有知識と手順
│   ├── ryunomaki/               # 龍の巻（知識）
│   └── toranomaki/              # 虎の巻（手順）
├── skills/                      # スキル実体
│   ├── proc-*/                  # 手順型スキル
│   ├── action-*/                # 単一アクション型スキル
│   └── cond-*/                  # 条件判断型スキル
├── agents/                      # エージェント実体
│   ├── shihan-*/                # 師範（統合型）
│   └── deshi-*/                 # 弟子（専門型）
├── .gemini/                     # Gemini CLIアダプター
│   ├── skills/
│   └── agents/
└── .claude/                     # Claude Codeアダプター
    ├── skills/
    └── agents/
```

## レビュー時の注意事項

### コーディング規約

- **Markdown**: すべてのMarkdownファイルは末尾に単一の改行（LF）を持つこと（MD047準拠）
- **Python**: PEP 8スタイルガイドに従う
- **Bash**: ShellCheckの警告に対応する
- **実行権限**: スクリプトファイルには適切な実行権限（chmod +x）を付与する

### コミットメッセージ規約

プレフィックスを必ず使用すること：

- `feat:` - 新機能の追加
- `fix:` - バグ修正
- `chore:` - ビルドプロセスやドキュメント、ツールの変更
- `refactor:` - リファクタリング（機能追加やバグ修正を伴わない）

Co-authored-by トレーラーを含めること：

- Gemini CLI使用時: `Co-authored-by: gemini-cli {model} <218195315+gemini-cli@users.noreply.github.com>`
- Claude Code使用時: `Co-authored-by: Claude {model} <noreply@anthropic.com>`

### ファイル構造

すべてのMarkdownファイルは以下の形式で開始すること：

```markdown
# [TITLE]

- Purpose: [目的の簡潔な記述]
- Scope: [適用範囲]
```

## プロジェクト固有の文脈

### 設計哲学

1. **認知負荷の最小化**: 各ファイルは簡潔に保ち、詳細は別ファイルに分離
2. **ツールへのオフロード**: 複雑なロジックはスクリプト化し、確実性を担保
3. **Medium Autonomy**: 手順は明確に、解釈には柔軟性を持たせる
4. **コンテキストの独立性**: 各スキル/エージェントは独立して動作可能にする

### 自律性レベル

- **Low Autonomy**: スクリプト化された確定的な処理
- **Medium Autonomy**: ガイドラインに基づく判断が必要な処理
- **High Autonomy**: 完全に自由な解釈と対応が可能な処理

## セキュリティとプライバシー

- **機密情報**: APIキー、パスワード、秘密鍵はコードに含めない
- **環境変数**: 機密情報は環境変数から読み込む
- **ログ**: 機密情報をログに出力しない
- **.gitignore**: 機密ファイルが適切に除外されているか確認

## パフォーマンス考慮事項

- **差分サイズ**: 1000行を超える差分は警告を表示
- **並列実行**: 可能な限り並列処理を活用
- **タイムアウト**: 長時間実行を防ぐためタイムアウトを設定
- **キャッシュ**: 重複するAPI呼び出しを避ける

## 依存関係

### 必須ツール

- Git: バージョン管理
- Gemini CLI: コードレビューエンジン
- jq: JSON処理
- timeout: プロセス制御（GNU coreutils）
- Python 3: スクリプト実行

### オプションツール

- Claude Code: オーケストレーション
- ShellCheck: シェルスクリプト静的解析
- markdownlint: Markdown lint
