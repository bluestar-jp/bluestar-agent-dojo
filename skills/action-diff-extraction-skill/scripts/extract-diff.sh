#!/bin/bash
# extract_diff.sh - Git差分抽出スクリプト
# Usage: ./extract_diff.sh [commit_range]

set -euo pipefail

# デフォルトはHEADとの差分
COMMIT_RANGE="${1:-HEAD}"

# 引数の検証（git rev-parseで確認）
if ! git rev-parse --verify "${COMMIT_RANGE}^{commit}" &>/dev/null && \
   ! git rev-parse --verify "${COMMIT_RANGE}" &>/dev/null; then
  echo "Error: Invalid commit range: $COMMIT_RANGE" >&2
  exit 1
fi

# 差分を取得
DIFF=$(git diff "$COMMIT_RANGE")

# 差分が空の場合はエラー
if [ -z "$DIFF" ]; then
  echo "Error: No changes detected in git diff $COMMIT_RANGE" >&2
  echo "Run 'git status' to check your working directory." >&2
  exit 1
fi

# 差分サイズをチェック
DIFF_SIZE=$(echo "$DIFF" | wc -l | tr -d ' ')

# 1000行以上の場合は警告
if [ "$DIFF_SIZE" -gt 1000 ]; then
  echo "Warning: Large diff detected ($DIFF_SIZE lines)." >&2
  echo "Consider splitting the review or reviewing specific files." >&2
fi

# 変更されたファイル一覧を取得
echo "Changed files:" >&2
git diff --name-only "$COMMIT_RANGE" >&2
echo "" >&2
echo "Total lines changed: $DIFF_SIZE" >&2
echo "---" >&2

# 差分を出力
echo "$DIFF"
