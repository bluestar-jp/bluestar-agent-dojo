#!/usr/bin/env python3
"""
外部定義ファイルを取得するスクリプト

Usage:
    fetch-definition.py --source <URL or path> --type <skill|agent> --output-dir <path>
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse


class DefinitionFetcher:
    """外部定義ファイルを取得するクラス"""

    # セキュリティ設定
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_SCHEMES = ['http', 'https']
    BLOCKED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '::1']
    SUSPICIOUS_PATTERNS = [
        r'\.\./|\.\.\\',  # パストラバーサル
        r'[;&|`$]',       # コマンドインジェクション
    ]

    def __init__(self, source: str, resource_type: str, output_dir: str):
        self.source = source
        self.resource_type = resource_type
        self.output_dir = Path(output_dir)
        self.source_type = self._detect_source_type()

        # セキュリティ検証
        self._validate_security()

    def _validate_security(self):
        """セキュリティ検証を実行"""
        # URL/パスの検証
        if self.source_type in ['http', 'archive', 'git']:
            self._validate_url(self.source)

        # パストラバーサル対策
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, self.source):
                raise ValueError(f"[セキュリティ] 不正なパターンが検出されました: {self.source}")

        # 出力ディレクトリの検証
        try:
            resolved_output = self.output_dir.resolve()
            # /tmpまたはユーザーディレクトリ配下であることを確認
            if not (str(resolved_output).startswith('/tmp') or
                    str(resolved_output).startswith(str(Path.home()))):
                print(f"[警告] 出力ディレクトリが想定外の場所です: {resolved_output}", file=sys.stderr)
        except Exception as e:
            raise ValueError(f"[セキュリティ] 出力ディレクトリの検証に失敗: {e}")

    def _validate_url(self, url: str):
        """URLの安全性を検証"""
        try:
            parsed = urlparse(url)

            # スキームの検証
            if parsed.scheme and parsed.scheme not in self.ALLOWED_SCHEMES:
                raise ValueError(f"[セキュリティ] 許可されていないスキーム: {parsed.scheme}")

            # ホスト名の検証
            if parsed.hostname:
                # localhostやプライベートIPのブロック
                if parsed.hostname in self.BLOCKED_HOSTS:
                    raise ValueError(f"[セキュリティ] ブロックされたホスト: {parsed.hostname}")

                # プライベートIPレンジのチェック（簡易版）
                if parsed.hostname.startswith('10.') or \
                   parsed.hostname.startswith('172.') or \
                   parsed.hostname.startswith('192.168.'):
                    raise ValueError(f"[セキュリティ] プライベートIPアドレスは許可されていません: {parsed.hostname}")

            print(f"[情報] URL検証成功: {url}")

        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"[セキュリティ] URL検証エラー: {e}")

    def _check_file_size(self, file_path: Path):
        """ファイルサイズを検証"""
        if file_path.exists() and file_path.is_file():
            size = file_path.stat().st_size
            if size > self.MAX_FILE_SIZE:
                raise ValueError(
                    f"[セキュリティ] ファイルサイズが制限を超えています: "
                    f"{size / 1024 / 1024:.2f}MB > {self.MAX_FILE_SIZE / 1024 / 1024:.2f}MB"
                )

    def _sanitize_filename(self, filename: str) -> str:
        """ファイル名をサニタイズ"""
        # パストラバーサル対策
        filename = os.path.basename(filename)

        # 危険な文字を除去
        filename = re.sub(r'[^\w\s\-\.]', '_', filename)

        # 空の場合はデフォルト名
        if not filename or filename == '.':
            filename = 'downloaded_file'

        return filename

    def _detect_source_type(self) -> str:
        """取得元のタイプを自動判定"""
        source = self.source

        if 'github.com' in source:
            return 'github'
        elif 'gitlab.com' in source or 'gitlab' in source:
            return 'gitlab'
        elif 'gist.github.com' in source:
            return 'gist'
        elif 'huggingface.co' in source:
            return 'huggingface'
        elif source.endswith('.git'):
            return 'git'
        elif source.startswith('http://') or source.startswith('https://'):
            parsed = urlparse(source)
            if parsed.path.endswith(('.zip', '.tar.gz', '.tar.bz2')):
                return 'archive'
            else:
                return 'http'
        elif source.startswith('npm:'):
            return 'npm'
        elif source.startswith('pypi:'):
            return 'pypi'
        elif source.startswith('/') or source.startswith('~'):
            return 'local'
        else:
            return 'unknown'

    def fetch(self) -> Dict:
        """取得を実行"""
        print(f"[情報] 取得元タイプを検出: {self.source_type}")
        print(f"[情報] 取得元: {self.source}")

        # 出力ディレクトリを作成
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # タイプ別に取得
        if self.source_type == 'github':
            return self._fetch_github()
        elif self.source_type == 'gist':
            return self._fetch_gist()
        elif self.source_type == 'git':
            return self._fetch_git()
        elif self.source_type == 'http':
            return self._fetch_http()
        elif self.source_type == 'archive':
            return self._fetch_archive()
        elif self.source_type == 'local':
            return self._fetch_local()
        else:
            raise ValueError(f"[エラー] サポートされていない取得元タイプ: {self.source_type}")

    def _fetch_github(self) -> Dict:
        """GitHub リポジトリから取得"""
        # URLからowner/repoを抽出
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)(?:/tree/[^/]+/(.+))?', self.source)
        if not match:
            raise ValueError(f"[エラー] 不正なGitHub URL: {self.source}")

        owner, repo, path = match.groups()
        repo = repo.replace('.git', '')

        # gh CLIで取得
        try:
            # リポジトリ情報を取得
            result = subprocess.run(
                ['gh', 'repo', 'view', f'{owner}/{repo}', '--json', 'description,topics,licenseInfo,url'],
                capture_output=True,
                text=True,
                check=True
            )
            repo_info = json.loads(result.stdout)

            # 特定のパスがある場合はそのファイル/ディレクトリを取得
            if path:
                self._fetch_github_path(owner, repo, path)
            else:
                # リポジトリ全体をクローン
                subprocess.run(
                    ['git', 'clone', '--depth', '1', self.source, str(self.output_dir / 'repo')],
                    check=True
                )

            return {
                'source_type': 'github',
                'metadata': repo_info,
                'files': self._list_files(self.output_dir)
            }

        except subprocess.CalledProcessError as e:
            print(f"[エラー] GitHubからの取得に失敗: {e.stderr}", file=sys.stderr)
            raise

    def _fetch_github_path(self, owner: str, repo: str, path: str):
        """GitHub の特定パスを取得"""
        try:
            result = subprocess.run(
                ['gh', 'api', f'repos/{owner}/{repo}/contents/{path}'],
                capture_output=True,
                text=True,
                check=True
            )
            content_info = json.loads(result.stdout)

            if isinstance(content_info, dict):
                # 単一ファイル
                self._download_github_file(content_info, self.output_dir)
            elif isinstance(content_info, list):
                # ディレクトリ
                for item in content_info:
                    if item['type'] == 'file':
                        self._download_github_file(item, self.output_dir)
                    elif item['type'] == 'dir':
                        # 再帰的に取得
                        safe_name = self._sanitize_filename(item['name'])
                        subdir = self.output_dir / safe_name
                        subdir.mkdir(exist_ok=True)
                        self._fetch_github_path(owner, repo, item['path'])

        except subprocess.CalledProcessError as e:
            print(f"[エラー] GitHubパスの取得に失敗: {e.stderr}", file=sys.stderr)
            raise

    def _download_github_file(self, file_info: Dict, output_dir: Path):
        """GitHubのファイルをダウンロード"""
        file_name = self._sanitize_filename(file_info['name'])
        download_url = file_info.get('download_url')
        file_size = file_info.get('size', 0)

        # ファイルサイズチェック
        if file_size > self.MAX_FILE_SIZE:
            print(f"[警告] ファイルサイズが大きすぎるためスキップ: {file_name} ({file_size / 1024 / 1024:.2f}MB)", file=sys.stderr)
            return

        if download_url:
            output_path = output_dir / file_name
            subprocess.run(
                ['curl', '-L', '-o', str(output_path), download_url],
                check=True
            )
            # ダウンロード後のサイズ検証
            self._check_file_size(output_path)

    def _fetch_gist(self) -> Dict:
        """Gist から取得"""
        # URLからgist IDを抽出
        match = re.search(r'gist\.github\.com/[^/]+/([a-f0-9]+)', self.source)
        if not match:
            raise ValueError(f"[エラー] 不正なGist URL: {self.source}")

        gist_id = match.group(1)

        try:
            # gh CLIでGistを取得
            result = subprocess.run(
                ['gh', 'gist', 'view', gist_id],
                capture_output=True,
                text=True,
                check=True
            )

            # Gistの内容を保存
            gist_file = self.output_dir / 'gist.md'
            gist_file.write_text(result.stdout)

            # ファイルサイズチェック
            self._check_file_size(gist_file)

            return {
                'source_type': 'gist',
                'metadata': {'gist_id': gist_id},
                'files': [str(gist_file)]
            }

        except subprocess.CalledProcessError as e:
            print(f"[エラー] Gistの取得に失敗: {e.stderr}", file=sys.stderr)
            raise

    def _fetch_git(self) -> Dict:
        """Git リポジトリから取得"""
        try:
            subprocess.run(
                ['git', 'clone', '--depth', '1', self.source, str(self.output_dir / 'repo')],
                check=True
            )

            return {
                'source_type': 'git',
                'metadata': {'git_url': self.source},
                'files': self._list_files(self.output_dir)
            }

        except subprocess.CalledProcessError as e:
            print(f"[エラー] Gitリポジトリのクローンに失敗: {e}", file=sys.stderr)
            raise

    def _fetch_http(self) -> Dict:
        """HTTP(S) URLから取得"""
        try:
            # ファイル名を取得してサニタイズ
            parsed = urlparse(self.source)
            filename = Path(parsed.path).name or 'downloaded_file.md'
            filename = self._sanitize_filename(filename)

            output_file = self.output_dir / filename

            # curlでダウンロード（ファイルサイズ制限付き）
            subprocess.run(
                ['curl', '-L', '--max-filesize', str(self.MAX_FILE_SIZE),
                 '-o', str(output_file), self.source],
                check=True
            )

            # ダウンロード後のサイズ検証
            self._check_file_size(output_file)

            return {
                'source_type': 'http',
                'metadata': {'url': self.source},
                'files': [str(output_file)]
            }

        except subprocess.CalledProcessError as e:
            print(f"[エラー] HTTP(S)からのダウンロードに失敗: {e}", file=sys.stderr)
            raise

    def _fetch_archive(self) -> Dict:
        """アーカイブファイルから取得"""
        tmp_path = None
        try:
            # 一時ファイルにダウンロード
            with tempfile.NamedTemporaryFile(delete=False, suffix='.archive') as tmp:
                tmp_path = tmp.name
                subprocess.run(
                    ['curl', '-L', '--max-filesize', str(self.MAX_FILE_SIZE),
                     '-o', tmp.name, self.source],
                    check=True
                )

                # ダウンロードしたファイルのサイズチェック
                self._check_file_size(Path(tmp.name))

                # 拡張子に応じて展開
                if self.source.endswith('.zip'):
                    subprocess.run(['unzip', '-q', tmp.name, '-d', str(self.output_dir)], check=True)
                elif self.source.endswith('.tar.gz') or self.source.endswith('.tgz'):
                    subprocess.run(['tar', 'xzf', tmp.name, '-C', str(self.output_dir)], check=True)
                elif self.source.endswith('.tar.bz2'):
                    subprocess.run(['tar', 'xjf', tmp.name, '-C', str(self.output_dir)], check=True)

            return {
                'source_type': 'archive',
                'metadata': {'archive_url': self.source},
                'files': self._list_files(self.output_dir)
            }

        except subprocess.CalledProcessError as e:
            print(f"[エラー] アーカイブの展開に失敗: {e}", file=sys.stderr)
            raise
        finally:
            # 一時ファイルのクリーンアップ
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    def _fetch_local(self) -> Dict:
        """ローカルファイルシステムから取得"""
        source_path = Path(self.source).expanduser().resolve()

        # パストラバーサル対策: 絶対パスに解決してから検証
        if not source_path.exists():
            raise FileNotFoundError(f"[エラー] 取得元が見つかりません: {self.source}")

        # システムディレクトリへのアクセスを制限
        sensitive_paths = ['/etc', '/sys', '/proc', '/dev', '/boot', '/root']
        for sensitive in sensitive_paths:
            if str(source_path).startswith(sensitive):
                raise ValueError(f"[セキュリティ] システムディレクトリへのアクセスは許可されていません: {source_path}")

        if source_path.is_file():
            # ファイルサイズチェック
            self._check_file_size(source_path)

            # 単一ファイル
            safe_name = self._sanitize_filename(source_path.name)
            dest_path = self.output_dir / safe_name
            shutil.copy2(source_path, dest_path)
            files = [str(dest_path.relative_to(self.output_dir))]
        elif source_path.is_dir():
            # ディレクトリ
            safe_name = self._sanitize_filename(source_path.name)
            dest_path = self.output_dir / safe_name
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
            files = self._list_files(self.output_dir)
        else:
            raise ValueError(f"[エラー] 不正な取得元: {self.source}")

        return {
            'source_type': 'local',
            'metadata': {'local_path': str(source_path)},
            'files': files
        }

    def _list_files(self, directory: Path) -> List[str]:
        """ディレクトリ内のファイル一覧を取得"""
        files = []
        for item in directory.rglob('*'):
            if item.is_file():
                files.append(str(item.relative_to(directory)))
        return files


def main():
    parser = argparse.ArgumentParser(description='外部のスキル/エージェント定義を取得')
    parser.add_argument('--source', required=True, help='取得元のURLまたはパス')
    parser.add_argument('--type', required=True, choices=['skill', 'agent'], help='リソースタイプ')
    parser.add_argument('--output-dir', required=True, help='出力ディレクトリ')

    args = parser.parse_args()

    try:
        fetcher = DefinitionFetcher(args.source, args.type, args.output_dir)
        result = fetcher.fetch()

        print(f"\n[成功] {len(result['files'])}個のファイルを取得しました")
        print(f"[情報] 出力ディレクトリ: {args.output_dir}")

        # 結果をJSONで保存
        result_file = Path(args.output_dir) / 'fetch_result.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"[情報] 取得結果を保存: {result_file}")

    except Exception as e:
        print(f"[エラー] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
