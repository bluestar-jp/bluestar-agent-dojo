# BlueStar Agent Dojo

BlueStarのエコシステムを支える自律型AIエージェントの「道場（スキル・知識育成リポジトリ）」です。
本プロジェクトでは、エージェントの能力を「知識（龍の巻）」と「指示（虎の巻）」の2つの軸で定義し、高度な自律性を実現します。

## 🏗 カスタムスキル・アーキテクチャ

エージェントのスキルを「静的な知恵」と「動的な振る舞い」に分類して管理します。

### 1. 🐉 龍の巻 (Ryu-no-maki) - 知識型 (Knowledge-based)
エージェントが判断を下すための背景情報、ルール、専門知識を格納します。

- **Context (文脈)**: `skills/ryu_no_maki/context/`
  - プロジェクトの目的、歴史、現在の状況など。
- **Guidelines (指針)**: `skills/ryu_no_maki/guidelines/`
  - コーディング規約、品質基準、倫理規定。
- **References (参照)**: `skills/ryu_no_maki/references/`
  - 技術仕様書、APIリファレンス、外部ドキュメント。

### 2. 🐯 虎の巻 (Tora-no-maki) - 指示型 (Instruction-based)
エージェントが実行すべき具体的なアクションやワークフローを定義します。

- **Single Action (単一行動)**: `skills/tora_no_maki/single_action/`
  - 明確な入力と出力を持つ単一のタスク定義。
- **Procedure (手順)**: `skills/tora_no_maki/procedure/`
  - 複雑な課題を解決するためのマルチステップなプロシージャ。
- **Conditional Instructions (条件付指示)**: `skills/tora_no_maki/conditional_instructions/`
  - 状況やフィードバックに応じて分岐・ループする高度なロジック。

## 📂 ディレクトリ構成

```text
bluestar-agent-dojo/
├── skills/
│   ├── ryu_no_maki/    # 龍の巻（知識型）
│   └── tora_no_maki/    # 虎の巻（指示型）
├── menkyokaiden/       # 各種AIツール向けの設定ファイル出力先
└── .serena/            # エージェントの内部設定と記憶
```

## 📜 ライセンス
[Apache License 2.0](./LICENSE)
