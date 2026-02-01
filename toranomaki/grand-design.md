# 道場全体設計図 (Grand Design)

## 思想：段階的開示 (Progressive Disclosure)
複雑なタスクを解決する際、最初から全てのエージェントを呼び出すのではなく、**「司令塔（師範）」から「専門家（弟子）」へ**とコンテキストを引き継ぎながら詳細化していくアーキテクチャを採用する。

## エージェント連携フロー

### 1. 開発フロー
```mermaid
graph TD
    User[ユーザー] -->|要件・相談| TechLead[テックリード師範]
    TechLead -->|技術方針・仕様書| FEC[フロントエンド弟子]
    TechLead -->|技術方針・仕様書| BEC[バックエンド弟子]
    FEC -->|コード| Review[コードレビュー弟子]
    BEC -->|コード| Review
    Review -->|承認| Repo[リポジトリ]
```

### 2. 広報フロー
```mermaid
graph TD
    User[ユーザー] -->|企画・ネタ| Editor[編集長師範]
    Editor -->|構成案| Writer[執筆弟子]
    Writer -->|原稿| Reviewer[校正弟子]
    Reviewer -->|OK| SNS[SNSマーケター弟子]
    SNS -->|拡散| Public[社会]
```

## ディレクトリ構造の意図
- **toranomaki/**: プロジェクト全体の指針・完成されたドキュメント。
- **zatsunomaki/**: 合意形成前の壁打ちメモや思考の断片を置くワークスペース（雑の巻）。
- **shihan/**: 変更頻度が低く、高い信頼性が求められるコア定義。
- **deshi/**: 開発中や実験的な定義。`shihan` と同じ構成を持ち、昇格を待つプロンプトを管理。
- **menkyokaiden/**: これら自然言語の定義を、Gemini CLIやCursorなどのツール設定ファイル（JSON/YAML等）に変換した結果。
