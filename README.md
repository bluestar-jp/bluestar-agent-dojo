# BlueStar Agent Dojo

AIエージェントのスキルと知識を育成するための「道場」です。

## ディレクトリ構造

本プロジェクトでは、カスタムスキルを以下の構造で管理しています。

### 龍の巻 (Ryu-no-maki) - 知識型
`skills/ryu_no_maki/`
- `context/`: プロジェクト背景や目的。
- `guidelines/`: 開発・運用の指針。
- `references/`: 技術仕様や外部リファレンス。

### 虎の巻 (Tora-no-maki) - 指示型
`skills/tora_no_maki/`
- `single_action/`: 単一の明確なアクション。
- `procedure/`: 複数のステップからなる手順。
- `conditional_instructions/`: 状況に応じた条件分岐を伴う指示。

## その他のディレクトリ
- `menkyokaiden/`: 成果物（各種AI設定ファイル）の出力先。
- `.serena/`: エージェントの内部設定と記憶。
