#!/bin/bash
# bump-version.sh - Bump version number for bluestar-agent-dojo plugin
#
# Usage:
#   ./scripts/bump-version.sh patch   # 1.0.0 → 1.0.1
#   ./scripts/bump-version.sh minor   # 1.0.0 → 1.1.0
#   ./scripts/bump-version.sh major   # 1.0.0 → 2.0.0
#   ./scripts/bump-version.sh 1.2.3   # Set specific version

set -e

PLUGIN_JSON=".claude-plugin/plugin.json"
MARKETPLACE_JSON="marketplace.json"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Install with: brew install jq"
    exit 1
fi

# Get current version
CURRENT_VERSION=$(jq -r .version "$PLUGIN_JSON")
echo "Current version: $CURRENT_VERSION"

# Parse current version
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Calculate new version based on argument
case "$1" in
    patch)
        NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
        ;;
    minor)
        NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
        ;;
    major)
        NEW_VERSION="$((MAJOR + 1)).0.0"
        ;;
    "")
        echo "Usage: $0 <patch|minor|major|VERSION>"
        exit 1
        ;;
    *)
        # Validate version format
        if [[ ! "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "Error: Invalid version format. Use X.Y.Z"
            exit 1
        fi
        NEW_VERSION="$1"
        ;;
esac

echo "New version: $NEW_VERSION"

# Update plugin.json
jq ".version = \"$NEW_VERSION\"" "$PLUGIN_JSON" > tmp.json && mv tmp.json "$PLUGIN_JSON"
echo "Updated $PLUGIN_JSON"

# Update marketplace.json
jq ".plugins[0].version = \"$NEW_VERSION\"" "$MARKETPLACE_JSON" > tmp.json && mv tmp.json "$MARKETPLACE_JSON"
echo "Updated $MARKETPLACE_JSON"

# Add changelog entry template
DATE=$(date +%Y-%m-%d)
CHANGELOG_ENTRY="## [$NEW_VERSION] - $DATE

### Added

### Changed

### Fixed

"

# Check if CHANGELOG.md exists and prepend entry
if [ -f "CHANGELOG.md" ]; then
    # Create temp file with new entry after the header
    {
        head -n 2 CHANGELOG.md
        echo ""
        echo "$CHANGELOG_ENTRY"
        tail -n +3 CHANGELOG.md
    } > tmp_changelog.md && mv tmp_changelog.md CHANGELOG.md
    echo "Added entry template to CHANGELOG.md"
fi

echo ""
echo "Version bumped to $NEW_VERSION"
echo "Next steps:"
echo "  1. Edit CHANGELOG.md with your changes"
echo "  2. git add . && git commit -m 'chore: bump version to $NEW_VERSION'"
echo "  3. make release"
