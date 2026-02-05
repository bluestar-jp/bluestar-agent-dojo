#!/bin/bash
# scripts/lint_markdown.sh
# 目的: Markdownファイルが編集された時にmarkdownlint-cli2を実行する

# .mdファイルが編集されたかチェック
# Claude Code: CLAUDE_FILE_PATHS (JSON配列)
# Gemini CLI: GEMINI_CHANGED_FILES (カンマ区切り)

MD_FILES=()

# Claude CodeのCLAUDE_FILE_PATHSを解析
if [ -n "$CLAUDE_FILE_PATHS" ]; then
  while IFS= read -r file; do
    if [[ "$file" == *.md ]]; then
      MD_FILES+=("$file")
    fi
  done < <(echo "$CLAUDE_FILE_PATHS" | jq -r '.[]' 2>/dev/null)
fi

# Gemini CLIのファイルパスを解析
if [ -n "$GEMINI_CHANGED_FILES" ]; then
  while IFS= read -r file; do
    if [[ "$file" == *.md ]]; then
      MD_FILES+=("$file")
    fi
  done < <(echo "$GEMINI_CHANGED_FILES" | tr ',' '\n')
fi

# Markdownファイルがなければ終了
if [ ${#MD_FILES[@]} -eq 0 ]; then
  exit 0
fi

echo "編集されたMarkdownファイルにmarkdownlintを実行中..."
npx markdownlint-cli2 "${MD_FILES[@]}" --fix
