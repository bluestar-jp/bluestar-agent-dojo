# DEPRECATED: proc-reviewing-code-skill

このスキルは非推奨です。以下の新しいスキルとエージェントに分割されました。

## 移行先

### オーケストレーター

- `agents/shihan-code-review.md` - コードレビューの計画と結果統合

### 専門エージェント

- `agents/deshi-frontend-reviewer.md` - フロントエンドレビュー
- `agents/deshi-backend-reviewer.md` - バックエンドレビュー
- `agents/deshi-infrastructure-reviewer.md` - インフラレビュー
- `agents/deshi-security-reviewer.md` - セキュリティレビュー

### 単一観点スキル

- `skills/action-frontend-review-skill/` - フロントエンド観点のレビュー基準
- `skills/action-backend-review-skill/` - バックエンド観点のレビュー基準
- `skills/action-infrastructure-review-skill/` - インフラ観点のレビュー基準
- `skills/action-security-review-skill/` - セキュリティ観点のレビュー基準
- `skills/action-diff-extraction-skill/` - 差分抽出

## 移行ガイド

旧:

```text
@proc-reviewing-code-skill でコードレビューを実行
```

新:

```text
shihan-code-review に従い、必要な観点のdeshiのみを呼び出してレビューを実行
```

## 削除予定

このディレクトリは後方互換性のため一定期間残されますが、将来のバージョンで削除される予定です。
