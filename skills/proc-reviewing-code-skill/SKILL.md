---
name: reviewing-code
description: Git差分を4観点（フロントエンド、バックエンド、インフラ、セキュリティ）で並列レビューし、JSON形式で報告するワークフロー。
disable-model-invocation: true
---

# Code Review Skill

- Purpose: Git差分を4観点（フロントエンド、バックエンド、インフラ、セキュリティ）で並列レビューし、JSON形式で報告する
- Scope: Git差分またはPRに対するコードレビュー自動化

## 概要

このスキルは、Gemini CLIヘッドレスモードを利用して、コード変更に対する包括的なレビューを実行します。複数の専門観点から並列的にレビューを行い、構造化された結果を提供します。

## ワークフロー (Plan → Agree → Execute → Verify)

### 1. Plan: 対象の特定

```bash
# 差分を取得
git diff HEAD

# 差分サイズをチェック
DIFF_SIZE=$(git diff HEAD | wc -l)
if [ "$DIFF_SIZE" -gt 1000 ]; then
  echo "Warning: Large diff detected ($DIFF_SIZE lines). Consider splitting the review."
fi
```

- 変更内容を確認
- 差分サイズをチェック（1000行超は警告）
- レビュー対象ファイルとサイズをユーザーに報告

### 2. Agree: ユーザー確認

- レビュー対象ファイル一覧を提示
- 実行するレビュー観点を確認
- 実行可否を確認

### 3. Execute: 並列レビュー実行

```bash
scripts/review-orchestrator.py \
  --diff "$(git diff HEAD)"
```

内部では4つのGemini CLIプロセスを並列起動：

- `scripts/parallel-review.sh`が各観点で独立したプロセスを起動
- タイムアウト: 各120秒
- 出力形式: JSON（`--output-format json`）
- エラーハンドリング: stderrキャプチャ、JSON検証

### 4. Verify: 結果検証

- JSON形式の妥当性チェック（jq）
- 4つの観点すべてで結果が得られたか確認
- エラーがあれば最大2回リトライ
- 結果をマージして統一フォーマットで出力

## レビュー観点 (Review Perspectives)

各観点の詳細基準は `references/` に格納：

1. **フロントエンド** (`frontend-review.md`)
   - UI/UXの一貫性
   - アクセシビリティ
   - パフォーマンス（レンダリング、バンドルサイズ）
   - 状態管理の適切性
   - コンポーネント設計

2. **バックエンド** (`backend-review.md`)
   - API設計とRESTful原則
   - データベースクエリ最適化
   - エラーハンドリング
   - ビジネスロジックの妥当性
   - スケーラビリティ

3. **インフラ** (`infrastructure-review.md`)
   - 設定管理
   - デプロイメント戦略
   - リソース管理（メモリ、CPU）
   - ロギングとモニタリング
   - 環境変数とシークレット管理

4. **セキュリティ** (`security-review.md`)
   - 認証・認可の実装
   - 入力検証とサニタイゼーション
   - OWASP Top 10対策
   - 機密情報の取り扱い
   - 依存関係の脆弱性

## エラーハンドリング

### Gemini CLI失敗時

```bash
# stderrを確認
if [ -s /tmp/review_${aspect}.err ]; then
  echo "Error in ${aspect} review:"
  cat /tmp/review_${aspect}.err
  # リトライ（最大2回）
fi
```

### 差分取得失敗時

```bash
# git status確認
git status
# ユーザーに報告
echo "Failed to extract diff. Please check git status."
```

### JSON不正時

```bash
# JSON検証
if ! jq empty /tmp/review_${aspect}.json 2>/dev/null; then
  echo "Invalid JSON from ${aspect} review. Retrying..."
  # 該当観点を再実行
fi
```

## リソース

- **Orchestrator**: `scripts/review-orchestrator.py` - 全体のプロセス制御
- **Parallel Engine**: `scripts/parallel-review.sh` - 4観点並列実行
- **Diff Extractor**: `scripts/extract-diff.sh` - Git差分抽出
- **Review Criteria**: `references/*.md` - 各観点の詳細基準

## 依存関係

- **Gemini CLI**: ヘッドレスモード対応バージョン
- **git**: バージョン管理
- **jq**: JSON処理とバリデーション
- **timeout**: プロセス制御（GNU coreutils）
- **Python 3**: オーケストレータースクリプト実行

## 使用例

### 基本的な使用方法

```bash
# 現在の変更をレビュー
gemini -p "@skills/proc-reviewing-code-skill.md

Review the current changes:
$(git diff HEAD)
"
```

### 特定の観点のみレビュー

```bash
# セキュリティ観点のみ
gemini -p "@skills/proc-reviewing-code-skill.md

Focus on security perspective only.
Review: $(git diff HEAD)
" --output-format json
```

## 出力形式

```json
{
  "aspects": [
    {
      "name": "security",
      "findings": [
        {
          "severity": "critical",
          "file": "src/api/auth.js",
          "line": 45,
          "issue": "JWT token verification is skipped in debug mode",
          "suggestion": "Remove debug bypass entirely. Use proper testing strategies."
        }
      ]
    },
    {
      "name": "backend",
      "findings": [...]
    }
  ],
  "summary": {
    "total_issues": 15,
    "critical": 2,
    "high": 5,
    "medium": 6,
    "low": 2
  }
}
```

## ベストプラクティス

### 認知負荷の最小化

- SKILL.mdは簡潔に（ワークフローの概要のみ）
- 詳細はreferences/に切り出し
- 必要な観点ファイルのみ動的に読み込み

### ツールへのオフロード

- 複雑なロジックはスクリプト化
- Plan → Agree → Execute → Verify ループを明示
- 検証済みスクリプトで予測可能な動作

### 自律性の制御（Medium Autonomy）

- 手順は明確、解釈には柔軟性
- レビュー観点の適用はエージェントが判断
- ユーザーインタラクションは自由度高く
