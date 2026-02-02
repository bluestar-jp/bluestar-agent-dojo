# Style and Conventions

## Communication
- **言語**: ユーザーへの最終出力は常に**日本語**。思考プロセス（Thought）には英語を使用可能。
- **態度**: 常にプロフェッショナルで、ハルシネーション（嘘）を避け、不明な点は「不明」と正直に伝える。

## Development Rules
- **DRY & KISS**: コードや定義は重複を避け、単純さを保つ。
- **Security**: セキュリティ脆弱性の排除を徹底し、機密情報を外部に出さない。

## Git Conventions
- **コミットメッセージ**: **日本語**で記述する。
- **Prefix**: Conventional Commits準拠（`feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `chore:`）。
- **Co-authoring**: AIによるコミットには必ず以下を末尾に含める：
  `Co-Authored-By: gemini-cli <218195315+gemini-cli@users.noreply.github.com>`

## Directory Conventions
- 新しいカスタムスキルの定義は `skills/` 配下の適切なカテゴリ（龍の巻・虎の巻）に追加する。
- 知識型（知識・背景）は `ryu_no_maki/`、指示型（手順・動作）は `tora_no_maki/` に分類する。
