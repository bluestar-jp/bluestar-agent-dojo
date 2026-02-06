---
name: pairwise-testing
description: ペアワイズテスト（オールペア法）を適用し、パラメータ間の2因子間相互作用を効率的にカバーするテストケースを導出する。3つ以上の独立パラメータがあり、全組合せテストが現実的でない場合に使用する。
---

# Pairwise Testing

- Purpose: ペアワイズテストによるテストケース導出
- Scope: 単一テスト技法の適用

## 実行手順

1. **テスト対象パラメータと値の列挙**
   - 各パラメータの取りうる値（レベル）を定義
   - パラメータ数と各レベル数を確認

2. **パラメータ間の相互作用分析**
   - 相互作用が期待されるパラメータペアを特定
   - 制約条件（無効な組合せ）を列挙

3. **ペアワイズ組合せ表の生成**
   - すべての2因子間の値の組合せが少なくとも1回出現する最小セットを生成
   - 直交配列またはオールペアアルゴリズムを適用

4. **制約条件の適用（無効な組合せの除外）**
   - 技術的に不可能な組合せを除外
   - 除外した組合せの理由を記録

5. **テストケースの作成**
   - 各行を1つのテストケースとして記述
   - 期待結果を付与

## 出力形式

```json
{
  "technique": "pairwise_testing",
  "requirement_id": "REQ-XXX",
  "test_cases": [
    {
      "id": "TC-PW-001",
      "title": "テストケースのタイトル",
      "preconditions": ["前提条件"],
      "test_data": {
        "parameters": {
          "param1": "値1",
          "param2": "値2",
          "param3": "値3"
        },
        "covered_pairs": [["param1=値1", "param2=値2"]]
      },
      "steps": ["手順1", "手順2"],
      "expected_result": "期待結果",
      "priority": "high|medium|low",
      "traceability": {
        "requirement_id": "REQ-XXX",
        "technique": "pairwise_testing",
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

- **パラメータのレベル数が多すぎる**: 同値分割で値を集約してから適用
- **制約条件が複雑**: 制約充足ソルバーの利用を検討
- **2因子では不十分**: リスクの高いパラメータ群にN因子カバレッジを適用

## 参照

詳細基準: `references/technique_guide.md`
