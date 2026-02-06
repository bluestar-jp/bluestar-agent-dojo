---
name: control-flow-testing
description: 制御フローテストを適用し、プログラムの制御構造（分岐、ループ、例外処理）を分析してテストケースを導出する。ソースコードが提供されており、ループやネスト（深度3以上）がある場合に使用する。
---

# Control Flow Testing

- Purpose: 制御フローテストによるテストケース導出
- Scope: 単一テスト技法の適用

## 実行手順

1. **対象コードの制御フローグラフ（CFG）の作成**
   - 基本ブロック（ノード）の特定
   - 制御の流れ（エッジ）の特定
   - 開始ノードと終了ノードの明示

2. **ノードとエッジの特定**
   - 分岐ノード: if, switch, ternary
   - 結合ノード: 分岐の合流点
   - ループノード: for, while, do-while

3. **独立パスの特定（サイクロマティック複雑度）**
   - V(G) = E - N + 2P で複雑度を計算
   - 基底パスセット（独立パスの集合）を導出

4. **各独立パスのテストケース作成**
   - 各パスを通過するための入力条件を特定
   - 期待結果を各パスの出口条件から導出

5. **ループ境界テスト**
   - 0回実行（ループスキップ）
   - 1回実行
   - 典型的な回数の実行
   - 最大回数の実行（境界値）

## 出力形式

```json
{
  "technique": "control_flow_testing",
  "requirement_id": "REQ-XXX",
  "test_cases": [
    {
      "id": "TC-CF-001",
      "title": "テストケースのタイトル",
      "preconditions": ["前提条件"],
      "test_data": {
        "input": {},
        "target_path": "パス記述（例: 1→2→3→5→7）",
        "cyclomatic_complexity": 0
      },
      "steps": ["手順1", "手順2"],
      "expected_result": "期待結果",
      "priority": "high|medium|low",
      "traceability": {
        "requirement_id": "REQ-XXX",
        "technique": "control_flow_testing",
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

- **複雑度が高すぎる（V(G)>20）**: 関数分割を推奨しつつ、リスクベースでパスを選択
- **到達不能パス**: デッドコードとして報告し、テスト対象から除外
- **例外パスの特定漏れ**: try-catch/throw構造を再解析

## 参照

詳細基準: `references/technique_guide.md`
