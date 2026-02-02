# bluestar-agent-dojo

BlueStarのエコシステムを支える自律型AIエージェントの道場です。
本プロジェクトでは、全エージェントで共有する知見を「巻物（makimono）」として集約し、それを活用するサブエージェント（「師範」と「弟子」）、および具体的なタスクを実行するエージェントスキルを定義することで、AIエージェントの自律性を実現させるために鍛錬を行います。

## 📂 ディレクトリ構成

```text
bluestar-agent-dojo/
├── makimono/           # 巻物: 全エージェント共有の知識と手順
│   ├── ryunomaki/      # 龍の巻: 知識型リソース
│   └── toranomaki/     # 虎の巻: 指示型リソース
├── agents/             # サブエージェント
│   ├── deshi-*/        # 弟子: 専門型エージェント
│   └── shihan-*/       # 師範: 統合型エージェント
├── skills/             # エージェントスキル
│   └── [type]-*-skill/ # 具体的なスキル定義
└── menkyokaiden/       # 各種AIエージェント向けの変換用リソース
```


## 🤖 カスタムサブエージェント

サブエージェントを役割に基づき「弟子」と「師範」に分類し、`[role]-[specialty]` の形式で管理します。

### 👶 弟子（deshi-*） - 専門型エージェント

特定のタスク、ドメインに関連した専門知識を持ち、指示に従って行動します。

- **Knowledge (知識)**: `agents/deshi-*/knowledge/`
  - 特定のドメインやタスクに必要な背景知識や専門データ。
- **Rules (規約)**: `agents/deshi-*/rules/`
  - 弟子が遵守すべき特定の動作ルール、制約、振る舞いの定義。
- **Collection (収集)**: `agents/deshi-*/collection/`
  - 外部ソースからの情報収集やデータ抽出のプロトコル。
- **Generation (生成)**: `agents/deshi-*/generation/`
  - コード、ドキュメント、コンテンツの生成ガイドライン。
- **Verification (検証)**: `agents/deshi-*/verification/`
  - 成果物の妥当性、正確性、品質を担保するためのテスト・評価。

### 👴 師範（shihan-*） - 統合型エージェント

複数の弟子エージェントを管理し、全体の戦略立案やタスクの割り当てを行います。

- **Routing (ルーティング)**: `agents/shihan-*/routing/`
  - ユーザーの要求を分析し、最適な弟子エージェントへタスクを振り分けるロジック。
- **Parallel (並列制御)**: `agents/shihan-*/parallel/`
  - 複数の弟子を並列に動作させ、結果を統合するためのオーケストレーション。
- **Sequential (シーケンシャル制御)**: `agents/shihan-*/sequential/`
  - 複数の弟子を順番に動作させ、前のステップの結果を次の弟子へ引き継ぐ直列的なワークフロー。


## 📜 巻物（Shared Makimono）

AIエージェントが参照する共有リソースです。

### 🐉 龍の巻 (ryunomaki) - 知識型
エージェントが判断を下すための背景情報、ルール、専門知識。
- `makimono/ryunomaki/guidelines/`: ベストプラクティス、設計原則。
- `makimono/ryunomaki/specs/`: 技術仕様、APIリファレンス。

### 🐯 虎の巻 (toranomaki) - 手順型
エージェントが実行すべき具体的なアクションやワークフローの雛形。
- `makimono/toranomaki/procedure/`: マルチステップなプロシージャ。
- `makimono/toranomaki/single_action/`: 単一のタスク定義。

## 🏗 カスタムエージェントスキル（Skills）

具体的なタスクを実行するための定義ファイルです。`[type]-[action]-skill` の形式で管理されます。

- **Procedure (`proc-*-skill`)**: 複数ステップの手順を実行するスキル。
- **Single Action (`action-*-skill`)**: 単一のアクションを実行するスキル。
- **Conditional (`cond-*-skill`)**: 状況に応じて分岐する高度なロジック。


## 📜 ライセンス

[Apache License 2.0](./LICENSE)


## 📝 免責事項

本プロジェクトの使用によって生じたいかなる損害（データ損失、予期しないAPIコスト、システム障害等）についても、開発者は一切の責任を負いません。
AIエージェントの自律動作による影響を含め、すべて利用者自身の責任においてご利用ください。
