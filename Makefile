# Makefile for bluestar-agent-dojo plugin management
#
# Usage:
#   make patch    - Bump patch version (1.0.0 → 1.0.1)
#   make minor    - Bump minor version (1.0.0 → 1.1.0)
#   make major    - Bump major version (1.0.0 → 2.0.0)
#   make release  - Create release with current version
#   make validate - Validate plugin structure
#   make status   - Show current version and status

.PHONY: patch minor major release validate status changelog help

# Default target
help:
	@echo "Available commands:"
	@echo "  make patch     - Bump patch version (bug fixes)"
	@echo "  make minor     - Bump minor version (new features)"
	@echo "  make major     - Bump major version (breaking changes)"
	@echo "  make release   - Tag and push current version"
	@echo "  make validate  - Validate plugin structure"
	@echo "  make status    - Show current version and git status"
	@echo "  make changelog - Open CHANGELOG.md for editing"

# Get current version from plugin.json
VERSION := $(shell jq -r .version .claude-plugin/plugin.json 2>/dev/null || echo "0.0.0")

# Show current status
status:
	@echo "Current version: $(VERSION)"
	@echo ""
	@git status --short

# Bump patch version (1.0.0 → 1.0.1)
patch:
	@./scripts/bump-version.sh patch

# Bump minor version (1.0.0 → 1.1.0)
minor:
	@./scripts/bump-version.sh minor

# Bump major version (1.0.0 → 2.0.0)
major:
	@./scripts/bump-version.sh major

# Create release with current version
release:
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Error: Working directory not clean. Commit changes first."; \
		exit 1; \
	fi
	@echo "Creating release v$(VERSION)..."
	@git tag -a "v$(VERSION)" -m "Release v$(VERSION)"
	@git push origin main
	@git push origin "v$(VERSION)"
	@echo "Released v$(VERSION) successfully!"

# Validate plugin structure
validate:
	@echo "Validating plugin structure..."
	@./scripts/validate-plugin.sh

# Open CHANGELOG for editing
changelog:
	@$${EDITOR:-vim} CHANGELOG.md
