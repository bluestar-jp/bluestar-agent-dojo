#!/bin/bash
# scripts/lint_markdown.sh
# Purpose: Run markdownlint-cli2 on all markdown files to ensure quality.

echo "Running markdownlint..."
npx markdownlint-cli2 "**/*.md" --fix
