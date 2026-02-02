# bluestar-agent-dojo

BlueStarのエコシステムを支える自律型AIエージェントの道場です。
本プロジェクトでは、サブエージェントを「師範」と「弟子」、エージェントスキル「龍の巻」と「虎の巻」の2つの軸で定義し、AIエージェントの自律性を実現します。

## 📂 ディレクトリ構成

```text
.
├── agents/             # サブエージェント
│   ├── deshi/          # 弟子: 専門型エージェント
│   └── shihan/         # 師範: 統合型エージェント
├── skills/             # エージェントスキル
│   ├── ryu_no_maki/    # 龍の巻: 知識型スキル
│   └── tora_no_maki/   # 虎の巻: 指示型スキル
└── menkyokaiden/       # 各種AIエージェント向けの変換用リソース
```

## 🤖 カスタムサブエージェント

エージェントの基本動作や役割に応じた構成を定義します。

- **弟子 (Deshi)**: `agents/deshi/`
  - 自律的な学習とタスク実行のコア。収集、生成、検証などのライフサイクルを管理。
- **師範 (Shihan)**: `agents/shihan/`
  - 複数の弟子やスキルの統率、ルーティング、並列処理の最適化。

## 🏗 カスタムエージェントスキル

エージェントスキルを「知識型」と「指示型」に分類して管理します。

### 🐉 龍の巻 (ryunomaki) - 知識型

エージェントが判断を下すための背景情報、ルール、専門知識を格納します。

- **Context (文脈)**: `skills/ryunomaki/context/`
  - プロジェクトの目的、歴史、現在の状況など。
- **Guidelines (指針)**: `skills/ryunomaki/guidelines/`
  - コーディング規約、品質基準、倫理規定。
- **References (参照)**: `skills/ryunomaki/references/`
  - 技術仕様書、APIリファレンス、外部ドキュメント。

### 🐯 虎の巻 (toranomaki) - 指示型

エージェントが実行すべき具体的なアクションやワークフローを定義します。

- **Single Action (単一行動)**: `skills/toranomaki/single_action/`
  - 明確な入力と出力を持つ単一のタスク定義。
- **Procedure (手順)**: `skills/toranomaki/procedure/`
  - 複雑な課題を解決するためのマルチステップなプロシージャ。
- **Conditional Instructions (条件付指示)**: `skills/toranomaki/conditional_instructions/`
  - 状況やフィードバックに応じて分岐・ループする高度なロジック。

## 📜 ライセンス

[Apache License 2.0](./LICENSE)

## 📝 免責事項

本プロジェクトの使用によって生じたいかなる損害（データ損失、予期しないAPIコスト、システム障害等）についても、開発者は一切の責任を負いません。
AIエージェントの自律動作による影響を含め、すべて利用者自身の責任においてご利用ください。
