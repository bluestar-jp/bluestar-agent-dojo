#!/bin/bash
# validate-plugin.sh - Validate plugin structure for bluestar-agent-dojo
#
# Checks:
#   - Required files exist
#   - JSON files are valid
#   - Skills have SKILL.md
#   - Version consistency

set -e

ERRORS=0
WARNINGS=0

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}ERROR:${NC} $1"
    ((ERRORS++))
}

warn() {
    echo -e "${YELLOW}WARN:${NC} $1"
    ((WARNINGS++))
}

ok() {
    echo -e "${GREEN}OK:${NC} $1"
}

echo "Validating bluestar-agent-dojo plugin structure..."
echo ""

# Check required files
echo "=== Required Files ==="

for file in ".claude-plugin/plugin.json" "marketplace.json" "CLAUDE.md" "LICENSE"; do
    if [ -f "$file" ]; then
        ok "$file exists"
    else
        error "$file not found"
    fi
done

# Validate JSON files
echo ""
echo "=== JSON Validation ==="

for json_file in ".claude-plugin/plugin.json" "marketplace.json"; do
    if [ -f "$json_file" ]; then
        if jq empty "$json_file" 2>/dev/null; then
            ok "$json_file is valid JSON"
        else
            error "$json_file is invalid JSON"
        fi
    fi
done

# Check version consistency
echo ""
echo "=== Version Consistency ==="

PLUGIN_VERSION=$(jq -r .version .claude-plugin/plugin.json 2>/dev/null || echo "N/A")
MARKETPLACE_VERSION=$(jq -r '.plugins[0].version' marketplace.json 2>/dev/null || echo "N/A")

echo "plugin.json version: $PLUGIN_VERSION"
echo "marketplace.json version: $MARKETPLACE_VERSION"

if [ "$PLUGIN_VERSION" = "$MARKETPLACE_VERSION" ]; then
    ok "Versions are consistent"
else
    error "Version mismatch between plugin.json and marketplace.json"
fi

# Check skills
echo ""
echo "=== Skills Validation ==="

if [ -d "skills" ]; then
    for skill_dir in skills/*/; do
        skill_name=$(basename "$skill_dir")
        if [ -f "${skill_dir}SKILL.md" ]; then
            ok "skills/$skill_name/SKILL.md exists"
        else
            error "skills/$skill_name/SKILL.md not found"
        fi
    done
else
    warn "skills/ directory not found"
fi

# Check agents
echo ""
echo "=== Agents Validation ==="

if [ -d "agents" ]; then
    agent_count=$(find agents -maxdepth 1 -name "*.md" | wc -l | tr -d ' ')
    ok "Found $agent_count agent definitions"
else
    warn "agents/ directory not found"
fi

# Check .claude adapter sync
echo ""
echo "=== Adapter Sync Check ==="

for skill_dir in skills/*/; do
    skill_name=$(basename "$skill_dir")
    if [ -f "${skill_dir}SKILL.md" ] && [ ! -f ".claude/skills/$skill_name/SKILL.md" ]; then
        warn ".claude/skills/$skill_name/SKILL.md not synced"
    fi
done

# Summary
echo ""
echo "=== Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo -e "${RED}Validation failed with $ERRORS error(s)${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}Validation passed!${NC}"
    exit 0
fi
