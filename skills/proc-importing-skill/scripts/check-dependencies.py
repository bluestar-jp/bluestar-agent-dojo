#!/usr/bin/env python3
"""
依存関係を確認し、未インストールのツールをチェックする

Usage:
    check-dependencies.py --path <resource_path>
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set


class DependencyChecker:
    """依存関係チェッククラス"""

    def __init__(self, path: str):
        self.path = Path(path)
        self.dependencies = {
            'cli_tools': set(),
            'python_packages': set(),
            'npm_packages': set(),
            'other': set()
        }

    def check(self) -> Dict:
        """依存関係をチェック"""
        print(f"[INFO] Checking dependencies for: {self.path}")

        # 依存関係を抽出
        self._extract_dependencies()

        # インストール状況を確認
        cli_status = self._check_cli_tools()
        python_status = self._check_python_packages()
        npm_status = self._check_npm_packages()

        result = {
            'path': str(self.path),
            'dependencies': {
                'cli_tools': list(self.dependencies['cli_tools']),
                'python_packages': list(self.dependencies['python_packages']),
                'npm_packages': list(self.dependencies['npm_packages']),
                'other': list(self.dependencies['other'])
            },
            'status': {
                'cli_tools': cli_status,
                'python_packages': python_status,
                'npm_packages': npm_status
            },
            'all_satisfied': self._check_all_satisfied(cli_status, python_status, npm_status)
        }

        # 結果を表示
        self._print_results(result)

        return result

    def _extract_dependencies(self):
        """依存関係を抽出"""
        # SKILL.md または AGENT.md から抽出
        main_files = ['SKILL.md', 'AGENT.md', 'README.md']

        for filename in main_files:
            file_path = self.path / filename
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                self._parse_dependency_section(content)
                self._parse_code_blocks(content)

        # スクリプトファイルから抽出
        script_dirs = ['scripts', 'bin', 'tools', 'verification']
        for dir_name in script_dirs:
            dir_path = self.path / dir_name
            if dir_path.exists():
                self._scan_scripts(dir_path)

    def _parse_dependency_section(self, content: str):
        """依存関係セクションを解析"""
        # 依存関係セクションを探す
        dep_section = re.search(
            r'##\s+(?:依存関係|Dependencies)(.+?)(?=##|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if dep_section:
            dep_text = dep_section.group(1)

            # CLIツール
            cli_tools = ['gh', 'git', 'jq', 'curl', 'wget', 'docker', 'kubectl']
            for tool in cli_tools:
                if re.search(rf'\b{tool}\b', dep_text, re.IGNORECASE):
                    self.dependencies['cli_tools'].add(tool)

            # Pythonパッケージ
            python_pkgs = re.findall(r'`([\w-]+)`', dep_text)
            for pkg in python_pkgs:
                if not pkg in cli_tools:
                    self.dependencies['python_packages'].add(pkg)

    def _parse_code_blocks(self, content: str):
        """コードブロックを解析"""
        # Bashコードブロック
        bash_blocks = re.findall(r'```(?:bash|sh)\n(.+?)```', content, re.DOTALL)
        for block in bash_blocks:
            self._extract_cli_tools(block)

        # Pythonコードブロック
        python_blocks = re.findall(r'```python\n(.+?)```', content, re.DOTALL)
        for block in python_blocks:
            self._extract_python_imports(block)

    def _extract_cli_tools(self, code: str):
        """CLIツールを抽出"""
        cli_tools = [
            'gh', 'git', 'jq', 'curl', 'wget', 'docker', 'kubectl',
            'npm', 'node', 'yarn', 'pip', 'python', 'python3',
            'terraform', 'ansible', 'aws', 'gcloud', 'az'
        ]

        for tool in cli_tools:
            if re.search(rf'\b{tool}\b', code):
                self.dependencies['cli_tools'].add(tool)

    def _extract_python_imports(self, code: str):
        """Pythonインポートを抽出"""
        # import文を解析
        imports = re.findall(r'^\s*(?:import|from)\s+([\w.]+)', code, re.MULTILINE)
        for imp in imports:
            # 標準ライブラリを除外
            stdlib = {
                'os', 'sys', 're', 'json', 'pathlib', 'subprocess', 'argparse',
                'typing', 'collections', 'itertools', 'functools', 'datetime'
            }
            base_module = imp.split('.')[0]
            if base_module not in stdlib:
                self.dependencies['python_packages'].add(base_module)

    def _scan_scripts(self, directory: Path):
        """スクリプトをスキャン"""
        for file in directory.rglob('*'):
            if file.is_file():
                if file.suffix == '.py':
                    self._scan_python_script(file)
                elif file.suffix == '.sh':
                    self._scan_shell_script(file)
                elif file.suffix == '.js':
                    self._scan_javascript_script(file)

    def _scan_python_script(self, file: Path):
        """Pythonスクリプトをスキャン"""
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            self._extract_python_imports(content)
        except Exception:
            pass

    def _scan_shell_script(self, file: Path):
        """シェルスクリプトをスキャン"""
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            self._extract_cli_tools(content)
        except Exception:
            pass

    def _scan_javascript_script(self, file: Path):
        """JavaScriptスクリプトをスキャン"""
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            # require/import文を解析
            imports = re.findall(r'(?:require|import)\s*\(?\s*[\'"]([^\'"\)]+)', content)
            for imp in imports:
                # 相対パスでない場合はパッケージ
                if not imp.startswith('.'):
                    self.dependencies['npm_packages'].add(imp)
        except Exception:
            pass

    def _check_cli_tools(self) -> Dict:
        """CLIツールのインストール状況を確認"""
        status = {}
        for tool in self.dependencies['cli_tools']:
            installed = shutil.which(tool) is not None
            status[tool] = {
                'installed': installed,
                'path': shutil.which(tool) if installed else None
            }
        return status

    def _check_python_packages(self) -> Dict:
        """Pythonパッケージのインストール状況を確認"""
        status = {}
        for package in self.dependencies['python_packages']:
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'show', package],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                installed = result.returncode == 0
                version = None
                if installed:
                    version_match = re.search(r'Version:\s*(.+)', result.stdout)
                    if version_match:
                        version = version_match.group(1).strip()

                status[package] = {
                    'installed': installed,
                    'version': version
                }
            except Exception:
                status[package] = {
                    'installed': False,
                    'version': None
                }
        return status

    def _check_npm_packages(self) -> Dict:
        """npmパッケージのインストール状況を確認"""
        status = {}

        # npmが利用可能か確認
        if not shutil.which('npm'):
            return status

        for package in self.dependencies['npm_packages']:
            try:
                result = subprocess.run(
                    ['npm', 'list', '-g', package],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                installed = result.returncode == 0
                status[package] = {
                    'installed': installed,
                    'global': installed
                }
            except Exception:
                status[package] = {
                    'installed': False,
                    'global': False
                }
        return status

    def _check_all_satisfied(self, cli_status: Dict, python_status: Dict, npm_status: Dict) -> bool:
        """すべての依存関係が満たされているか"""
        all_cli = all(info['installed'] for info in cli_status.values())
        all_python = all(info['installed'] for info in python_status.values())
        all_npm = all(info['installed'] for info in npm_status.values())
        return all_cli and all_python and all_npm

    def _print_results(self, result: Dict):
        """結果を表示"""
        print("\n" + "=" * 60)
        print("DEPENDENCY CHECK RESULTS")
        print("=" * 60)

        # CLIツール
        if result['dependencies']['cli_tools']:
            print("\n📦 CLI Tools:")
            for tool, info in result['status']['cli_tools'].items():
                status = "✓" if info['installed'] else "✗"
                print(f"  {status} {tool}")
                if not info['installed']:
                    print(f"    Install: brew install {tool} (or appropriate package manager)")

        # Pythonパッケージ
        if result['dependencies']['python_packages']:
            print("\n🐍 Python Packages:")
            for package, info in result['status']['python_packages'].items():
                status = "✓" if info['installed'] else "✗"
                version = f" ({info['version']})" if info.get('version') else ""
                print(f"  {status} {package}{version}")
                if not info['installed']:
                    print(f"    Install: pip install {package}")

        # npmパッケージ
        if result['dependencies']['npm_packages']:
            print("\n📦 npm Packages:")
            for package, info in result['status']['npm_packages'].items():
                status = "✓" if info['installed'] else "✗"
                print(f"  {status} {package}")
                if not info['installed']:
                    print(f"    Install: npm install -g {package}")

        print("\n" + "=" * 60)
        if result['all_satisfied']:
            print("✓ All dependencies satisfied")
        else:
            print("⚠️  Some dependencies are missing")
        print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Check dependencies')
    parser.add_argument('--path', required=True, help='Path to resource directory')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    try:
        checker = DependencyChecker(args.path)
        result = checker.check()

        # 結果を保存
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"[INFO] Result saved to: {args.output}")

        # 終了コード
        sys.exit(0 if result['all_satisfied'] else 1)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
