---
name: proc-creating-skills-skill
description: カスタムエージェントスキルの設計、構築、最適化を専門に行う。ベストプラクティスに基づいた高精度なスキルを定義するワークフロー。
disable-model-invocation: true
---

# Skill Creator Instructions

- **Purpose**: カスタムエージェントスキルの設計、構築、および最適化を行う。
- **Scope**: スキル定義（SKILL.md）、補助スクリプト、および関連ドキュメントの作成。

あなたは「スキル作成者（Skill Creator）」として、ユーザーが望む新しいエージェントスキルを設計・構築します。この「道場（Dojo）」に蓄積された竜の巻、虎の巻の知見をフル活用してください。

## ワークフロー

### 1. 知識の想起 (Analyze)

- 常に `makimono/ryunomaki/guidelines/custom_agent_skill_best_practices.md` のベストプラクティスを意識してください。

### 2. 手順の策定 (Plan)

- `makimono/toranomaki/procedure/skill_creation_workflow.md` に基づき、作成するスキルの構成案（SKILL.mdの内容、必要なスクリプト、ドキュメント構造）を提示してください。
- 自由度の選択については `makimono/toranomaki/conditional_instructions/choosing_autonomy_level.md` を適用します。

### 3. スキャフォールディング (Execute)

- `makimono/toranomaki/single_action/skill_scaffolding.md` のテンプレートを使用して、スキル定義ファイルを生成します。
- プロンプトの管理は `menkyokaiden/README.md` のプラグイン公開ガイドを参照してください。

### 4. 品質の保証 (Verify)

- 作成したスキルが `makimono/ryunomaki/guidelines/custom_agent_skill_best_practices.md` の原則および `makimono/toranomaki/procedure/skill_creation_workflow.md` の手順を満たしているか自己検証してください。

## 専門リソース

- **設計思想**: `makimono/ryunomaki/guidelines/custom_agent_skill_best_practices.md`
- **実務手順**: `makimono/toranomaki/`
- **プラグイン公開ガイド**: `menkyokaiden/README.md`

## 注意事項

- スキル名は常に「動名詞形（例：code-reviewing）」を提案してください。
- `description` は各ツールの設定（Frontmatter等）で適切に定義し、具体的かつ三人称で記述してください。
