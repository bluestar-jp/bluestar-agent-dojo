---
name: branch-coverage-testing
description: 分岐網羅テストを適用し、コード内のすべての分岐（true/false）を最低1回実行するテストケースを導出する。ソースコードが提供されている場合にホワイトボックステストの基本技法として使用する。
---

# Branch Coverage Testing

- Purpose: 分岐網羅テストによるテストケース導出
- Scope: 単一テスト技法の適用

## 実行手順

1. **対象コードの分岐点の特定**
   - if/else文
   - switch/case文
   - 三項演算子
   - 短絡評価（&&, ||）
   - try-catch-finally

2. **各分岐のtrue/false条件の列挙**
   - 各分岐点でtrue/falseの両方の結果を記録
   - 複合条件（A && B）の場合は個別条件も分析

3. **分岐をカバーする最小テストケースセットの設計**
   - すべての分岐結果（true/false）を少なくとも1回実行
   - テストケース数を最小化しつつ100%カバレッジを目指す

4. **複合条件のMC/DC分析（必要に応じて）**
   - 各条件が独立して結果に影響することを検証
   - 安全性が重要なシステムで適用

5. **テストケースの作成とカバレッジ確認**
   - 各テストケースがカバーする分岐を明示
   - カバレッジ率を算出

## 出力形式

```json
{
  "technique": "branch_coverage_testing",
  "requirement_id": "REQ-XXX",
  "test_cases": [
    {
      "id": "TC-BC-001",
      "title": "テストケースのタイトル",
      "preconditions": ["前提条件"],
      "test_data": {
        "input": {},
        "target_branches": ["分岐1:true", "分岐2:false"]
      },
      "steps": ["手順1", "手順2"],
      "expected_result": "期待結果",
      "priority": "high|medium|low",
      "traceability": {
        "requirement_id": "REQ-XXX",
        "technique": "branch_coverage_testing",
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

- **100%カバレッジ達成不可**: 到達不能分岐をデッドコードとして報告
- **複合条件の爆発**: MC/DCで必要最小限のテストケースに絞る
- **暗黙の分岐見落とし**: 短絡評価や例外ハンドラを再チェック

## 参照

詳細基準: `references/technique_guide.md`
