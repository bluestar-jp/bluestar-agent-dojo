---
name: data-flow-testing
description: データフローテストを適用し、変数の定義-使用チェーンを分析して、データに関連する欠陥を検出するテストケースを導出する。ソースコードが提供されており、変数の定義-使用チェーンが複雑な場合に使用する。
---

# Data Flow Testing

- Purpose: データフローテストによるテストケース導出
- Scope: 単一テスト技法の適用

## 実行手順

1. **変数の定義（def）箇所の特定**
   - 変数への代入、パラメータ受け取り、入力読み取りを列挙
   - 各定義にノード番号を付与

2. **変数の使用（use）箇所の特定**
   - c-use（計算使用）: 演算や出力で値を参照
   - p-use（述語使用）: 条件判定で値を参照

3. **定義-使用ペア（du-pair）の列挙**
   - 各変数について定義箇所と使用箇所のペアを作成
   - 定義から使用に至るパスに再定義がないことを確認

4. **各du-pairをカバーするテストパスの設計**
   - all-defs: 各定義が少なくとも1つの使用に到達
   - all-uses: すべてのdu-pairをカバー（推奨）
   - all-du-paths: すべてのdu-pair間のパスをカバー（最強）

5. **テストケースの作成**
   - 各テストパスに対して入力値と期待結果を設定
   - 異常パターン（未定義使用、定義-未使用）を報告

## 出力形式

```json
{
  "technique": "data_flow_testing",
  "requirement_id": "REQ-XXX",
  "test_cases": [
    {
      "id": "TC-DF-001",
      "title": "テストケースのタイトル",
      "preconditions": ["前提条件"],
      "test_data": {
        "input": {},
        "target_variable": "変数名",
        "du_pair": {"def": "ノードX", "use": "ノードY", "use_type": "c-use|p-use"}
      },
      "steps": ["手順1", "手順2"],
      "expected_result": "期待結果",
      "priority": "high|medium|low",
      "traceability": {
        "requirement_id": "REQ-XXX",
        "technique": "data_flow_testing",
        "rationale": "導出根拠"
      }
    }
  ],
  "coverage_analysis": {
    "identified": 0,
    "covered": 0,
    "percentage": 100
  }
}
```

## 自己修正

- **du-pairが膨大**: all-defsカバレッジに絞り、リスクの高い変数のみall-usesを適用
- **ポインタ/参照の追跡困難**: エイリアス解析を簡略化し、保守的に報告
- **異常パターン検出**: 未定義使用や定義-未使用をバグ候補として報告

## 参照

詳細基準: `references/technique_guide.md`
