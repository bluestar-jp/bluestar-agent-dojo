---
name: action-state-transition-testing-skill
description: 状態遷移テストを適用し、システムの状態とイベントに基づく遷移パスからテストケースを導出する。システムに明確な状態遷移（ステータス変更、ライフサイクル管理等）が存在する場合に使用する。
---

# State Transition Testing

- Purpose: 状態遷移テストによるテストケース導出
- Scope: 単一テスト技法の適用

## 実行手順

1. **状態の列挙**
   - システムが取りうるすべての状態を特定する
   - 初期状態と終了状態を明示する

2. **イベント（トリガー）の特定**
   - 各状態遷移を引き起こすイベントを列挙する
   - イベントに付随するガード条件を特定する

3. **状態遷移図/表の作成**
   - 状態遷移図: 状態をノード、遷移をエッジで表現
   - 状態遷移表: 現状態×イベントのマトリクスで次状態を定義

4. **有効遷移のテストケース作成（0-switchカバレッジ）**
   - すべての有効な遷移を少なくとも1回実行するテストケースを設計
   - 各テストケースで遷移前の状態、イベント、期待される次状態を明示

5. **無効遷移（不正イベント）のテストケース作成**
   - 状態遷移表の空セル（未定義遷移）を特定
   - 各無効遷移に対してシステムが適切にエラー処理することを検証

6. **必要に応じてN-switchカバレッジの追加**
   - 1-switch: 連続する2つの遷移の組合せをカバー
   - リスクの高い遷移シーケンスを優先

## 出力形式

```json
{
  "technique": "state_transition_testing",
  "requirement_id": "REQ-XXX",
  "test_cases": [
    {
      "id": "TC-ST-001",
      "title": "テストケースのタイトル",
      "preconditions": ["初期状態の設定"],
      "test_data": {
        "initial_state": "状態A",
        "event": "イベント1",
        "guard": "ガード条件"
      },
      "steps": ["状態Aを設定", "イベント1を発生させる"],
      "expected_result": "状態Bに遷移する",
      "priority": "high|medium|low",
      "traceability": {
        "requirement_id": "REQ-XXX",
        "technique": "state_transition_testing",
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

- **状態の特定漏れ**: 要件を再読し、暗黙的な状態（初期化中、エラー状態等）を追加
- **遷移の矛盾**: 状態遷移表で非決定的な遷移がないか検証
- **無効遷移の扱い不明**: ユーザーに期待動作を確認

## 参照

詳細基準: `references/technique_guide.md`
