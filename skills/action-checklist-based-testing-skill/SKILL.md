---
name: checklist-based-testing
description: チェックリストベーステストを適用し、ドメイン標準や組織の品質基準に基づく体系的なチェック項目からテストケースを導出する。経験ベーステストとしてドメイン標準チェックを体系的に適用する場合に使用する。
---

# Checklist-Based Testing

- Purpose: チェックリストベーステストによるテストケース導出
- Scope: 単一テスト技法の適用

## 実行手順

1. **対象ドメインの標準チェックリスト選択**
   - 汎用チェックリスト（入力検証、エラーハンドリング、セキュリティ等）
   - ドメイン別チェックリスト（Web API、DB、ファイル処理等）
   - 組織固有のチェックリスト（過去の品質基準）

2. **要件に応じたチェック項目のカスタマイズ**
   - 要件に関連する項目のフィルタリング
   - 要件固有の追加項目の追加

3. **各チェック項目の適用可否判断**
   - 適用可能: テストケース導出対象
   - 適用不可: 理由を記録してスキップ
   - 要確認: ユーザーに適用可否を確認

4. **適用可能項目からテストケースの導出**
   - 各チェック項目を具体的なテスト条件に変換
   - テストデータと期待結果を設定

5. **チェックリストのカバレッジ確認**
   - 適用項目のカバー率を算出
   - 未カバー項目の理由を記録

## 出力形式

```json
{
  "technique": "checklist_based_testing",
  "requirement_id": "REQ-XXX",
  "test_cases": [
    {
      "id": "TC-CB-001",
      "title": "テストケースのタイトル",
      "preconditions": ["前提条件"],
      "test_data": {
        "input": {},
        "checklist_category": "カテゴリ名",
        "checklist_item": "チェック項目"
      },
      "steps": ["手順1", "手順2"],
      "expected_result": "期待結果",
      "priority": "high|medium|low",
      "traceability": {
        "requirement_id": "REQ-XXX",
        "technique": "checklist_based_testing",
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

- **チェックリストが古い/不適切**: 要件に合わせて項目を更新
- **項目が一般的すぎる**: 要件の具体的なコンテキストに特化
- **他技法との重複**: 同値分割等で導出済みのケースはタグ付けのみ

## 参照

詳細基準: `references/technique_guide.md`
