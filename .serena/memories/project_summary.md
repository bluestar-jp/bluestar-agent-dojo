# Project Summary: BlueStar Agent Dojo

## Purpose
AIエージェントの「道場」として、BlueStarエコシステムにおける自律型エージェントの定義、ペルソナ、知識、行動規範を一元管理・育成するためのリポジトリです。特定のツールに依存しないコア定義を保持し、実用的な設定へと変換します。

## Architecture
カスタムスキルを「知識（龍の巻）」と「指示（虎の巻）」の2つの軸で構成します：
1. **龍の巻 (Ryu-no-maki) - 知識型**: コンテキスト、ガイドライン、リファレンスなどの静的なナレッジ。
2. **虎の巻 (Tora-no-maki) - 指示型**: 単一アクション、プロシージャ、条件付指示などの動的なアクション定義。

## Directory Structure
- `skills/ryu_no_maki/`: 知識型スキルの定義（context, guidelines, references）。
- `skills/tora_no_maki/`: 指示型スキルの定義（single_action, procedure, conditional_instructions）。
- `menkyokaiden/`: 各種AIツール向けの設定ファイル出力先。

## Core Documents
- `README.md`: プロジェクト全体の概要。
- `skills/ryu_no_maki/guidelines/`: スキル開発・運用における共通ガイドライン。
