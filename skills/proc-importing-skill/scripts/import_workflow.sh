#!/bin/bash
#
# 外部定義のインポートワークフローを統合実行する
#
# Usage:
#   import_workflow.sh --source <URL or path> --type <skill|agent> [--auto-approve]

set -euo pipefail

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# スクリプトディレクトリ
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# 作業ディレクトリ
WORK_DIR="/tmp/bluestar-import-$$"
STAGING_DIR="$WORK_DIR/staging"
CONVERTED_DIR="$WORK_DIR/converted"

# デフォルト値
AUTO_APPROVE=false
SOURCE=""
RESOURCE_TYPE=""

# ログ関数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# クリーンアップ関数
cleanup() {
    if [ -d "$WORK_DIR" ]; then
        log_info "Cleaning up temporary files..."
        rm -rf "$WORK_DIR"
    fi
}

# エラーハンドラ
error_exit() {
    log_error "$1"
    cleanup
    exit 1
}

# 引数のパース
while [[ $# -gt 0 ]]; do
    case $1 in
        --source)
            SOURCE="$2"
            shift 2
            ;;
        --type)
            RESOURCE_TYPE="$2"
            shift 2
            ;;
        --auto-approve)
            AUTO_APPROVE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 --source <URL or path> --type <skill|agent> [--auto-approve]"
            exit 1
            ;;
    esac
done

# 必須パラメータチェック
if [ -z "$SOURCE" ] || [ -z "$RESOURCE_TYPE" ]; then
    error_exit "必須パラメータが不足しています。--source と --type を指定してください"
fi

# リソースタイプの検証
if [ "$RESOURCE_TYPE" != "skill" ] && [ "$RESOURCE_TYPE" != "agent" ]; then
    error_exit "不正なリソースタイプ: $RESOURCE_TYPE ('skill' または 'agent' を指定してください)"
fi

# セキュリティ検証: 危険な文字のチェック
if [[ "$SOURCE" =~ [;\&\|\`\$] ]]; then
    error_exit "セキュリティ: 取得元に不正な文字が含まれています"
fi

log_info "Starting import workflow"
log_info "Source: $SOURCE"
log_info "Type: $RESOURCE_TYPE"
echo ""

# 作業ディレクトリを作成
mkdir -p "$STAGING_DIR" "$CONVERTED_DIR"

# ==========================================
# Phase 1: Plan - 取得と分析
# ==========================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 1: PLAN - Fetch and Analyze${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1.1 外部定義を取得
log_info "Fetching definition from source..."
python3 "$SCRIPT_DIR/fetch_definition.py" \
    --source "$SOURCE" \
    --type "$RESOURCE_TYPE" \
    --output-dir "$STAGING_DIR" || error_exit "Failed to fetch definition"

echo ""

# 1.2 定義を分析
log_info "Analyzing definition..."
python3 "$SCRIPT_DIR/analyze_definition.py" \
    --input-dir "$STAGING_DIR" \
    --type "$RESOURCE_TYPE" \
    --output "$WORK_DIR/analysis.json" || error_exit "Failed to analyze definition"

echo ""

# 1.3 命名規則を適用
log_info "Applying naming conventions..."
python3 "$SCRIPT_DIR/apply_naming.py" \
    --input "$WORK_DIR/analysis.json" \
    --output "$WORK_DIR/renamed.json" || error_exit "Failed to apply naming"

echo ""

# 命名結果を読み込み
ORIGINAL_NAME=$(jq -r '.original_name' "$WORK_DIR/renamed.json")
NEW_NAME=$(jq -r '.new_name' "$WORK_DIR/renamed.json")
BASE_PATH=$(jq -r '.base_path' "$WORK_DIR/renamed.json")
TARGET_PATH="$PROJECT_ROOT/$BASE_PATH"

log_success "Name conversion: $ORIGINAL_NAME → $NEW_NAME"
log_info "Target path: $TARGET_PATH"

# ==========================================
# Phase 2: Agree - ユーザー確認
# ==========================================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 2: AGREE - User Confirmation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# プラン情報を表示
echo "Import Plan:"
echo "  Source:        $SOURCE"
echo "  Type:          $RESOURCE_TYPE"
echo "  Original name: $ORIGINAL_NAME"
echo "  New name:      $NEW_NAME"
echo "  Target path:   $TARGET_PATH"
echo ""

# 既存リソースとの競合チェック
if [ -d "$TARGET_PATH" ]; then
    log_warning "Target directory already exists: $TARGET_PATH"
    echo "Options:"
    echo "  1. Overwrite existing resource"
    echo "  2. Use different name"
    echo "  3. Cancel import"
    echo ""

    if [ "$AUTO_APPROVE" = false ]; then
        read -p "Choose option [1/2/3]: " choice
        case $choice in
            1)
                log_info "Will overwrite existing resource"
                rm -rf "$TARGET_PATH"
                ;;
            2)
                read -p "Enter new name: " custom_name
                NEW_NAME="$custom_name"
                BASE_PATH="${BASE_PATH%%/*}/$NEW_NAME"
                TARGET_PATH="$PROJECT_ROOT/$BASE_PATH"
                log_info "Using custom name: $NEW_NAME"
                ;;
            3)
                log_info "Import cancelled by user"
                cleanup
                exit 0
                ;;
            *)
                error_exit "Invalid choice"
                ;;
        esac
    else
        log_warning "Auto-approve enabled, overwriting existing resource"
        rm -rf "$TARGET_PATH"
    fi
fi

# 類似性チェック
if [ "$RESOURCE_TYPE" = "skill" ]; then
    EXISTING_DIR="$PROJECT_ROOT/skills"
elif [ "$RESOURCE_TYPE" = "agent" ]; then
    EXISTING_DIR="$PROJECT_ROOT/agents"
fi

log_info "Checking similarity with existing resources..."
python3 "$SCRIPT_DIR/check_similarity.py" \
    --new "$STAGING_DIR" \
    --existing "$EXISTING_DIR" \
    --threshold 0.7 \
    --output "$WORK_DIR/similarity.json" || {
    log_warning "Similarity check found potential conflicts"

    if [ "$AUTO_APPROVE" = false ]; then
        echo ""
        read -p "Continue anyway? [y/N]: " continue_choice
        if [ "$continue_choice" != "y" ] && [ "$continue_choice" != "Y" ]; then
            log_info "Import cancelled by user"
            cleanup
            exit 0
        fi
    fi
}

echo ""

# 最終確認
if [ "$AUTO_APPROVE" = false ]; then
    read -p "Proceed with import? [y/N]: " final_confirm
    if [ "$final_confirm" != "y" ] && [ "$final_confirm" != "Y" ]; then
        log_info "Import cancelled by user"
        cleanup
        exit 0
    fi
fi

# ==========================================
# Phase 3: Execute - 変換と配置
# ==========================================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 3: EXECUTE - Convert and Deploy${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 3.1 ディレクトリ構造を変換
log_info "Converting directory structure..."
python3 "$SCRIPT_DIR/convert_structure.py" \
    --input "$STAGING_DIR" \
    --output "$CONVERTED_DIR" \
    --config "$WORK_DIR/renamed.json" || error_exit "Failed to convert structure"

echo ""

# 3.2 変換済みリソースを配置
log_info "Deploying converted resource..."
CONVERTED_PATH="$CONVERTED_DIR/$BASE_PATH"
if [ ! -d "$CONVERTED_PATH" ]; then
    error_exit "変換済みリソースが見つかりません: $CONVERTED_PATH"
fi

# セキュリティ: ターゲットパスがプロジェクトルート配下であることを確認
RESOLVED_TARGET=$(cd "$(dirname "$TARGET_PATH")" 2>/dev/null && pwd)/$(basename "$TARGET_PATH") || true
if [[ ! "$RESOLVED_TARGET" =~ ^"$PROJECT_ROOT" ]]; then
    error_exit "セキュリティ: ターゲットパスがプロジェクトルート外です: $TARGET_PATH"
fi

mkdir -p "$(dirname "$TARGET_PATH")"
cp -r "$CONVERTED_PATH" "$TARGET_PATH" || error_exit "リソースの配置に失敗しました"

log_success "リソースを配置しました: $TARGET_PATH"

# ==========================================
# Phase 4: Verify - 検証
# ==========================================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 4: VERIFY - Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 4.1 構造検証
log_info "Validating structure..."
python3 "$SCRIPT_DIR/validate_structure.py" \
    --path "$TARGET_PATH" \
    --type "$RESOURCE_TYPE" \
    --output "$WORK_DIR/validation.json" || {
    log_warning "Validation found issues (see above)"
}

echo ""

# 4.2 依存関係チェック
log_info "Checking dependencies..."
python3 "$SCRIPT_DIR/check_dependencies.py" \
    --path "$TARGET_PATH" \
    --output "$WORK_DIR/dependencies.json" || {
    log_warning "Some dependencies are missing (see above)"
}

echo ""

# ==========================================
# 完了
# ==========================================
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Import Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

log_success "Resource imported successfully"
echo ""
echo "Details:"
echo "  Name:         $NEW_NAME"
echo "  Type:         $RESOURCE_TYPE"
echo "  Path:         $TARGET_PATH"
echo ""
echo "Next steps:"
echo "  1. Review the imported resource: cd $TARGET_PATH"
echo "  2. Adjust SKILL.md/AGENT.md as needed"
echo "  3. Test the functionality"
echo "  4. Commit the changes: git add $BASE_PATH && git commit"
echo ""

# クリーンアップ
cleanup

exit 0
