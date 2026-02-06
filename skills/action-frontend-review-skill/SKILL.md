---
name: action-frontend-review-skill
description: フロントエンド観点（UI/UX、アクセシビリティ、パフォーマンス）でコード差分をレビューし、JSON形式で結果を出力する。フロントエンドコード（JSX/TSX/CSS）のレビュー時に使用する。
---

# Frontend Code Review

- Purpose: フロントエンド観点でコード変更をレビュー
- Scope: 単一観点のコードレビュー

## 対象ファイルパターン

- `*.jsx`, `*.tsx`, `*.js`, `*.ts`（コンポーネント）
- `*.css`, `*.scss`, `*.less`, `*.styled.ts`
- `components/**`, `pages/**`, `views/**`

## レビュー観点（優先度順）

### Critical/High（必須チェック）

1. **アクセシビリティ**
   - セマンティックHTML（`<button>` vs `<div onClick>`）
   - キーボード操作可能性
   - ARIA属性の適切な使用
   - カラーコントラスト

2. **パフォーマンス**
   - 不要な再レンダリング（メモ化の欠如）
   - バンドルサイズへの影響
   - 遅延読み込みの欠如

3. **状態管理**
   - データ破壊の可能性
   - 状態の不整合

### Medium/Low（推奨チェック）

- UI/UXの一貫性
- コンポーネント設計（単一責任原則）
- 命名規則の遵守

## Claude Code ツール活用

- `Grep`: パターン検索で問題コードを発見
- `Read`: 詳細なコード確認
- 不明確な場合: ユーザーに確認を求める

## 出力形式

```json
{
  "aspect": "frontend",
  "findings": [
    {
      "severity": "critical|high|medium|low",
      "category": "accessibility|performance|state_management|ui_ux|component_design",
      "file": "path/to/file",
      "line": 45,
      "issue": "問題の説明",
      "suggestion": "改善提案"
    }
  ]
}
```

## 自己修正

- **コンテキスト不足**: 関連ファイルを追加で読み込む
- **判断困難**: 重要度を下げて報告、ユーザー確認を推奨
- **誤検知の可能性**: コンテキストを追加確認

## 参照

詳細基準: `references/review-criteria.md`
