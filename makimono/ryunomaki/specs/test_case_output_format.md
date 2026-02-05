# Test Case Output Format Specification

- Purpose: テスト設計エコシステムの全レイヤーで使用するJSON出力形式の定義
- Scope: Level 1（Skill）, Level 2（Deshi）, Level 3（Shihan）の出力仕様

## Level 1: Skill出力

個別テスト技法が出力するテストケース群。

```json
{
  "technique": "equivalence_partitioning",
  "requirement_id": "REQ-001",
  "test_cases": [
    {
      "id": "TC-EP-001",
      "title": "テストケースのタイトル",
      "preconditions": ["前提条件1", "前提条件2"],
      "test_data": {
        "input": {},
        "partitions": {}
      },
      "steps": ["手順1", "手順2"],
      "expected_result": "期待結果",
      "priority": "high",
      "traceability": {
        "requirement_id": "REQ-001",
        "technique": "equivalence_partitioning",
        "rationale": "導出根拠"
      }
    }
  ],
  "coverage_analysis": {
    "identified": 3,
    "covered": 3,
    "percentage": 100
  }
}
```

### フィールド定義

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `technique` | string | Yes | 技法識別子（スネークケース） |
| `requirement_id` | string | Yes | 対象要件ID |
| `test_cases` | array | Yes | テストケース配列 |
| `test_cases[].id` | string | Yes | `TC-{技法略称}-{連番}` |
| `test_cases[].title` | string | Yes | テストケースの簡潔なタイトル |
| `test_cases[].preconditions` | array | Yes | 前提条件のリスト |
| `test_cases[].test_data` | object | Yes | テストデータ（技法固有） |
| `test_cases[].steps` | array | Yes | 実行手順 |
| `test_cases[].expected_result` | string | Yes | 期待結果 |
| `test_cases[].priority` | string | Yes | `high`, `medium`, `low` |
| `test_cases[].traceability` | object | Yes | トレーサビリティ情報 |
| `coverage_analysis` | object | Yes | カバレッジ分析 |

### テストケースID命名規則

| 技法 | プレフィックス |
| --- | --- |
| equivalence_partitioning | TC-EP |
| boundary_value_analysis | TC-BVA |
| decision_table_testing | TC-DT |
| state_transition_testing | TC-ST |
| usecase_testing | TC-UC |
| pairwise_testing | TC-PW |
| control_flow_testing | TC-CF |
| data_flow_testing | TC-DF |
| branch_coverage_testing | TC-BC |
| error_guessing | TC-EG |
| exploratory_testing | TC-ET |
| checklist_based_testing | TC-CB |

## Level 2: Deshi出力

カテゴリ専門家が複数技法の結果を統合して出力する形式。

```json
{
  "category": "blackbox",
  "techniques_applied": ["equivalence_partitioning", "boundary_value_analysis"],
  "techniques_skipped": [
    {
      "technique": "state_transition_testing",
      "reason": "要件に状態遷移の記述がないため"
    }
  ],
  "test_cases": [],
  "summary": {
    "total_cases": 15,
    "by_priority": {
      "high": 5,
      "medium": 7,
      "low": 3
    },
    "by_technique": {
      "equivalence_partitioning": 8,
      "boundary_value_analysis": 7
    }
  }
}
```

### フィールド定義

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `category` | string | Yes | `blackbox`, `whitebox`, `experience` |
| `techniques_applied` | array | Yes | 適用した技法の識別子リスト |
| `techniques_skipped` | array | Yes | スキップした技法とその理由 |
| `test_cases` | array | Yes | 全技法から統合したテストケース配列 |
| `summary` | object | Yes | 集計情報 |

## Level 3: Shihan統合出力

オーケストレーターが全カテゴリの結果を統合した最終出力。

```json
{
  "test_design_result": {
    "requirement_summary": "要件の要約",
    "categories": [],
    "overall_summary": {
      "total_cases": 35,
      "by_priority": {
        "high": 10,
        "medium": 15,
        "low": 10
      },
      "by_category": {
        "blackbox": 20,
        "whitebox": 10,
        "experience": 5
      }
    },
    "duplicate_removals": [
      {
        "kept": "TC-EP-003",
        "removed": "TC-BVA-001",
        "reason": "同一入力条件・期待結果の重複"
      }
    ],
    "traceability_matrix": {
      "REQ-001": ["TC-EP-001", "TC-BVA-002", "TC-DT-001"]
    }
  }
}
```

### フィールド定義

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `test_design_result` | object | Yes | ルートオブジェクト |
| `requirement_summary` | string | Yes | 要件の要約 |
| `categories` | array | Yes | 各deshiのLevel 2出力配列 |
| `overall_summary` | object | Yes | 全体の集計情報 |
| `duplicate_removals` | array | Yes | 重複排除の記録 |
| `traceability_matrix` | object | Yes | 要件ID → テストケースIDの対応表 |

## priority判定基準

| 優先度 | 基準 |
| --- | --- |
| `high` | 主要機能に直結、障害時の影響大、セキュリティ関連 |
| `medium` | 補助的機能、エッジケース、パフォーマンス関連 |
| `low` | UI/UXの微細な確認、推奨設定の検証 |
