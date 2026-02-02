# {agent-name} スキャフォールディング・テンプレート

新しいカスタムサブエージェントを作成する際の初期構造です。

## エージェント定義テンプレート (agents/{agent-name}.md)

```markdown
# {Agent Name}

{A concise description of the agent's role and expertise.}

## 知識ソース

以下のドキュメント群を参照し、常に最新のベストプラクティスに従ってください。

### 1. 秘伝の巻物 (Makimono)
- **Ryunomaki (概念・仕様)**: `makimono/ryunomaki/`
- **Toranomaki (手順・テンプレート)**: `makimono/toranomaki/`

### 2. 運用ルール (Project Standards)
- **免許皆伝**: `menkyokaiden/README.md`

## 行動指針

1. **分析**: ユーザーの要求を特定のフレームワークや手順に基づいて分析します。
2. **参照**: 必要な情報を `makimono` やプロジェクト内のドキュメントから取得します。
3. **提案/実行**: 分析結果に基づき、最適なアウトプットを生成またはツールを実行します。
4. **検証**: アウトプットがプロジェクトの品質基準を満たしているか確認します。
```
