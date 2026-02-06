---
name: action-backend-review-skill
description: バックエンド観点（API設計、DB最適化、エラーハンドリング）でコード差分をレビューし、JSON形式で結果を出力する。バックエンドコード（API、DB、サーバーサイド）のレビュー時に使用する。
---

# Backend Code Review

- Purpose: バックエンド観点でコード変更をレビュー
- Scope: 単一観点のコードレビュー

## 対象ファイルパターン

- `*.py`, `*.go`, `*.java`, `*.rb`, `*.php`
- `api/**`, `services/**`, `controllers/**`
- `models/**`, `repositories/**`
- `routes/**`, `handlers/**`

## レビュー観点（優先度順）

### Critical/High（必須チェック）

1. **N+1問題**
   - ループ内クエリの検出
   - eager loading（JOINやpreload）の欠如
   - ORMの不適切な使用

2. **エラーハンドリング**
   - 例外の捕捉漏れ
   - 適切なログ記録の欠如
   - 不適切なエラーレスポンス

3. **トランザクション**
   - データ整合性の破壊可能性
   - ロールバック処理の欠如

### Medium/Low（推奨チェック）

- API設計（RESTful原則）
- スケーラビリティ考慮
- キャッシュ戦略

## Claude Code ツール活用

- `Grep`: N+1パターン、例外処理の検索
- `Read`: クエリロジックの詳細確認
- 不明確な場合: ユーザーに確認を求める

## 出力形式

```json
{
  "aspect": "backend",
  "findings": [
    {
      "severity": "critical|high|medium|low",
      "category": "api_design|database|error_handling|business_logic|scalability",
      "file": "path/to/file",
      "line": 45,
      "issue": "問題の説明",
      "suggestion": "改善提案"
    }
  ]
}
```

## 自己修正

- **N+1問題の検出が不確実**: 関連クエリを追加調査
- **ビジネスロジックの妥当性が不明**: ユーザー確認を推奨
- **誤検知の可能性**: コンテキストを追加確認

## 参照

詳細基準: `references/review-criteria.md`
