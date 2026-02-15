---
name: action-revising-article-skill
description: ブログ記事レビュー後のフィードバックを処理し、OK/NGに基づいて適切なアクションを決定する。修正プラン策定とループバック先の判断を含む。
---

# Article Revision Decision Skill

- Purpose: レビューフィードバックを処理し、適切なアクションを決定
- Scope: OK/NGの判定、フィードバック→修正アクションのマッピング、ループバック条件

## 入力形式

```json
{
  "review_results": {
    "structure_review": {
      "overall_quality": "good|needs_revision",
      "findings": [...]
    },
    "humanize_review": {
      "overall_quality": "natural|needs_humanizing",
      "findings": [...]
    }
  },
  "user_feedback": {
    "approval": "ok|ng",
    "comments": "ユーザーのコメント（NGの場合）",
    "specific_issues": [
      {
        "paragraph_id": "P2",
        "issue": "コード例の説明が不足"
      }
    ]
  }
}
```

## ワークフロー

### Step 1: フィードバックの分類

`makimono/toranomaki/conditional_instructions/handling_blog_review_feedback.md` を参照し、フィードバックを以下のいずれかに分類：

1. **OK（承認）**: 品質基準を満たし、公開可能
2. **Minor Revision（軽微な修正）**: 部分的な修正で対応可能
3. **Major Revision（大幅な修正）**: 構造的な見直しが必要
4. **Reject（却下・再計画）**: 記事の方向性が根本的に間違っている

### Step 2: 判定基準の適用

#### OK（承認）の判定基準

- [ ] 構造・読みやすさレビューで`critical`問題がゼロ
- [ ] AIっぽさ除去レビューで`high`以上の問題が2件以下
- [ ] ユーザーが内容に合意している
- [ ] 技術的正確性が確認されている

**アクション**: Phase 6 (Generate & Publish) へ進む

---

#### Minor Revision（軽微な修正）の判定基準

- [ ] `medium`以下の問題のみ
- [ ] 修正対象が2-3段落以内
- [ ] 構造の変更が不要
- [ ] 10分以内で修正可能

**アクション**: Phase 3 (Execute) へループバック（対象段落のみ再執筆）

---

#### Major Revision（大幅な修正）の判定基準

- [ ] `critical`または`high`問題が3件以上
- [ ] 修正対象が4段落以上
- [ ] 構造の変更が必要（セクションの追加/削除/順序変更）
- [ ] 30分以上の修正時間が見込まれる

**アクション**: Phase 1 (Plan) へループバック（アウトライン再設計）

---

#### Reject（却下・再計画）の判定基準

- [ ] 記事タイプとテーマが不整合
- [ ] 対象読者が不明確または不適切
- [ ] 技術的に誤った内容が多数
- [ ] 構造が全体的に破綻している

**アクション**: Phase 1 (Plan) へループバック（テーマから再検討）

---

### Step 3: フィードバックタイプのマッピング

#### 内容の修正

**フィードバック例**:

- 「段落P3の説明が不十分」
- 「コード例が動作しない」
- 「専門用語の定義が欠けている」

**マッピング**:

```json
{
  "decision": "minor_revision",
  "target": "specific_paragraphs",
  "paragraphs": ["P3"],
  "action": "段落を再執筆",
  "loop_back_to": "Phase 3 (Execute)"
}
```

---

#### 構造の変更

**フィードバック例**:

- 「セクションの順序が不自然」
- 「まとめが不足している」
- 「前提条件セクションを追加すべき」

**マッピング**:

```json
{
  "decision": "major_revision",
  "target": "article_structure",
  "action": "アウトラインを再構築",
  "loop_back_to": "Phase 1 (Plan)",
  "structural_changes": [
    {
      "type": "add_section",
      "section": "前提条件",
      "position": "after はじめに"
    }
  ]
}
```

---

#### トーンとスタイルの調整

**フィードバック例**:

- 「AIっぽさが残っている」
- 「説明が堅苦しすぎる」

**マッピング**:

```json
{
  "decision": "minor_revision",
  "target": "tone_and_style",
  "action": "AIっぽさ除去レビューを再実行",
  "loop_back_to": "Phase 4 (Verify)"
}
```

---

#### 技術的正確性の修正

**フィードバック例**:

- 「このコードは動作しない」
- 「バージョン情報が古い」
- 「推奨されていない手法を紹介している」

**マッピング**:

```json
{
  "decision": "minor_revision",
  "target": "technical_accuracy",
  "paragraphs": ["P4", "P6"],
  "action": "技術内容を検証し再執筆",
  "loop_back_to": "Phase 3 (Execute)",
  "verification_required": [
    "コード例の動作確認",
    "バージョン情報の最新化"
  ]
}
```

---

### Step 4: 修正プランの生成

#### Minor Revision の修正プラン

```json
{
  "decision": "minor_revision",
  "scope": "targeted",
  "revision_plan": {
    "tasks": [
      {
        "task_id": 1,
        "paragraph_id": "P2",
        "issue": "専門用語の説明不足",
        "action": "「メモ化」の定義を1文追加",
        "estimated_time": "2分"
      },
      {
        "task_id": 2,
        "paragraph_id": "P5",
        "issue": "コード説明が簡素",
        "action": "コードブロック前後に説明を追加",
        "estimated_time": "5分"
      }
    ],
    "total_estimated_time": "7分",
    "loop_back_to": "Phase 3 (Execute)",
    "preserve_paragraphs": ["P1", "P3", "P4", "P6", "P7"]
  }
}
```

#### Major Revision の修正プラン

```json
{
  "decision": "major_revision",
  "scope": "structural",
  "revision_plan": {
    "structural_changes": [
      {
        "type": "add_section",
        "section": "前提条件",
        "position": "after はじめに",
        "paragraphs_to_add": 1
      },
      {
        "type": "reorder_sections",
        "from": ["はじめに", "手順", "前提条件"],
        "to": ["はじめに", "前提条件", "手順"],
        "reason": "前提条件を先に説明すべき"
      }
    ],
    "content_revisions": [
      {
        "paragraph_id": "P1",
        "action": "導入部分を書き直し"
      },
      {
        "paragraph_id": "P3",
        "action": "トランジション追加"
      }
    ],
    "total_paragraphs_affected": 5,
    "total_estimated_time": "40分",
    "loop_back_to": "Phase 1 (Plan)"
  }
}
```

---

## 出力形式

```json
{
  "decision": "ok|minor_revision|major_revision|reject",
  "next_phase": "Phase 6: Generate & Publish|Phase 3: Execute|Phase 1: Plan",
  "revision_plan": {
    "scope": "none|targeted|structural|full_replanning",
    "tasks": [...],
    "loop_back_to": "Phase 3 (Execute)",
    "estimated_time": "7分"
  },
  "recommendations": [
    "段落P2とP3の間にトランジションを追加",
    "専門用語「メモ化」の初出時に定義を追加"
  ],
  "user_confirmation_required": false
}
```

## ループバック戦略

### Phase 1へループバック（再計画）

**条件**:

- 構造的な変更が必要
- セクションの追加/削除が必要
- 記事タイプの変更が必要

**保持する要素**:

- theme（テーマ）
- target_audience（対象読者）
- key_points（キーポイント）

**再作成する要素**:

- outline（アウトライン）
- section_structure（セクション構成）
- paragraph_plan（段落計画）

---

### Phase 3へループバック（段落再執筆）

**条件**:

- 特定の段落の内容修正が必要
- 段落間のトランジション調整が必要
- コード例の修正が必要

**保持する段落**:

- 修正対象以外の段落は保持

**再執筆する段落**:

- 修正対象の段落のみ

**トランジションの更新**:

- 前後の段落との繋がりを調整

---

### Phase 4へループバック（再レビュー）

**条件**:

- トーンとスタイルの調整のみ必要
- AIっぽさ除去の再実行が必要
- 軽微な読みやすさの改善が必要

**レビュー対象**:

- humanize（AIっぽさ除去）を再実行
- 構造レビューはスキップ可能

**厳格化**:

- より厳しい基準でレビュー

---

## エスカレーション基準

以下の場合、ユーザーに判断を仰ぐ：

1. **2回の自己修正後も`critical`問題が残る**
   - 自己修正の限界を超えている
   - ユーザーの判断が必要

2. **フィードバックが曖昧で解釈できない**
   - 具体的な指示を依頼

3. **技術的正確性に自信がない**
   - ユーザーに検証を依頼

4. **修正が元の意図から逸脱する可能性**
   - ユーザーに確認

## 自己修正

### 判断が困難な場合

- 重要度を保守的に判定（`minor_revision` より `major_revision`）
- ユーザー確認を推奨事項として追加

### 修正範囲が不明確な場合

- 最小限の修正から開始（`minor_revision`）
- 追加の修正が必要なら再度フィードバックループ

## 参照

- **フィードバック処理基準**: `makimono/toranomaki/conditional_instructions/handling_blog_review_feedback.md`
- **ワークフロー全体**: `makimono/toranomaki/procedure/blog_writing_workflow.md`
- **レビュー基準**: `makimono/ryunomaki/guidelines/blog_review_criteria.md`
