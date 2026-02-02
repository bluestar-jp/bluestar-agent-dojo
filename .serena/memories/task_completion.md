# Task Completion Guidelines

作業を完了する際は、以下のステップを必ず踏むこと。

1. **環境の変更をローカルに適用**:
   `container-use checkout <env_id>` を実行し、作業環境の変更を現在のディレクトリに反映させる。
2. **メモリの同期**:
   ディレクトリ構造や規約に変更があった場合、`write_memory` を使用して Serena の記憶を更新する。
3. **コミット & プッシュ**:
   - 規約（Conventional Commits）に準拠したメッセージを作成。
   - `Co-Authored-By: gemini-cli <218195315+gemini-cli@users.noreply.github.com>` を含める。
   - `git push origin main` でリモートに反映。
4. **完了報告**:
   ユーザーに作業完了を伝え、適用・確認のためのコマンド（`log`, `checkout`）を提示する。
