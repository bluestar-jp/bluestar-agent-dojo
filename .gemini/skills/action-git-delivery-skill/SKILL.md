---
name: action-git-delivery-skill
description: gitでセッション内で操作されたファイルをコミットし、リモートにプッシュする。
---

# Git Delivery Skill

- Purpose: 開発作業後の変更を安全にコミットし、プッシュする
- Scope: 変更ファイルの特定、規約に準拠したコミット、プッシュ

## 入力

| パラメータ | 必須 | デフォルト | 説明 |
| ---------- | ---- | ---------- | ---- |
| message | Yes | - | コミットメッセージ（Conventional Commits準拠を推奨） |

## 実行手順

1. `git status --porcelain` を使用して、現在ステージングされている、または未追跡/変更済みのファイルを特定する
2. 対象ファイルのみを `git add` する
3. コミットメッセージの末尾に `Co-Authored-By: gemini-cli <218195315+gemini-cli@users.noreply.github.com>` を追加してコミットする
4. `git push origin HEAD` を実行する

## 出力形式

```json
{
  "status": "success",
  "committed_files": ["path/to/file1", "path/to/file2"],
  "commit_hash": "abc1234...",
  "message": "Commit and push completed."
}
```

## エラーハンドリング

- **変更なし**: コミット対象がない場合はその旨を報告して終了する
- **プッシュ失敗**: リモートとの競合が発生した場合は、ユーザーに手動解決を促す
- **メッセージ未指定**: 必須パラメータエラーを返す

## リソース

- **スクリプト**: `scripts/deliver.sh`
