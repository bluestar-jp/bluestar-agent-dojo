# Project Summary: BlueStar Agent Dojo

## 目的
BlueStarにおけるAIエージェントの定義、設計、設定を一元管理するリポジトリ。「道場」として、エージェントの定義（プロンプト）を管理・育成する。特定のAIツールに依存しないコア定義を目指す。

## 構造
*   **shihan/** (師範): 正規・安定版 (Stable) の定義。
*   **deshi/** (弟子): 実験・開発版 (Experimental) の定義。
*   **toranomaki/** (虎の巻): 全体設計、ルール等の正本ドキュメント。
*   **zatsunomaki/** (雑の巻): アイデア、草稿。
*   **menkyokaiden/** (免許皆伝): ツール用設定ファイルへの変換成果物。

## 技術スタック
*   Markdown (.md): ドキュメントおよびエージェント定義。
*   YAML (.yml): プロジェクト設定。
