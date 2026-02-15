---
name: action-composing-paragraph-skill
description: ブログ記事の単一段落を執筆する。テーマ、アウトライン、前後の文脈から段落コンテンツを生成する。
---

# Paragraph Composition Skill

- Purpose: 技術ブログ記事の段落を執筆する
- Scope: 単一段落の構成設計と本文生成

## 入力形式

```json
{
  "paragraph_id": "P1",
  "section": "はじめに",
  "outline": "課題の明示と記事のゴール",
  "key_points": [
    "課題の具体化",
    "記事で解決すること",
    "対象読者"
  ],
  "preceding_content": "<前段落までの内容（前後のコンテキスト）>",
  "following_outline": "<次段落の概要>",
  "estimated_words": 150,
  "paragraph_type": "introduction|explanation|instruction|comparison|conclusion"
}
```

## ワークフロー

### Step 1: 段落構造の設計

`makimono/toranomaki/single_action/blog_paragraph_scaffolding.md` を参照し、段落タイプに応じたテンプレートを選択：

- **introduction**: 問題提起 → 影響 → ゴール
- **explanation**: 定義 → 仕組み → 具体例
- **instruction**: 手順概要 → コード例 → 説明 → 注意点
- **comparison**: 比較観点 → オプションA → オプションB → 推奨
- **conclusion**: 要点 → 達成したこと → 次のステップ

### Step 2: トピックセンテンスの作成

段落の主題を1-2文で明示：

- **パターンA**: 問題提起型（「<問題>が発生する。<影響>。」）
- **パターンB**: 解決策提示型（「<手法>を使うと<結果>。」）
- **パターンC**: 状況説明型（「<技術>は<定義>。」）
- **パターンD**: 比較型（「<技術A>と<技術B>では<観点>が異なる。」）

### Step 3: 根拠・詳細・例の追加

トピックセンテンスを以下で支える：

- **データ**: 測定結果、ベンチマーク、数値
- **コード例**: 具体的な実装コード + 説明
- **具体例**: シナリオ、ユースケース
- **理由**: なぜそうなるのか、どのような仕組みか

### Step 4: トランジションの追加（オプション）

次の段落への繋ぎ：

- **予告型**: 「次に、<次の話題>を見ていく。」
- **因果型**: 「この結果、<次の内容>が必要になる。」
- **対比型**: 「一方、<次の観点>も考慮すべきだ。」
- **なし**: 段落間の繋がりが自明な場合

## ベストプラクティス

### DO（推奨）

✅ トピックセンテンスで段落の主題を明確に
✅ 1段落1アイデアの原則を守る
✅ 具体例やデータで主張を支える
✅ コードブロックの前後に説明を付ける
✅ 能動態を使う
✅ 短い文と長い文を織り交ぜる

### DON'T（避ける）

❌ 前置き宣言（「本段落では〜を説明します」）
❌ 安全クッション（「一般的に」「多くの場合」）
❌ 抽象語の空回り（「これは重要です」）
❌ 同義語の言い換え連打（「シンプルです。簡単です。分かりやすいです。」）
❌ 根拠なしの主張
❌ 太字・括弧・コロンの過剰使用

## 出力形式

```json
{
  "paragraph_id": "P1",
  "content": "段落の本文テキスト（Markdown形式）",
  "word_count": 150,
  "key_points_covered": [
    "課題の具体化",
    "記事で解決すること"
  ],
  "transition_to_next": "次段落への繋ぎ文（あれば）",
  "code_blocks": [
    {
      "language": "typescript",
      "content": "コードの内容",
      "explanation": "コードの説明"
    }
  ]
}
```

## 品質チェックリスト

段落執筆後、以下を確認：

- [ ] トピックセンテンスが明確か
- [ ] 根拠や具体例で主題を支えているか
- [ ] 1段落1アイデアの原則を守っているか
- [ ] 段落の長さが適切か（100-300文字）
- [ ] 前置き宣言や安全クッションがないか
- [ ] 抽象語の空回りがないか
- [ ] コード例に説明が付いているか
- [ ] 次の段落への繋がりが自然か

## 自己修正

### コンテキスト不足

- 前後の段落を再確認
- key_pointsを見直す
- 必要なら簡略化

### 段落が長すぎる（300文字超）

- トピックを2つに分割できないか検討
- 詳細を別段落に移動
- 箇条書きを検討

### トピックが不明確

- トピックセンテンスを先頭に移動
- key_pointsに立ち返る
- 1段落1アイデアを再確認

## 参照

- **段落テンプレート**: `makimono/toranomaki/single_action/blog_paragraph_scaffolding.md`
- **ベストプラクティス**: `makimono/ryunomaki/guidelines/blog_writing_best_practices.md`
- **AIっぽさ除去**: `makimono/ryunomaki/guidelines/blog_humanize_rules.md`
- **具体例**: `references/composition_guidelines.md`（作成予定）
