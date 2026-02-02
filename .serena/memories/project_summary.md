# Project Summary: BlueStar Agent Dojo

## Purpose

AIエージェントの「道場」として、BlueStarエコシステムにおける自律型エージェントのスキル（知識・指示）を一元管理・育成するためのリポジトリ。
「真実のソース（Source of Truth）」から、各プラットフォーム（Gemini, Claude等）向けの構成ファイルを生成・同期する。

## Tech Stack

- **Definition**: Markdown, YAML
- **Tooling**: Serena (Agent Platform), Gemini CLI, container-use (Environment)
- **Scripting**: Python (Sync verification)
- **Output Target**: AI Agent Custom Instructions, MCP Tools

## Architecture: 龍虎体系 (Ryu-Ko System)

1. **龍の巻 (Ryu-no-maki) - 知識型**: 背景、規約、リファレンス。
   - `makimono/ryunomaki/`
2. **虎の巻 (Tora-no-maki) - 指示型**: アクション、プロシージャ、分岐ロジック。
   - `makimono/toranomaki/`

## Core Directory Structure

- `agents/`: エージェント定義の真実のソース。
- `skills/`: スキル定義の真実のソース。
- `makimono/`: 体系化された知識・指示のライブラリ（龍の巻・虎の巻）。
- `menkyokaiden/`: プラットフォーム向け設定ファイルの出力・公開用ディレクトリ。
- `.gemini/`, `.claude/`: 各プラットフォーム固有のアダプター設定。
- `scripts/`: 同期検証スクリプト等。
- `.serena/`: エージェントの設定と記憶。
