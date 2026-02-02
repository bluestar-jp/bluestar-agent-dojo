# Project Summary: BlueStar Agent Dojo

## Purpose
AIエージェントの「道場」として、BlueStarエコシステムにおける自律型エージェントのスキル（知識・指示）を一元管理・育成するためのリポジトリ。

## Tech Stack
- **Definition**: Markdown, YAML
- **Tooling**: Serena (Agent Platform), Gemini CLI, container-use (Environment)
- **Output Target**: AI Agent Custom Instructions, MCP Tools

## Architecture: 龍虎体系 (Ryu-Ko System)
1. **龍の巻 (Ryu-no-maki) - 知識型**: 背景、規約、リファレンス。
2. **虎の巻 (Tora-no-maki) - 指示型**: アクション、プロシージャ、分岐ロジック。

## Directory Structure
- `skills/ryu_no_maki/`: 知識型スキル（context, guidelines, references）。
- `skills/tora_no_maki/`: 指示型スキル（single_action, procedure, conditional_instructions）。
- `menkyokaiden/`: プラットフォーム向け設定ファイルの出力先。
- `.serena/`: エージェントの設定と記憶。
