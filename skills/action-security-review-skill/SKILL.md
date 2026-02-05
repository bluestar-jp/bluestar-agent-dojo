---
name: security-review
description: セキュリティ観点（認証/認可、入力検証、OWASP対策）でコード差分をレビューし、JSON形式で結果を出力する。
trigger: セキュリティ関連コードのレビュー時
---

# Security Code Review

- Purpose: セキュリティ観点でコード変更をレビュー
- Scope: 単一観点のコードレビュー

## 対象ファイルパターン

- `auth/**`, `**/auth*`, `**/security*`
- `**/login*`, `**/session*`, `**/token*`
- `package.json`, `requirements.txt`, `go.mod`（依存関係）
- すべてのソースコード（入力検証観点）

## レビュー観点（優先度順）

### Critical/High（必須チェック）

1. **認証バイパス**
   - デバッグモードでの認証スキップ
   - 権限チェックの欠如
   - 不適切なJWT検証

2. **インジェクション**
   - SQLインジェクション（直接文字列結合）
   - XSS（エスケープなしの出力）
   - コマンドインジェクション

3. **機密情報**
   - ハードコードされたAPIキー/パスワード
   - ログへの機密情報出力
   - コミットされた.envファイル

### Medium/Low（推奨チェック）

- OWASP Top 10対策
- 依存関係の脆弱性
- セッション管理

## Claude Code ツール活用

- `Grep`: セキュリティパターンの検索
- `Bash`: `npm audit`, `pip-audit` 等の実行
- `Read`: 認証ロジックの詳細確認
- 不明確な場合: ユーザーに確認を求める

## 出力形式

```json
{
  "aspect": "security",
  "findings": [
    {
      "severity": "critical|high|medium|low",
      "category": "authentication|input_validation|owasp|sensitive_data|dependencies",
      "file": "path/to/file",
      "line": 45,
      "issue": "問題の説明",
      "suggestion": "改善提案"
    }
  ]
}
```

## 自己修正

- **誤検知の可能性**: コンテキストを追加確認
- **脆弱性の深刻度が不明**: CVEデータベースを参照
- **判断困難**: 重要度を上げて報告（セキュリティは保守的に）

## 参照

詳細基準: `references/review-criteria.md`
