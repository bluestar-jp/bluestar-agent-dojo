#!/bin/bash
# parallel_review.sh - 4観点並列レビュー実行エンジン
# Usage: ./parallel_review.sh "<diff_content>" "<project_context>"

set -euo pipefail

# 引数チェック
if [ $# -ne 2 ]; then
  echo "Usage: $0 '<diff_content>' '<project_context>'" >&2
  exit 1
fi

DIFF_CONTENT="$1"
PROJECT_CONTEXT="$2"
REVIEW_ASPECTS=("frontend" "backend" "infrastructure" "security")
TIMEOUT=120  # 各レビューのタイムアウト（秒）
PIDS=()
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFERENCES_DIR="$(cd "$SCRIPT_DIR/../references" && pwd)"

# セキュアな一時ディレクトリの作成
TEMP_DIR=$(mktemp -d -t code_review.XXXXXXXX)

# timeoutコマンドの検出（GNU timeout または gtimeout）
TIMEOUT_CMD=""
if command -v timeout &> /dev/null; then
  TIMEOUT_CMD="timeout"
elif command -v gtimeout &> /dev/null; then
  TIMEOUT_CMD="gtimeout"
else
  echo "Warning: timeout command not found. Reviews will run without timeout limit." >&2
fi

# 一時ディレクトリのクリーンアップ
# shellcheck disable=SC2317,SC2329
cleanup() {
  if [ -n "${TEMP_DIR:-}" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
  fi
}
trap cleanup EXIT

echo "Starting parallel code review with 4 perspectives..." >&2
echo "Timeout per aspect: ${TIMEOUT}s" >&2
echo "" >&2

# 並列実行：各観点ごとにGemini CLIプロセスを起動
for aspect in "${REVIEW_ASPECTS[@]}"; do
  {
    echo "Launching ${aspect} review..." >&2

    # Gemini CLI ヘッドレスモード with ベストプラクティス
    if [ -n "$TIMEOUT_CMD" ]; then
      CMD_PREFIX="$TIMEOUT_CMD ${TIMEOUT}"
    else
      CMD_PREFIX=""
    fi

    # レビューガイドラインを読み込み
    REVIEW_GUIDELINES=$(cat "${REFERENCES_DIR}/${aspect}-review.md")

    # 差分内容を一時ファイルに保存（パラメータ展開を防ぐため）
    printf '%s' "$DIFF_CONTENT" > "${TEMP_DIR}/diff_content.txt"

    # プロンプトを構築
    PROMPT=$(cat <<_REVIEW_PROMPT_EOF_
# Project Context
${PROJECT_CONTEXT}

# Review Focus: ${aspect}
You are reviewing code changes from a ${aspect} perspective.
Your task is to identify issues, risks, and improvement opportunities.

# Code Changes
$(cat "${TEMP_DIR}/diff_content.txt")

# Review Guidelines
${REVIEW_GUIDELINES}

# Output Format
Provide findings in JSON format with this exact structure:
{
  "aspect": "${aspect}",
  "findings": [
    {
      "severity": "critical|high|medium|low",
      "category": "string",
      "file": "relative/path/to/file",
      "line": 0,
      "issue": "description",
      "suggestion": "improvement"
    }
  ]
}

IMPORTANT: Output ONLY valid JSON, no additional text or explanation.
_REVIEW_PROMPT_EOF_
)

    $CMD_PREFIX gemini \
      -p "$PROMPT" \
      --output-format json \
      > "${TEMP_DIR}/review_${aspect}_raw.json" 2>"${TEMP_DIR}/review_${aspect}.err" || {
        # エラーハンドリング：失敗時はエラー情報を記録（jqで安全にJSON構築）
        jq -n \
          --arg aspect "$aspect" \
          --arg stderr "$(head -n 10 "${TEMP_DIR}/review_${aspect}.err" 2>/dev/null)" \
          '{aspect: $aspect, error: "Review failed", stderr: $stderr}' \
          > "${TEMP_DIR}/review_${aspect}.json"
        echo "Error: ${aspect} review failed" >&2
        echo "${aspect} review completed" >&2
        return
      }

    # Gemini CLI出力からresponseフィールドを抽出し、Markdownコードブロックを除去
    if [ -f "${TEMP_DIR}/review_${aspect}_raw.json" ]; then
      # responseフィールドを抽出
      RESPONSE=$(jq -r '.response // empty' "${TEMP_DIR}/review_${aspect}_raw.json" 2>/dev/null)

      if [ -n "$RESPONSE" ]; then
        # Markdownコードブロック（```json ... ```）を除去
        # shellcheck disable=SC2016
        echo "$RESPONSE" | sed -n '/^```json$/,/^```$/p' | sed '1d;$d' > "${TEMP_DIR}/review_${aspect}.json"

        # JSONが空または不正な場合は、元のレスポンスから直接抽出を試みる
        if ! jq empty "${TEMP_DIR}/review_${aspect}.json" 2>/dev/null; then
          # 別の形式の可能性：コードブロックなしでJSONが直接入っている場合
          echo "$RESPONSE" > "${TEMP_DIR}/review_${aspect}.json"
        fi
      else
        # responseフィールドがない場合は、生の出力をそのまま使用
        cp "${TEMP_DIR}/review_${aspect}_raw.json" "${TEMP_DIR}/review_${aspect}.json"
      fi

      # 一時ファイルをクリーンアップ
      rm -f "${TEMP_DIR}/review_${aspect}_raw.json"
    fi

    echo "${aspect} review completed" >&2
  } &
  PIDS+=($!)
done

echo "" >&2
echo "Waiting for all reviews to complete..." >&2

# 全プロセスの完了を待機し、失敗を検出
failed=0
for i in "${!PIDS[@]}"; do
  pid="${PIDS[$i]}"
  aspect="${REVIEW_ASPECTS[$i]}"

  if wait "$pid"; then
    echo "✓ ${aspect} review succeeded" >&2
  else
    ((failed++))
    echo "✗ ${aspect} review failed (PID: $pid)" >&2
  fi
done

echo "" >&2
echo "Review completion status: $((${#REVIEW_ASPECTS[@]} - failed))/${#REVIEW_ASPECTS[@]} succeeded" >&2
echo "" >&2

# 結果のバリデーション
echo "Validating JSON outputs..." >&2
invalid_count=0
for aspect in "${REVIEW_ASPECTS[@]}"; do
  if [ -f "${TEMP_DIR}/review_${aspect}.json" ]; then
    if jq empty "${TEMP_DIR}/review_${aspect}.json" 2>/dev/null; then
      echo "✓ ${aspect}: Valid JSON" >&2
    else
      echo "✗ ${aspect}: Invalid JSON" >&2
      ((invalid_count++))
      # 不正なJSONの場合、エラー情報を確認
      if [ -s "${TEMP_DIR}/review_${aspect}.err" ]; then
        echo "  Error output:" >&2
        head -n 5 "${TEMP_DIR}/review_${aspect}.err" | sed 's/^/    /' >&2
      fi
    fi
  else
    echo "✗ ${aspect}: Output file not found" >&2
    ((invalid_count++))
  fi
done

echo "" >&2

# 全結果をマージして出力
echo "Merging results..." >&2

# jqを使用して各JSONファイルを配列にマージ
if ASPECTS_JSON=$(jq -s '.' "${TEMP_DIR}"/review_{frontend,backend,infrastructure,security}.json 2>/dev/null) && [ -n "$ASPECTS_JSON" ]; then
  # 成功：review_summaryと統合
  jq -n \
    --argjson summary "$(jq -n \
      --argjson total "${#REVIEW_ASPECTS[@]}" \
      --argjson successful "$((${#REVIEW_ASPECTS[@]} - failed))" \
      --argjson failed_count "$failed" \
      --argjson invalid "$invalid_count" \
      '{total_aspects: $total, successful: $successful, failed: $failed_count, invalid_json: $invalid}')" \
    --argjson aspects "$ASPECTS_JSON" \
    '{review_summary: $summary, aspects: $aspects}'
else
  # 失敗：フォールバック処理
  echo "Warning: Failed to merge results with jq. Attempting manual merge..." >&2
  {
    echo "{"
    echo "  \"review_summary\": {"
    echo "    \"total_aspects\": ${#REVIEW_ASPECTS[@]},"
    echo "    \"successful\": $((${#REVIEW_ASPECTS[@]} - failed)),"
    echo "    \"failed\": ${failed},"
    echo "    \"invalid_json\": ${invalid_count}"
    echo "  },"
    echo "  \"aspects\": ["

    first=true
    for aspect in "${REVIEW_ASPECTS[@]}"; do
      if [ -f "${TEMP_DIR}/review_${aspect}.json" ] && jq empty "${TEMP_DIR}/review_${aspect}.json" 2>/dev/null; then
        if ! $first; then
          echo ","
        fi
        first=false
        cat "${TEMP_DIR}/review_${aspect}.json"
      fi
    done

    echo ""
    echo "  ]"
    echo "}"
  } | jq . 2>/dev/null || {
    echo "Error: Could not produce valid JSON output" >&2
    exit 1
  }
fi

# 終了コード：失敗があれば非ゼロ
exit $failed
