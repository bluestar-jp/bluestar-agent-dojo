---
name: usecase-testing
description: ユースケーステストを適用し、アクターとシステムの対話シナリオからテストケースを導出する。ユーザーワークフローやビジネスプロセスのシナリオが記述されている場合に使用する。
---

# Use Case Testing

- Purpose: ユースケーステストによるテストケース導出
- Scope: 単一テスト技法の適用

## 実行手順

1. **アクターの特定**
   - システムと対話するアクター（ユーザー、外部システム等）を列挙
   - 各アクターの権限レベルを確認

2. **基本フロー（正常シナリオ）の定義**
   - 主要な成功パスをステップごとに定義
   - 各ステップのアクターアクションとシステムレスポンスを明示

3. **代替フロー（バリエーション）の特定**
   - 基本フローから分岐する有効な代替パスを列挙
   - 各代替フローの分岐条件と合流点を明示

4. **例外フロー（エラーシナリオ）の特定**
   - エラー条件とシステムのエラーハンドリングを定義
   - リカバリパスの有無を確認

5. **各フローからテストケースの導出**
   - 基本フロー: 最低1テストケース
   - 各代替フロー: 最低1テストケース
   - 各例外フロー: 最低1テストケース

## 出力形式

```json
{
  "technique": "usecase_testing",
  "requirement_id": "REQ-XXX",
  "test_cases": [
    {
      "id": "TC-UC-001",
      "title": "テストケースのタイトル",
      "preconditions": ["前提条件"],
      "test_data": {
        "actor": "アクター名",
        "flow_type": "basic|alternative|exception",
        "scenario": "シナリオ概要"
      },
      "steps": ["手順1", "手順2"],
      "expected_result": "期待結果",
      "priority": "high|medium|low",
      "traceability": {
        "requirement_id": "REQ-XXX",
        "technique": "usecase_testing",
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

- **フローの粒度が不適切**: 1ステップ=1アクションに分解
- **代替フローの漏れ**: 各ステップで「他に何が起きうるか」を再検討
- **前提条件の不足**: アクターの認証状態やデータ状態を追加

## 参照

詳細基準: `references/technique_guide.md`
