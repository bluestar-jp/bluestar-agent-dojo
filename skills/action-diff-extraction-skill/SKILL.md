---
name: diff-extraction
description: Git差分を取得・分析し、変更ファイルの種類と統計情報を出力する。
trigger: コードレビュー前の差分取得時
---

# Diff Extraction Skill

- Purpose: Git差分を取得し、変更内容を分析
- Scope: 単一アクションとしての差分抽出

## 入力

| パラメータ | 必須 | デフォルト | 説明 |
| ---------- | ---- | ---------- | ---- |
| commit_range | No | HEAD | 差分取得の範囲（例: HEAD~3, main..feature） |

## 実行手順

1. `scripts/extract-diff.sh` を実行
2. 差分サイズをチェック（1000行超は警告）
3. 変更ファイル一覧を出力

## 出力形式

```json
{
  "commit_range": "HEAD",
  "files_changed": ["path/to/file1", "path/to/file2"],
  "total_lines": 150,
  "diff_content": "... git diff output ..."
}
```

## エラーハンドリング

- **差分なし**: エラーメッセージを返却し、ユーザーに確認を促す
- **無効なcommit_range**: git rev-parseで検証し、エラーを報告

## リソース

- **スクリプト**: `scripts/extract-diff.sh`
