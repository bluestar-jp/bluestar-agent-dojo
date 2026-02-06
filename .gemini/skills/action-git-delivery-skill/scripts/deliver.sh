#!/bin/bash
# skills/action-git-delivery-skill/scripts/deliver.sh

set -e

MESSAGE=$1
TRAILER="Co-Authored-By: gemini-cli <218195315+gemini-cli@users.noreply.github.com>"

if [ -z "$MESSAGE" ]; then
  echo '{"status": "error", "reason": "Commit message is required"}'
  exit 1
fi

# 変更されたファイルを特定（ステージング済み、未ステージング、未追跡）
CHANGES=$(git status --porcelain | awk '{print $2}')

if [ -z "$CHANGES" ]; then
  echo '{"status": "skipped", "reason": "No changes detected"}'
  exit 0
fi

# 変更されたファイルのみをadd
echo "$CHANGES" | xargs git add

# コミットメッセージの作成（トレーラーの前に空行を入れるのが一般的）
FULL_MESSAGE=$(printf "%s

%s" "$MESSAGE" "$TRAILER")

# コミット実行
git commit -m "$FULL_MESSAGE"

# コミット情報の取得
COMMIT_HASH=$(git rev-parse HEAD)
COMMITTED_FILES=$(git diff-tree --no-commit-id --name-only -r "$COMMIT_HASH" | jq -R . | jq -s .)

# プッシュ実行
git push origin HEAD

# 結果をJSONで出力
jq -n 
  --arg status "success" 
  --arg hash "$COMMIT_HASH" 
  --argjson files "$COMMITTED_FILES" 
  '{status: $status, commit_hash: $hash, committed_files: $files, message: "Commit and push completed."}'
