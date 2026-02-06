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
# Update plugin.json
jq ".version = \"$NEW_VERSION\"" "$PLUGIN_JSON" > tmp.json && mv tmp.json "$PLUGIN_JSON"
echo "Updated $PLUGIN_JSON"

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
