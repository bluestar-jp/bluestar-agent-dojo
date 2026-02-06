# Task Completion Guidelines

作業を完了する際は、以下のステップを必ず踏むこと。

1. **環境の変更をローカルに適用**:
   `container-use checkout <env_id>` を実行し、作業環境の変更を現在のディレクトリに反映させる。
2. **検証**:
   - `python3 scripts/verify-best-practices.py` で構成がベストプラクティスに準拠しているか確認。
   - `sh scripts/validate-plugin.sh` でプラグインの整合性を確認。
   - `sh scripts/lint-markdown.sh` でMarkdown形式を確認。
3. **メモリの同期**:
   ディレクトリ構造、規約、新機能の追加があった場合、`write_memory` を使用して Serena の記憶を更新する。
4. **コミット & プッシュ**:
   - 規約（Conventional Commits）に準拠した日本語メッセージを作成。
   - 適切な `Co-authored-by` トレーラーを含める。
   - `git push origin main` でリモートに反映。
5. **完了報告**:
   ユーザーに作業完了を伝え、適用・確認のためのコマンド（`log`, `checkout`）を提示する。
