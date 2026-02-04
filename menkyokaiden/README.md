# 免許皆伝 (Menkyokaiden)

このプロジェクトにおけるAIエージェント/スキルのプロンプト管理に関する運用ルール（Single Source of Truth）を定義します。

## 運用思想：コンテキスト・エンジニアリング中心設計

AIエージェントのパフォーマンスを最大化するため、プロンプト（指示）の「実体」と「適用（コンテキスト注入）」を明確に分離します。
これにより、特定のAIエージェント（Gemini CLI, Claude Code, Devinなど）の仕様変更に左右されず、純粋な「指示の質」を維持・向上させることを目的とします。

## 運用ルール

### 1. Source of Truth (SoT)

プロンプトの「実体（Markdown本文）」は、以下のディレクトリで一元管理します。ここにはツール固有の設定（Frontmatter等）は含めません。

- **`agents/`**: サブエージェント（人格、役割）のプロンプト実体
- **`skills/`**: 特定技能（スキル、手順）のプロンプト実体

### 2. Context Injection (各ツールへの適用)

各AIツール向けのディレクトリ（`.gemini/`, `.claude/` 等）には、SoTを参照してコンテキストを注入するための「ラッパーファイル」を配置します。

- **構成原則**:
  - **Frontmatter**: 各ツールの仕様に合わせたメタデータを定義。
  - **Body**: 具体的な指示は書かず、`@agents/xxx.md` や `@skills/xxx.md` の記法（または各ツールのInclude機能）を用いてSoTを読み込ませる。

### ディレクトリ構成図

```text
bluestar-agent-dojo/
├── agents/                      # 【SoT】エージェント定義（純粋Markdown）
│   └── deshi_skill_expert.md
├── skills/                      # 【SoT】スキル定義（純粋Markdown）
│   └── proc-creating-skills-skill.md
│
├── .gemini/                     # 【Context】Gemini CLI用アダプター
│   ├── agents/
│   │   └── deshi-skill-expert.md  # -> @agents/deshi_skill_expert.md
│   └── skills/
│       └── proc-creating-skills-skill/
│           └── SKILL.md           # -> @skills/proc-creating-skills-skill.md
│
└── .claude/                     # 【Context】Claude Code用アダプター
    └── ...
```

### 修正・追加フロー

1. **SoTの編集**: `agents/` または `skills/` 内のファイルを新規作成・編集します。
2. **アダプターの配置**: 新規追加の場合、`.gemini/`, `.claude/` 配下にラッパーファイルを配置します。
3. **整合性チェック**: 以下のコマンドを実行して、修正漏れがないか確認します。

   ```bash
   python3 .github/scripts/verify_sync.py
   ```

4. **反映**: 各エージェントは実行時に最新のSoTを自動的に読み込みます。
