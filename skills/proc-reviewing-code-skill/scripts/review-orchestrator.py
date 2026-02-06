#!/usr/bin/env python3
"""
review_orchestrator.py - コードレビュー全体のオーケストレーション

Usage:
    ./review_orchestrator.py --diff "<diff_content>" --context "<project_context>"
    ./review_orchestrator.py --help
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# スクリプトのディレクトリを取得
SCRIPT_DIR = Path(__file__).parent.resolve()
PARALLEL_REVIEW_SCRIPT = SCRIPT_DIR / "parallel-review.sh"


class ReviewOrchestrator:
    """コードレビュープロセスの統合管理"""

    def __init__(self, diff_content: str, project_context: str, max_retries: int = 2):
        self.diff_content = diff_content
        self.project_context = project_context
        self.max_retries = max_retries
        self.results: Optional[Dict] = None

    def validate_inputs(self) -> bool:
        """入力の検証"""
        logger.info("Validating inputs...")

        # 差分サイズチェック
        diff_lines = len(self.diff_content.split('\n'))
        logger.info(f"Diff size: {diff_lines} lines")

        if diff_lines == 0:
            logger.error("Empty diff provided")
            return False

        if diff_lines > 1000:
            logger.warning(
                f"Large diff detected ({diff_lines} lines). "
                "Consider splitting the review or reviewing specific files."
            )
            # 警告は出すが、処理は続行

        # 並列レビュースクリプトの存在確認
        if not PARALLEL_REVIEW_SCRIPT.exists():
            logger.error(f"Parallel review script not found: {PARALLEL_REVIEW_SCRIPT}")
            return False

        if not os.access(PARALLEL_REVIEW_SCRIPT, os.X_OK):
            logger.error(f"Parallel review script is not executable: {PARALLEL_REVIEW_SCRIPT}")
            return False

        logger.info("Input validation passed")
        return True

    def run_parallel_review(self) -> Optional[Dict]:
        """並列レビューの実行"""
        logger.info("Starting parallel review execution...")

        try:
            result = subprocess.run(
                [str(PARALLEL_REVIEW_SCRIPT), self.diff_content, self.project_context],
                capture_output=True,
                text=True,
                timeout=600  # 全体のタイムアウト: 10分
            )

            # stderrをログに出力（進捗情報が含まれる）
            if result.stderr:
                for line in result.stderr.split('\n'):
                    if line.strip():
                        logger.info(f"parallel_review: {line}")

            # JSON結果をパース
            if result.stdout:
                try:
                    review_data = json.loads(result.stdout)
                    logger.info("Successfully parsed review results")
                    return review_data
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON output: {e}")
                    logger.debug(f"Raw output: {result.stdout[:500]}")
                    return None

            # 出力がない場合
            logger.error("No output from parallel review script")
            return None

        except subprocess.TimeoutExpired:
            logger.error("Parallel review timed out after 10 minutes")
            return None
        except Exception as e:
            logger.error(f"Failed to execute parallel review: {e}")
            return None

    def validate_results(self, results: Dict) -> bool:
        """結果の検証"""
        logger.info("Validating results...")

        if not results:
            logger.error("Empty results")
            return False

        # review_summaryの確認
        if 'review_summary' not in results:
            logger.warning("Missing review_summary in results")
            return False

        summary = results['review_summary']
        total = summary.get('total_aspects', 0)
        successful = summary.get('successful', 0)
        failed = summary.get('failed', 0)

        logger.info(f"Review summary: {successful}/{total} aspects succeeded, {failed} failed")

        # 少なくとも1つの観点で成功している必要がある
        if successful == 0:
            logger.error("All review aspects failed")
            return False

        # aspectsの確認
        if 'aspects' not in results or not results['aspects']:
            logger.error("Missing or empty aspects in results")
            return False

        logger.info(f"Found {len(results['aspects'])} aspect results")

        # 各観点の結果をチェック
        for aspect in results['aspects']:
            aspect_name = aspect.get('aspect', 'unknown')
            if 'error' in aspect:
                logger.warning(f"Aspect '{aspect_name}' returned an error: {aspect.get('error')}")
            elif 'findings' in aspect:
                findings_count = len(aspect['findings'])
                logger.info(f"Aspect '{aspect_name}': {findings_count} findings")

        return True

    def merge_and_format_results(self, results: Dict) -> Dict:
        """結果のマージと整形"""
        logger.info("Merging and formatting results...")

        # サマリー情報の集計
        total_issues = 0
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }

        all_findings = []

        for aspect in results.get('aspects', []):
            if 'findings' in aspect:
                for finding in aspect['findings']:
                    all_findings.append(finding)
                    total_issues += 1

                    severity = finding.get('severity', 'unknown').lower()
                    if severity in severity_counts:
                        severity_counts[severity] += 1

        # 重要度順にソート
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'unknown': 4}
        all_findings.sort(key=lambda x: severity_order.get(x.get('severity', 'unknown').lower(), 4))

        # 最終レポート作成
        report = {
            'summary': {
                'total_issues': total_issues,
                'critical': severity_counts['critical'],
                'high': severity_counts['high'],
                'medium': severity_counts['medium'],
                'low': severity_counts['low']
            },
            'review_details': results.get('review_summary', {}),
            'findings_by_aspect': {},
            'all_findings': all_findings
        }

        # 観点別にグルーピング
        for aspect in results.get('aspects', []):
            aspect_name = aspect.get('aspect', 'unknown')
            report['findings_by_aspect'][aspect_name] = {
                'findings': aspect.get('findings', []),
                'count': len(aspect.get('findings', [])),
                'error': aspect.get('error')
            }

        logger.info(f"Formatted report: {total_issues} total issues found")
        return report

    def execute_with_retry(self) -> Optional[Dict]:
        """リトライロジック付きでレビューを実行"""
        for attempt in range(1, self.max_retries + 2):  # max_retries + 初回実行
            logger.info(f"Review attempt {attempt}/{self.max_retries + 1}")

            results = self.run_parallel_review()

            if results and self.validate_results(results):
                logger.info("Review completed successfully")
                return self.merge_and_format_results(results)

            if attempt <= self.max_retries:
                logger.warning(f"Retrying... ({attempt}/{self.max_retries} retries)")
            else:
                logger.error("Max retries reached, review failed")
                return None

        return None

    def run(self) -> bool:
        """メインのワークフロー実行"""
        logger.info("=" * 60)
        logger.info("Code Review Orchestrator - Starting")
        logger.info("=" * 60)

        # 1. Plan: 入力検証
        if not self.validate_inputs():
            logger.error("Input validation failed")
            return False

        # 2. Execute: 並列レビュー実行（リトライ付き）
        self.results = self.execute_with_retry()

        if not self.results:
            logger.error("Review execution failed")
            return False

        # 3. Verify: 結果出力
        logger.info("=" * 60)
        logger.info("Review Results")
        logger.info("=" * 60)
        logger.warning(
            "Review results may contain code snippets. "
            "Ensure no sensitive data is exposed in CI/CD logs."
        )
        print(json.dumps(self.results, indent=2, ensure_ascii=False))

        logger.info("=" * 60)
        logger.info("Code Review Orchestrator - Completed")
        logger.info("=" * 60)

        return True


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description='Code Review Orchestrator - 4観点並列レビューを統合管理'
    )
    parser.add_argument(
        '--diff',
        required=True,
        help='Git diff content to review'
    )
    parser.add_argument(
        '--context',
        required=True,
        help='Project context information'
    )
    parser.add_argument(
        '--max-retries',
        type=int,
        default=2,
        help='Maximum number of retries on failure (default: 2)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # オーケストレーター実行
    orchestrator = ReviewOrchestrator(
        diff_content=args.diff,
        project_context=args.context,
        max_retries=args.max_retries
    )

    success = orchestrator.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
