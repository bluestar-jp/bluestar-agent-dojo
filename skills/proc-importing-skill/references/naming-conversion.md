# 命名規則変換ルール

- Purpose: 外部定義ファイルの名前をbluestar-agent-dojo標準に変換する
- Scope: スキルとエージェントの命名規則

## スキルの命名規則

### フォーマット

```text
[type]-[action]-skill
```text

### type の判定基準

外部定義の特徴から適切なtypeを判定します。

#### proc (Procedure)

以下の特徴がある場合:

- 複数ステップのワークフローを含む
- 「Step 1」「Step 2」のような段階的な指示
- Plan → Execute → Verify のようなフロー
- 並列処理や複雑なオーケストレーション

### スキルの命名規則の例

- `code-reviewer` → `proc-reviewing-code-skill`
- `deploy-manager` → `proc-deploying-skill`
- `test-runner` → `proc-running-tests-skill`

#### action (Single Action)

以下の特徴がある場合:

- 単一の明確なアクション
- 入力 → 処理 → 出力のシンプルな構造
- 他のスキルから呼び出されることを想定
- 独立した小さな機能

### スキルの命名規則の例

- `formatter` → `action-formatting-code-skill`
- `linter` → `action-linting-code-skill`
- `validator` → `action-validating-input-skill`

#### cond (Conditional Instructions)

以下の特徴がある場合:

- 条件分岐が主体
- 状況判断やルーティング
- 「IF...THEN...」構造が多い
- 意思決定や選択ロジック

### スキルの命名規則の例

- `priority-judge` → `cond-judging-priority-skill`
- `router` → `cond-routing-requests-skill`
- `autonomy-chooser` → `cond-choosing-autonomy-skill`

### action の命名

- 動名詞形（-ing形）を使用
- ケバブケース（kebab-case）
- 明確で簡潔な動詞を選択

### スキルの命名規則の変換例

- `CodeFormatter` → `formatting-code`
- `test_runner` → `running-tests`
- `DeployToProduction` → `deploying-to-production`

### suffix の確認

- 必ず `-skill` で終わる
- 元の名前に `skill` が含まれていても重複しない
  - 例: `formatting-skill` → `action-formatting-code-skill` （`-skill-skill`にしない）

## エージェントの命名規則

### フォーマット

```text
[role]-[specialty]
```text

### role の判定基準

#### shihan (師範 - 統合型)

以下の特徴がある場合:

- 戦略立案やタスク委任
- 複数エージェントのオーケストレーション
- ルーティングや並列制御
- 全体の統括や調整

### エージェントの命名規則の例

- `orchestrator` → `shihan-orchestrator`
- `task-router` → `shihan-routing`
- `parallel-executor` → `shihan-parallel`

#### deshi (弟子 - 専門型)

以下の特徴がある場合:

- 特定ドメインの専門知識
- 個別タスクの実行
- 技術的な専門性
- 独立した機能単位

### エージェントの命名規則の例

- `skill-creator` → `deshi-skill-expert`
- `code-analyzer` → `deshi-code-analyst`
- `security-expert` → `deshi-security-expert`

### specialty の命名

- ケバブケース（kebab-case）
- 役割や専門分野を表す名詞
- 簡潔で明確な名前

### エージェントの命名規則の変換例

- `SkillCreator` → `skill-expert`
- `code_reviewer` → `code-reviewer`
- `SecurityAnalyst` → `security-expert`

## 変換アルゴリズム

### 1. 既存の命名パターンを検出

```python
import re

def detect_pattern(name: str) -> dict:
    """既存の命名パターンを検出"""
    patterns = {
        'camel': re.compile(r'^[a-z]+([A-Z][a-z]+)+$'),
        'pascal': re.compile(r'^[A-Z][a-z]+([A-Z][a-z]+)+$'),
        'snake': re.compile(r'^[a-z]+(_[a-z]+)+$'),
        'kebab': re.compile(r'^[a-z]+(-[a-z]+)+$'),
    }

    for pattern_name, pattern in patterns.items():
        if pattern.match(name):
            return {'type': pattern_name, 'name': name}

    return {'type': 'unknown', 'name': name}
```text

### 2. ケバブケースへの統一

```python
def to_kebab_case(name: str, pattern_type: str) -> str:
    """任意のケースからケバブケースに変換"""
    if pattern_type == 'camel' or pattern_type == 'pascal':
        # CamelCase → kebab-case
        name = re.sub('([a-z0-9])([A-Z])', r'\1-\2', name)
        return name.lower()

    elif pattern_type == 'snake':
        # snake_case → kebab-case
        return name.replace('_', '-')

    elif pattern_type == 'kebab':
        return name.lower()

    else:
        # 不明な場合はそのまま小文字化
        return name.lower()
```text

### 3. プレフィックスとサフィックスの追加

```python
def apply_convention(
    name: str,
    resource_type: str,  # 'skill' or 'agent'
    sub_type: str  # 'proc'/'action'/'cond' or 'shihan'/'deshi'
) -> str:
    """命名規則を適用"""

    # 既存のプレフィックス・サフィックスを除去
|name = re.sub(r'^(proc | action | cond | shihan | deshi)-', '', name)|
    name = re.sub(r'-skill$', '', name)

    if resource_type == 'skill':
        return f"{sub_type}-{name}-skill"
    elif resource_type == 'agent':
        return f"{sub_type}-{name}"
    else:
        raise ValueError(f"Unknown resource_type: {resource_type}")
```text

## 競合の処理

### 完全一致の場合

既存のリソースと名前が完全一致:

```python
def handle_exact_match(name: str) -> str:
    """完全一致時の処理"""
    # オプション1: バージョン番号を付与
    return f"{name}-v2"

    # オプション2: タイムスタンプを付与
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    return f"{name}-{timestamp}"

    # オプション3: ユーザーに確認
    # (実装はインタラクティブに行う)
```text

### 類似名の場合

既存のリソースと名前が類似:

```python
def suggest_alternative(name: str, existing: list) -> list:
    """代替名を提案"""
    suggestions = []

    # より具体的な名前を提案
    suggestions.append(f"{name}-extended")
    suggestions.append(f"{name}-custom")
    suggestions.append(f"community-{name}")

    return suggestions
```text

## 使用例

### スキルの変換例

```python
# 入力
original_name = "CodeFormatter"
resource_type = "skill"
characteristics = {"single_action": True, "workflow": False}

# 処理
pattern = detect_pattern(original_name)  # {'type': 'pascal', ...}
kebab = to_kebab_case(original_name, pattern['type'])  # 'code-formatter'
sub_type = determine_skill_type(characteristics)  # 'action'
final_name = apply_convention(kebab, resource_type, sub_type)

# 出力
print(final_name)  # 'action-formatting-code-skill'
```text

### エージェントの変換例

```python
# 入力
original_name = "security_analyst"
resource_type = "agent"
characteristics = {"orchestration": False, "specialization": True}

# 処理
pattern = detect_pattern(original_name)  # {'type': 'snake', ...}
kebab = to_kebab_case(original_name, pattern['type'])  # 'security-analyst'
sub_type = determine_agent_role(characteristics)  # 'deshi'
final_name = apply_convention(kebab, resource_type, sub_type)

# 出力
print(final_name)  # 'deshi-security-analyst'
```text

## 変換マトリックス

| 元の名前 | リソース種別 | 特徴 | 変換後 |
|---------|------------|------|--------|
| CodeReviewer | skill | 複数ステップ | proc-reviewing-code-skill |
| test_runner | skill | 複数ステップ | proc-running-tests-skill |
| Formatter | skill | 単一アクション | action-formatting-code-skill |
| priorityJudge | skill | 条件判断 | cond-judging-priority-skill |
| Orchestrator | agent | タスク委任 | shihan-orchestrator |
| skill_creator | agent | 専門知識 | deshi-skill-expert |
| SecurityExpert | agent | 専門知識 | deshi-security-expert |

## 注意事項

- 動詞は必ず動名詞形（-ing形）にする
  - ❌ `create-skill` → ✅ `creating-skill`
  - ❌ `deploy-app` → ✅ `deploying-app`

- 冗長な単語は削除
  - ❌ `skill-skill-creator` → ✅ `skill-creator`
  - ❌ `agent-orchestrator-agent` → ✅ `orchestrator`

- 明確性を優先
  - 曖昧な名前は具体化: `handler` → `handling-requests`
  - 汎用的すぎる名前は避ける: `manager` → `managing-deployments`

- 一貫性の維持
  - 既存のスキル/エージェント名と類似のパターンを使用
  - プロジェクト内での用語統一
