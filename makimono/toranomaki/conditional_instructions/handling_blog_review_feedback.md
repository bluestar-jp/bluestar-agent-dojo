# レビューフィードバック処理の判断基準

- Purpose: ブログ記事レビュー後のフィードバックを処理し、適切なアクションを決定する
- Scope: OK/NGの判定、フィードバック→修正アクションのマッピング、ループバック条件

## 1. フィードバックの分類

### 1.1 OK（承認）

記事が品質基準を満たし、公開可能な状態。

#### 判定基準

- 構造・読みやすさレビューで`critical`問題がゼロ
- AIっぽさ除去レビューで`high`以上の問題が2件以下
- ユーザーが内容に合意している
- 技術的正確性が確認されている

#### アクション

```json
{
  "decision": "approve",
  "next_phase": "Phase 6: Generate & Publish",
  "action": "記事生成・公開プロセスへ進む"
}
```

---

### 1.2 Minor Revision（軽微な修正）

部分的な修正で対応可能。

#### 判定基準

- `medium`以下の問題のみ
- 修正対象が2-3段落以内
- 構造の変更が不要
- 10分以内で修正可能

#### アクション

```json
{
  "decision": "minor_revision",
  "scope": "targeted",
  "revision_targets": ["P2", "P5"],
  "revision_instructions": [
    {
      "paragraph_id": "P2",
      "issue": "専門用語の説明が不足",
      "action": "用語の定義を1-2文追加"
    },
    {
      "paragraph_id": "P5",
      "issue": "コード例の説明が簡素すぎる",
      "action": "コードブロックの前後に説明を追加"
    }
  ],
  "loop_back_to": "Phase 3 (Execute)",
  "estimated_time": "5-10分"
}
```

---

### 1.3 Major Revision（大幅な修正）

構造的な見直しが必要。

#### 判定基準

- `critical`または`high`問題が3件以上
- 修正対象が4段落以上
- 構造の変更が必要（セクションの追加/削除/順序変更）
- 30分以上の修正時間が見込まれる

#### アクション

```json
{
  "decision": "major_revision",
  "scope": "structural",
  "structural_changes": [
    {
      "type": "reorder_sections",
      "from": ["はじめに", "手順", "前提条件"],
      "to": ["はじめに", "前提条件", "手順"],
      "reason": "前提条件を先に説明すべき"
    },
    {
      "type": "add_section",
      "section": "トラブルシューティング",
      "position": "before まとめ",
      "reason": "よくある問題への対処が不足"
    }
  ],
  "revision_targets": ["P1", "P3", "P4", "P6", "P7"],
  "loop_back_to": "Phase 1 (Plan)",
  "estimated_time": "30-60分"
}
```

---

### 1.4 Reject（却下・再計画）

記事の方向性が根本的に間違っている。

#### 判定基準

- 記事タイプとテーマが不整合
- 対象読者が不明確または不適切
- 技術的に誤った内容が多数
- 構造が全体的に破綻している

#### アクション

```json
{
  "decision": "reject",
  "reason": "記事タイプとテーマが不整合。How-toとして書くべき内容が比較記事になっている",
  "action": "アウトラインから再検討",
  "loop_back_to": "Phase 1 (Plan)",
  "recommendations": [
    "テンプレートをHow-toに変更",
    "比較要素を削除し、実装手順に集中",
    "セクション構成を再設計"
  ]
}
```

---

## 2. フィードバックタイプ別の処理

### 2.1 内容の修正

**フィードバック例**:

- 「段落P3の説明が不十分」
- 「コード例が動作しない」
- 「専門用語の定義が欠けている」

**処理**:

```json
{
  "feedback_type": "content_revision",
  "target": "specific_paragraphs",
  "paragraphs": ["P3"],
  "action": "段落を再執筆",
  "loop_back_to": "Phase 3 (Execute)",
  "preserve": ["P1", "P2", "P4", "P5"]
}
```

---

### 2.2 構造の変更

**フィードバック例**:

- 「セクションの順序が不自然」
- 「まとめが不足している」
- 「前提条件セクションを追加すべき」

**処理**:

```json
{
  "feedback_type": "structural_revision",
  "target": "article_structure",
  "action": "アウトラインを再構築",
  "loop_back_to": "Phase 1 (Plan)",
  "structural_changes": [
    {
      "type": "add_section",
      "section": "前提条件",
      "position": "after はじめに"
    },
    {
      "type": "reorder_sections",
      "from": ["A", "B", "C"],
      "to": ["A", "C", "B"]
    }
  ]
}
```

---

### 2.3 トーンとスタイルの調整

**フィードバック例**:

- 「AIっぽさが残っている」
- 「説明が堅苦しすぎる」
- 「会話的すぎて専門性が欠ける」

**処理**:

```json
{
  "feedback_type": "tone_revision",
  "target": "全段落",
  "action": "AIっぽさ除去レビューを再実行",
  "loop_back_to": "Phase 4 (Verify)",
  "specific_instructions": [
    "前置き宣言を完全に削除",
    "抽象語を具体的な説明に置き換え",
    "文のリズムを不均一にする"
  ]
}
```

---

### 2.4 技術的正確性の修正

**フィードバック例**:

- 「このコードは動作しない」
- 「バージョン情報が古い」
- 「推奨されていない手法を紹介している」

**処理**:

```json
{
  "feedback_type": "technical_correction",
  "target": "specific_paragraphs",
  "paragraphs": ["P4", "P6"],
  "action": "技術内容を検証し再執筆",
  "loop_back_to": "Phase 3 (Execute)",
  "verification_required": [
    "コード例の動作確認",
    "バージョン情報の最新化",
    "公式ドキュメントとの整合性確認"
  ]
}
```

---

## 3. ループバック条件と戦略

### 3.1 Phase 1へループバック（再計画）

**条件**:

- 構造的な変更が必要
- セクションの追加/削除が必要
- 記事タイプの変更が必要

**戦略**:

```json
{
  "loop_strategy": "replanning",
  "preserve": {
    "theme": true,
    "target_audience": true,
    "key_points": ["保持すべきキーポイント"]
  },
  "recreate": {
    "outline": true,
    "section_structure": true,
    "paragraph_plan": true
  }
}
```

---

### 3.2 Phase 3へループバック（段落再執筆）

**条件**:

- 特定の段落の内容修正が必要
- 段落間のトランジション調整が必要
- コード例の修正が必要

**戦略**:

```json
{
  "loop_strategy": "targeted_rewrite",
  "preserve_paragraphs": ["P1", "P2", "P5"],
  "rewrite_paragraphs": ["P3", "P4"],
  "update_transitions": {
    "P2_to_P3": "前段落との繋がりを強化",
    "P4_to_P5": "次段落への流れを自然に"
  }
}
```

---

### 3.3 Phase 4へループバック（再レビュー）

**条件**:

- トーンとスタイルの調整のみ必要
- AIっぽさ除去の再実行が必要
- 軽微な読みやすさの改善が必要

**戦略**:

```json
{
  "loop_strategy": "re_review",
  "review_focus": "humanize",
  "skip_structure_review": true,
  "apply_stricter_criteria": {
    "preface_detection": "厳格化",
    "symbol_threshold": "太字3回以上で警告"
  }
}
```

---

## 4. 修正プランの生成

### 4.1 修正優先度の決定

```json
{
  "priority_mapping": {
    "critical": {
      "severity": "critical",
      "action": "即座に修正（Phase 3へ）",
      "max_defer": 0
    },
    "high": {
      "severity": "high",
      "action": "優先的に修正（Phase 3へ）",
      "max_defer": 1
    },
    "medium": {
      "severity": "medium",
      "action": "次回修正時に対応",
      "max_defer": 2
    },
    "low": {
      "severity": "low",
      "action": "時間があれば対応",
      "max_defer": 999
    }
  }
}
```

### 4.2 修正タスクの順序決定

```json
{
  "task_ordering": [
    {
      "order": 1,
      "task": "構造的な問題の修正",
      "reason": "他の修正の基盤となる"
    },
    {
      "order": 2,
      "task": "技術的正確性の修正",
      "reason": "信頼性の基盤"
    },
    {
      "order": 3,
      "task": "内容の充実化",
      "reason": "品質向上"
    },
    {
      "order": 4,
      "task": "トーンとスタイルの調整",
      "reason": "最後の仕上げ"
    }
  ]
}
```

---

## 5. 自己修正の限界

### 5.1 自己修正可能な範囲

- **表現の調整**: 前置き宣言の削除、抽象語の具体化
- **軽微な追加**: 1-2文の説明追加、トランジション追加
- **記号の削除**: 太字、括弧、コロンの削減

### 5.2 人間判断が必要な範囲

- **技術的判断**: 推奨手法の選択、アーキテクチャの妥当性
- **対象読者の調整**: 初心者向けか上級者向けか
- **記事の方向性**: テーマや目的の根本的な変更

### 5.3 エスカレーション基準

```json
{
  "escalation_triggers": [
    {
      "condition": "2回の自己修正後も`critical`問題が残る",
      "action": "ユーザーに判断を仰ぐ"
    },
    {
      "condition": "フィードバックが曖昧で解釈できない",
      "action": "明確化を依頼"
    },
    {
      "condition": "技術的正確性に自信がない",
      "action": "ユーザーに検証を依頼"
    },
    {
      "condition": "修正が元の意図から逸脱する可能性",
      "action": "ユーザーに確認"
    }
  ]
}
```

---

## 6. 出力形式

### 6.1 修正プラン（Minor Revision）

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
    "loop_back_to": "Phase 3 (Execute)"
  }
}
```

### 6.2 修正プラン（Major Revision）

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

## 7. 関連リソース

### 竜の巻（知識）

- `makimono/ryunomaki/guidelines/blog_review_criteria.md` - レビュー基準
- `makimono/ryunomaki/guidelines/blog_humanize_rules.md` - AIっぽさ除去ルール

### 虎の巻（手順）

- `makimono/toranomaki/procedure/blog_writing_workflow.md` - 全体ワークフロー

### スキル

- `skills/action-revising-article-skill/` - この判断基準を実装するスキル
