# Project Summary: BlueStar Agent Dojo

## Purpose

BlueStarエコシステムにおける自律型AIエージェントの「道場」であり、スキル（知識・指示）を一元管理・育成するためのリポジトリ。
Claude Codeを中心に設計されており、共有知見を「巻物（Makimono）」として集約し、サブエージェント（師範・弟子）やスキルを通じて自律性を実現する。

## SoT (Source of Truth) Principle

プロンプトの実体は `agents/` および `skills/` にあり、`.claude/` や `.gemini/` などの各プラットフォーム用アダプターディレクトリはこれらを参照する。

## Tech Stack

- **Definition**: Markdown, YAML
- **Tooling**: Serena (Agent Platform), Gemini CLI, Claude Code (Primary), container-use (Environment)
- **Scripting**: Python (Sync verification, specialized tasks)
- **Plugin System**: Claude Code Marketplace 連携 (`marketplace.json`)

## Architecture: 龍虎体系 (Ryu-Ko System)

1. **龍の巻 (Ryu-no-maki) - 知識型**: 背景、規約、リファレンス。
   - `makimono/ryunomaki/` (Context, Guidelines, Specs, References)
2. **虎の巻 (Tora-no-maki) - 手順型**: アクション、プロシージャ、分岐ロジック。
   - `makimono/toranomaki/` (Procedure, Single Action, Conditional Instructions)

## Agent & Skill Categories

- **師範 (shihan - 統合型)**: 戦略立案、タスク委任、オーケストレーション。
  - `shihan-routing`, `shihan-parallel`, `shihan-sequential`
- **弟子 (deshi - 専門型)**: 特定ドメインタスクの実行、専門知識の維持。
  - `deshi-skill-expert`, `deshi-code-reviewer`
- **スキル (skills)**: 具体的なタスク実行定義 (`[type]-[action]-skill`)。
  - `proc-creating-skills-skill`, `proc-disciplined-dev-skill`, `proc-importing-skill`, `proc-reviewing-code-skill`
