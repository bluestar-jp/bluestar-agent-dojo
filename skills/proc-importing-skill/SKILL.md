---
name: proc-importing-skill
description: 外部リポジトリやコミュニティから良質なスキル・エージェント定義を取得し、bluestar-agent-dojoの構造に適合させて統合する。
---

# External Skill/Agent Import Skill

- Purpose: 外部リポジトリやコミュニティから良質なスキル・エージェント定義を取得し、bluestar-agent-dojoの構造に適合させて統合する
- Scope: GitHub、公開リポジトリ、URLから取得可能な定義ファイルの変換と統合

## 概要

このスキルは、外部で設計・構築されたスキルやサブエージェント定義を取得し、bluestar-agent-dojoの命名規則とディレクトリ構造に準拠した形式に変換します。既存リソースとの競合を検出し、適切なメタデータとドキュメントを生成します。

## ワークフロー (Plan → Agree → Execute → Verify)

### 1. Plan: 取得元の分析

まず、ユーザーが提供した取得元（URL、GitHubリポジトリ、ファイルパス）を分析します。

#### 情報収集

- 取得元のタイプを特定（GitHub URL、HTTP URL、ローカルパス）
- 定義ファイルの形式を推定（Markdown、JSON、YAML）
- リソースタイプを判定（スキルかエージェントか）

#### Claude Codeツールの使用

このスキルはスタンドアロンスクリプトとして設計されていますが、Claude Code環境で使用する場合は以下のツールを推奨します。

#### 外部URLからの取得

```python
# WebFetchツールを使用（推奨）
# Claude Codeのネイティブツールで安全にコンテンツを取得
from claude_tools import WebFetch

result = WebFetch(
    url="https://github.com/example/skill",
    prompt="スキル定義ファイルの内容を抽出してください"
)
```

#### ローカルファイルの読み込み

```python
# Readツールを使用（推奨）
# cat コマンドではなく、Readツールで安全に読み込み
from claude_tools import Read

content = Read(file_path="/path/to/skill/SKILL.md")
```

#### ファイル操作

```python
# Write/Editツールを使用（推奨）
# cp/mv コマンドではなく、専用ツールを使用
from claude_tools import Write, Edit

# 新規ファイル作成
Write(file_path="skills/imported-skill/SKILL.md", content=content)

# 既存ファイル編集
Edit(file_path="skills/imported-skill/SKILL.md",
     old_string="...", new_string="...")
```

#### スクリプト実行時の注意

このスキルのスクリプトは独立実行可能ですが、Claude Code環境では：

- Bashツールは git, gh, npm などのCLIツールの実行に限定
- ファイル操作は Read/Write/Edit ツールを優先
- Web取得は WebFetch ツールを優先

#### 計画の提示

- 取得するファイル一覧
- 推定されるリソースタイプ（proc-*, action-*, cond-*, shihan-*, deshi-*）
- 変換が必要な項目（命名規則、ディレクトリ構造）
- 既存リソースとの競合可能性

### 2. Agree: ユーザー確認

以下を提示してユーザーの合意を得る:

- **取得対象**: ファイル名、URL、サイズ
- **配置先**: `skills/` または `agents/` 配下の新規ディレクトリ名
- **命名規則の適用**: 元の名前 → 変換後の名前
- **競合チェック結果**: 既存の類似リソースがある場合は警告
- **実行可否**: ユーザーに進行の承認を求める

### 3. Execute: 取得と変換

#### 3.1 外部定義の取得

```bash
scripts/fetch-definition.py \
  --source "{URL or path}" \
  --type "{skill|agent}" \
  --output-dir /tmp/import_staging
```

#### 取得方法の選択

- GitHub: `gh` CLI または Git clone
- HTTPS: `curl` または WebFetch ツール
- ローカル: `cp` コマンドまたは Read ツール

#### 3.2 構造分析

取得した定義ファイルを解析し、以下を抽出します:

```python
# scripts/analyze-definition.py
{
  "resource_type": "skill|agent",
  "original_name": "...",
  "description": "...",
  "files": [...],
  "dependencies": [...],
  "autonomy_level": "high|medium|low"
}
```

#### 3.3 命名規則の適用

`references/naming-conversion.md` のルールに基づき変換:

#### スキルの場合の命名規則

- タイプ判定: Procedureか、Single Actionか、Conditional Instructionsか
- プレフィックス付与: `proc-`, `action-`, `cond-`
- サフィックス確認: `-skill` で終わっているか
- 例: `code-formatter` → `action-formatting-code-skill`

#### エージェントの場合の命名規則

- 役割判定: 師範（統合型）か、弟子（専門型）か
- プレフィックス付与: `shihan-`, `deshi-`
- 例: `orchestrator` → `shihan-orchestrator`

```bash
scripts/apply-naming.py \
  --input /tmp/import_staging/analysis.json \
  --output /tmp/import_staging/renamed.json
```

#### 3.4 ディレクトリ構造の変換

bluestar-agent-dojoの標準構造に適合させます:

#### スキルの場合のディレクトリ構造

```text
skills/{proc|action|cond}-{action}-skill/
├── SKILL.md (必須)
├── scripts/ (オプション)
├── references/ (オプション)
└── assets/ (オプション)
```

#### エージェントの場合のディレクトリ構造

```text
agents/{shihan|deshi}-{specialty}/
├── AGENT.md (必須)
├── rules/ (オプション)
├── knowledge/ (オプション)
├── verification/ (オプション)
└── collection/ (オプション)
```

```bash
scripts/convert-structure.py \
  --input /tmp/import_staging \
  --output /tmp/import_staging/converted \
  --config references/structure-template.json
```

#### 3.5 メタデータとドキュメントの生成

以下を自動生成または補完します:

- SKILL.md または AGENT.md のヘッダー（Purpose, Scope）
- 依存関係の明記
- 使用例の追加
- エラーハンドリングの記述

```bash
scripts/generate-metadata.py \
  --input /tmp/import_staging/converted \
  --template references/skill-template.md
```

#### 3.6 競合検出と回避

既存のスキル/エージェントと名前や機能が重複していないか確認:

```bash
# 名前の重複チェック
ls skills/ | grep -E "^{proposed-name}$"
ls agents/ | grep -E "^{proposed-name}$"

# 類似性チェック（descriptionの比較）
scripts/check-similarity.py \
  --new /tmp/import_staging/converted/SKILL.md \
  --existing skills/
```

#### 競合時の対応

- 完全一致: ユーザーに上書きまたはスキップを確認
- 類似性高い: 統合または別名での保存を提案
- 競合なし: そのまま配置

### 4. Verify: 統合と検証

#### 4.1 最終配置

```bash
# 変換済みリソースを本番ディレクトリに配置
cp -r /tmp/import_staging/converted/* \
  /Users/aono/develop/bluestar/bluestar-agent-dojo/
```

#### 4.2 構造検証

```bash
# ディレクトリ構造が正しいか確認
scripts/validate-structure.py \
  --path skills/{new-skill-name}

# SKILL.mdの必須フィールドを確認
grep -E "^- Purpose:" skills/{new-skill-name}/SKILL.md
grep -E "^- Scope:" skills/{new-skill-name}/SKILL.md
```

#### 4.3 依存関係の確認

```bash
# 外部ツールや未インストールパッケージをチェック
scripts/check-dependencies.py \
  --path skills/{new-skill-name}
```

#### 4.4 ドキュメント生成

統合レポートを作成:

```markdown
# Import Report

## Source
- URL: {source-url}
- Type: {skill|agent}
- Date: {timestamp}

## Conversion
- Original name: {original}
- New name: {converted}
- Files imported: {count}

## Verification
- Structure: ✓ Valid
- Naming: ✓ Compliant
- Conflicts: None detected
- Dependencies: {list}

## Usage
{example command}
```

#### 4.5 エラーハンドリング

各段階で発生しうるエラーに対応:

#### 取得失敗

- ネットワークエラー: リトライまたはキャッシュ使用
- 認証エラー: ユーザーにトークン提供を依頼
- 404エラー: URLの確認を促す

#### 変換失敗

- 不明な形式: 手動でのマッピングをユーザーに依頼
- 必須情報欠如: デフォルト値を提案

#### 競合検出

- 重複名: サフィックスに番号付与（例: `-v2`）
- 機能重複: ユーザーに統合または保持を確認

#### 検証失敗

- 構造不正: 修正箇所を指摘し、自動修正を試みる
- 依存関係未解決: インストール手順を提示

最大2回まで自己修正を試み、解決しない場合は詳細なエラーレポートを提供します。

## リソース

### スクリプト

- **fetch-definition.py**: 外部定義の取得
- **analyze-definition.py**: 構造分析とメタデータ抽出
- **apply-naming.py**: 命名規則の適用
- **convert-structure.py**: ディレクトリ構造の変換
- **generate-metadata.py**: ドキュメント生成
- **check-similarity.py**: 既存リソースとの類似性チェック
- **validate-structure.py**: 最終検証
- **check-dependencies.py**: 依存関係確認

### 参照ドキュメント

- **naming-conversion.md**: 命名規則の変換ルール
- **structure-template.json**: ディレクトリ構造のテンプレート
- **skill-template.md**: SKILL.mdのテンプレート
- **agent-template.md**: AGENT.mdのテンプレート
- **supported-sources.md**: サポートされる取得元の一覧

## 依存関係

- **Claude Code**: Read, Write, Edit, Glob, Grep, Bash, WebFetchツール
- **gh CLI**: GitHub APIアクセス
- **git**: リポジトリのクローン
- **curl**: HTTP(S)からのファイル取得
- **jq**: JSON処理
- **Python 3**: 変換スクリプトの実行

## 使用例

### GitHubからスキルをインポート

```bash
# Claude Codeで実行
@skills/proc-importing-skill

Import the skill from:
https://github.com/example/ai-agent-skill

Type: skill
```

### 公開URLからエージェント定義をインポート

```bash
@skills/proc-importing-skill

Import the agent definition from:
https://example.com/agent-definitions/expert.md

Type: agent
```

### ローカルファイルからインポート

```bash
@skills/proc-importing-skill

Import from local path:
/Users/aono/Downloads/custom-skill/

Type: skill
```

## ベストプラクティス

### 取得元の信頼性確認

- 公式リポジトリやコミュニティで実績のあるソースを優先
- 不明なスクリプトは実行前に内容を確認
- セキュリティリスクのあるコードは警告

### 段階的な統合

- 一度にすべてをインポートせず、Plan → Agree で確認
- 変換後は必ず検証ステップを実行
- 本番環境に配置する前にテスト

### ドキュメントの充実

- インポート元の情報を明記（トレーサビリティ）
- オリジナルのライセンスを尊重
- 変更履歴を記録

### 自律性の制御（Medium Autonomy）

- 手順は明確だが、判断はエージェントに委ねる
- ユーザーの合意を重視（Agreeステップ）
- 柔軟な対応（競合時の選択肢提示など）

## セキュリティ

このスキルは外部の信頼できないコンテンツを扱うため、以下のセキュリティ対策が実装されています。

### 実装済みの対策

#### URL検証

- 許可されたスキーム: http, https のみ
- ブロック対象: localhost, 127.0.0.1, プライベートIPアドレス
- 不正な文字のチェック（コマンドインジェクション対策）

#### ファイルサイズ制限

- 最大ファイルサイズ: 100MB
- ダウンロード前後でサイズを検証
- 制限超過時は警告またはスキップ

#### パストラバーサル対策

- ファイル名のサニタイズ
- パス解決と検証
- システムディレクトリへのアクセス制限

#### 入力検証

- コマンドライン引数の検証
- 危険な文字パターンの検出
- ターゲットパスがプロジェクトルート配下であることを確認

### 使用上の注意

#### 信頼できるソースのみを使用

- 公式リポジトリや検証済みのソースを優先
- 不明なURLからのインポートは慎重に

#### インポート前の確認

- Plan → Agree フェーズで内容を確認
- 疑わしいコードやスクリプトは手動で検証

#### 定期的なレビュー

- インポートしたスキル/エージェントを定期的にレビュー
- 不要または危険なコンテンツは削除

### セキュリティレポート

詳細なセキュリティレビューは [SECURITY_REVIEW.md](./SECURITY_REVIEW.md) を参照してください。

## Claude Code統合

### 推奨ツール使用

Claude Code環境で使用する場合、以下のツールを活用してください：

**ファイル操作**: Read, Write, Edit ツール（cp/mv コマンドではなく）
**Web取得**: WebFetch ツール（curl コマンドではなく）
**CLI操作**: Bash ツール（git, gh, npm などの実行のみ）

### スクリプトの独立性

このスキルのスクリプトは Claude Code に依存せず独立実行可能ですが、Claude Code統合時は上記のツールを優先することでより安全かつ効率的に動作します。
