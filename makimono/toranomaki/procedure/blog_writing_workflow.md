# ブログ執筆ワークフロー手順

- Purpose: 技術ブログ記事執筆の全体ワークフロー（PAVE: Plan → Agree → Execute → Verify）
- Scope: テーマ分析からレビュー、公開までの全フェーズ

## ワークフロー概要

```text
Phase 1: Plan (計画)
  ├── テーマ分析
  ├── テンプレート選択
  └── アウトライン構造化

Phase 2: Agree (合意)
  └── ユーザー確認・調整

Phase 3: Execute (実行)
  └── 段落執筆（sequential）

Phase 4: Verify (検証)
  ├── 並列レビュー（2系統）
  │   ├── 構造・読みやすさレビュー
  │   └── AIっぽさ除去レビュー
  ├── レビュー結果統合
  ├── 自己修正（最大2ラウンド）
  └── 人間レビュー

Phase 5: Generate & Publish (生成・公開)
  ├── Markdown記事生成
  └── GitHubリポジトリ公開
```

---

## Phase 1: Plan - テーマ分析とアウトライン構造化

### 入力

- ユーザー提供のテーマ
- 段落構成案（段落数と各段落の概要）
- 対象読者（オプション）

### 実行手順

#### Step 1.1: テーマ分析

```json
{
  "theme": "ユーザー提供のテーマ",
  "target_audience": "初心者 | 中級者 | 上級者",
  "article_goal": "記事で達成したいこと"
}
```

#### Step 1.2: テンプレート選択

`makimono/ryunomaki/specs/blog_article_output_format.md`を参照し、テーマに最適なテンプレートを選択：

- **How-to**: 特定の実装手順や問題解決
- **Deep Dive**: 技術の内部仕組みや詳細分析
- **比較**: 複数技術の比較検討
- **振り返り/事例**: プロジェクト実践での学び
- **コンセプト解説**: 抽象的な概念の説明

#### Step 1.3: アウトライン構造化

```json
{
  "theme": "記事テーマ",
  "article_type": "how-to",
  "template": {
    "sections": [
      {"heading": "はじめに", "level": 2},
      {"heading": "前提条件", "level": 2},
      {"heading": "手順", "level": 2, "subsections": ["Step 1", "Step 2"]}
    ]
  },
  "paragraphs": [
    {
      "id": "P1",
      "section": "はじめに",
      "outline": "課題の明示と記事のゴール",
      "key_points": ["課題の具体化", "記事で解決すること", "対象読者"],
      "estimated_words": 150
    },
    {
      "id": "P2",
      "section": "前提条件",
      "outline": "必要な知識と環境",
      "key_points": ["前提知識", "ツールバージョン", "環境構築"],
      "estimated_words": 100
    }
  ],
  "composition_plan": [
    {"paragraph_id": "P1", "dependencies": []},
    {"paragraph_id": "P2", "dependencies": ["P1"]}
  ]
}
```

### 出力

構造化されたアウトラインと実行計画（JSON形式）

### チェックポイント

- [ ] 記事タイプとテーマが整合している
- [ ] 各段落の役割が明確
- [ ] 段落間の依存関係が適切
- [ ] 全体のストーリーラインが一貫している

---

## Phase 2: Agree - ユーザー確認

### 入力

Phase 1の出力（アウトライン）

### 実行手順

#### Step 2.1: アウトラインの提示

ユーザーに以下を提示：

- 選択したテンプレートと理由
- セクション構成
- 各段落の概要とキーポイント
- 推定文字数

#### Step 2.2: フィードバック収集

ユーザーからの調整要望を確認：

- セクションの追加/削除/順序変更
- 段落の追加/削除/内容調整
- キーポイントの修正

#### Step 2.3: アウトライン確定

フィードバックを反映し、最終アウトラインを確定

### 出力

確定したアウトライン（JSON形式）

### チェックポイント

- [ ] ユーザーが構成に合意している
- [ ] 必要な調整を全て反映している
- [ ] 実行可能な状態になっている

---

## Phase 3: Execute - 段落執筆

### 入力

Phase 2で確定したアウトライン

### 実行手順

#### Step 3.1: 段落の順次執筆

各段落を**sequential**に執筆（前段落のコンテキストを次に渡す）：

1. `deshi-blog-composer` + `action-composing-paragraph-skill` を使用
2. 各段落の入力：

   ```json
   {
     "paragraph_id": "P1",
     "section": "はじめに",
     "outline": "課題の明示と記事のゴール",
     "key_points": ["課題の具体化", "記事で解決すること"],
     "preceding_content": "<前段落までの内容>",
     "following_outline": "<次段落の概要>"
   }
   ```

3. 各段落の出力：

   ```json
   {
     "paragraph_id": "P1",
     "content": "本文テキスト",
     "word_count": 150,
     "key_points_covered": ["課題の具体化", "記事で解決すること"],
     "transition_to_next": "次段落への繋ぎ文"
   }
   ```

#### Step 3.2: ドラフト記事の組み立て

全段落を統合し、ドラフト記事を生成：

```json
{
  "draft_article": {
    "frontmatter": {
      "title": "記事タイトル",
      "emoji": "📝",
      "type": "tech",
      "topics": ["react", "typescript"],
      "published": false
    },
    "content": "<全段落を統合したMarkdownテキスト>",
    "word_count": 1500,
    "sections": [
      {"heading": "はじめに", "paragraphs": ["P1"]},
      {"heading": "前提条件", "paragraphs": ["P2"]}
    ]
  }
}
```

### 出力

ドラフト記事（Markdown形式）

### チェックポイント

- [ ] 全段落が執筆されている
- [ ] 段落間のトランジションが自然
- [ ] 各段落のキーポイントがカバーされている
- [ ] コードブロックが適切にフォーマットされている

---

## Phase 4: Verify - 並列セルフレビュー

### 入力

Phase 3のドラフト記事

### 実行手順

#### Step 4.1: 並列レビューの実行（2系統）

`Task`ツールの`run_in_background: true`で並列実行：

#### レビュー系統A: 構造・読みやすさレビュー

- エージェント: `deshi-blog-reviewer`
- スキル: `action-reviewing-article-skill`
- 観点: 文章の流れ、段落間の繋がり、読みやすさ
- 出力:

  ```json
  {
    "review_type": "structure_readability",
    "overall_quality": "good | needs_revision",
    "findings": [
      {
        "severity": "high|medium|low",
        "category": "structure|flow|paragraph|sentence|terminology|visual|completeness",
        "paragraph_id": "P2",
        "issue": "段落間のトランジションが唐突",
        "suggestion": "P1の末尾に繋ぎ文を追加、またはP2の冒頭を調整"
      }
    ]
  }
  ```

#### レビュー系統B: AIっぽさ除去レビュー

- エージェント: `deshi-blog-humanizer`
- スキル: `action-humanizing-article-skill`
- 観点: テンプレ感、記号過多、過剰な丁寧さ、前置き宣言、抽象語
- 出力:

  ```json
  {
    "review_type": "humanize",
    "overall_quality": "natural | needs_humanizing",
    "findings": [
      {
        "severity": "high|medium|low",
        "category": "preface|cushion|abstract|repetition|symbol|rhythm|tone",
        "paragraph_id": "P1",
        "original": "本記事では、Reactのパフォーマンス最適化について解説します。",
        "rewritten": "Reactアプリケーションが遅い。ページの読み込みに3秒かかる。",
        "rule_violated": "ルール1.1: 前置き宣言の禁止",
        "explanation": "前置き宣言を削除し、問題提起から直接始める"
      }
    ],
    "rewritten_full_text": "書き換え後の全文（段落構成維持、±20%以内）"
  }
  ```

#### Step 4.2: レビュー結果の統合

両系統の結果を統合：

```json
{
  "combined_review": {
    "structure_review": {
      "quality": "good | needs_revision",
      "critical_issues": 0,
      "high_issues": 2,
      "medium_issues": 5,
      "low_issues": 3
    },
    "humanize_review": {
      "quality": "natural | needs_humanizing",
      "critical_issues": 0,
      "high_issues": 3,
      "medium_issues": 4,
      "low_issues": 2
    },
    "overall_status": "ok | needs_minor_revision | needs_major_revision",
    "revision_plan": [
      {
        "priority": "high",
        "action": "humanizer の書き換え提案を適用（P1, P3）",
        "affected_paragraphs": ["P1", "P3"]
      },
      {
        "priority": "high",
        "action": "段落間トランジションを追加（P2→P3）",
        "affected_paragraphs": ["P2", "P3"]
      }
    ]
  }
}
```

#### Step 4.3: 自己修正（最大2ラウンド）

統合レビュー結果に基づき自己修正：

1. **高優先度の問題から修正**
   - humanizerの書き換え提案を適用
   - 構造的な問題（トランジション、段落順序等）を修正

2. **修正後の検証**
   - 技術的正確性が維持されているか
   - 文字数が±20%以内か
   - 段落構成が維持されているか

3. **再レビュー（必要に応じて）**
   - 修正後も問題が残る場合、最大2ラウンドまで再実行

#### Step 4.4: 人間レビューへの引き渡し

統合後のドラフトと両系統のレビュー結果をユーザーに提示：

```markdown
# レビュー結果

## 構造・読みやすさレビュー
- 全体品質: good
- 問題点: 2件（high）、5件（medium）

## AIっぽさ除去レビュー
- 全体品質: needs_humanizing
- 問題点: 3件（high）、4件（medium）

## 自己修正実施内容
1. 前置き宣言を削除し、問題提起から開始（P1）
2. 段落間トランジションを追加（P2→P3）
3. 抽象語を具体的な説明に置き換え（P4, P5）

## ドラフト記事
<修正後のMarkdown>
```

### 出力

- 修正後のドラフト記事
- レビュー結果サマリー
- 人間レビューへの指示

### チェックポイント

- [ ] 両系統のレビューが完了している
- [ ] レビュー結果が適切に統合されている
- [ ] 高優先度の問題が自己修正されている
- [ ] 技術的正確性が維持されている

---

## Phase 5: Human Review - 人間レビュー

### 入力

Phase 4の修正後ドラフトとレビュー結果

### 実行手順

#### Step 5.1: ドラフトの提示

ユーザーに以下を提示：

- 修正後のドラフト記事
- 両系統のレビュー結果
- 自己修正内容

#### Step 5.2: フィードバック処理

`action-revising-article-skill` を使用してフィードバックを処理：

- **OK**: Phase 6へ進む
- **NG**: 修正プラン策定

  ```json
  {
    "feedback_type": "revision_required",
    "revision_targets": ["P2", "P5"],
    "revision_instructions": [
      {
        "paragraph_id": "P2",
        "issue": "コード例の説明が不足",
        "action": "コードの前後に説明を追加"
      }
    ],
    "loop_back_to": "Phase 3 (Execute)",
    "scope": "targeted"
  }
  ```

#### Step 5.3: 修正ループ（NGの場合）

- 修正対象段落のみを再執筆（Phase 3へループバック）
- 再レビュー実施（Phase 4へ）
- 人間レビュー再実施

### 出力

- 承認済みドラフト（OKの場合）
- 修正プラン（NGの場合）

### チェックポイント

- [ ] ユーザーが内容を確認している
- [ ] 必要な修正が明確になっている
- [ ] 修正範囲が適切に特定されている

---

## Phase 6: Generate & Publish - 記事生成・公開

### 入力

Phase 5で承認されたドラフト

### 実行手順

#### Step 6.1: Markdown記事生成

`action-generating-article-skill` を使用：

1. Zenn frontmatterの生成

   ```yaml
   ---
   title: "記事タイトル"
   emoji: "📝"
   type: "tech"
   topics: ["react", "typescript"]
   published: false
   ---
   ```

2. 本文のフォーマット
   - 見出し階層の調整
   - コードブロックの言語指定確認
   - 画像パスの検証

3. ファイル名の生成

   ```text
   articles/2024-03-15-nextjs-ogp-generation.md
   ```

#### Step 6.2: GitHubリポジトリ公開

`action-publishing-article-skill` を使用：

1. ファイル配置

   ```bash
   cp <generated-file> <repo>/articles/
   ```

2. Git操作

   ```bash
   git add articles/<filename>.md
   git commit -m "feat: Add blog post - <title>

   Co-authored-by: Claude Sonnet 4.5 <noreply@anthropic.com>"
   git push origin main
   ```

3. Zenn連携確認
   - Zennダッシュボードで記事が表示されるか確認
   - 下書き状態で正しく反映されているか確認

### 出力

- 生成されたMarkdownファイル
- GitHubリポジトリURL
- Zenn記事プレビューURL

### チェックポイント

- [ ] Zenn frontmatterが仕様に準拠している
- [ ] ファイル名が規則に従っている
- [ ] GitHubに正常にプッシュされている
- [ ] Zennで記事が確認できる

---

## エラーハンドリング

### 段落執筆失敗（Phase 3）

**症状**: 特定の段落が生成できない

**対応**:

1. アウトラインを簡略化して再試行
2. 前段落のコンテキストを調整
3. 最大2回リトライ後、ユーザーに報告

### レビュー失敗（Phase 4）

**症状**: レビュー系統の一方が失敗

**対応**:

1. 成功した系統の結果を保持
2. 失敗した系統を再実行（最大2回）
3. 片方のみでも人間レビューへ進む

### 自己修正失敗（Phase 4）

**症状**: 修正後も品質基準を満たさない

**対応**:

1. 修正前のドラフトを保持
2. レビュー結果を明示して人間レビューへ
3. ユーザー判断を仰ぐ

### 公開失敗（Phase 6）

**症状**: GitHubプッシュやZenn連携が失敗

**対応**:

1. ローカルにMarkdownファイルを保存
2. エラー詳細をユーザーに報告
3. 手動公開の手順を提示

---

## 関連リソース

### 竜の巻（知識）

- `makimono/ryunomaki/guidelines/blog_writing_best_practices.md`
- `makimono/ryunomaki/guidelines/blog_review_criteria.md`
- `makimono/ryunomaki/guidelines/blog_humanize_rules.md`
- `makimono/ryunomaki/specs/blog_article_output_format.md`

### 虎の巻（手順）

- `makimono/toranomaki/conditional_instructions/handling_blog_review_feedback.md`
- `makimono/toranomaki/single_action/blog_paragraph_scaffolding.md`

### スキル

- `skills/action-composing-paragraph-skill/`
- `skills/action-reviewing-article-skill/`
- `skills/action-humanizing-article-skill/`
- `skills/action-generating-article-skill/`
- `skills/action-publishing-article-skill/`
- `skills/action-revising-article-skill/`

### エージェント

- `agents/deshi-blog-composer.md`
- `agents/deshi-blog-reviewer.md`
- `agents/deshi-blog-humanizer.md`
