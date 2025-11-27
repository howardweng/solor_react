"""Custom pytest plugin for markdown report generation."""
import os
from datetime import datetime

import pytest


def pytest_addoption(parser):
    """Add command line option for markdown report."""
    group = parser.getgroup("markdown report")
    group.addoption(
        "--md-report",
        action="store",
        dest="md_report",
        default=None,
        help="Generate markdown report to given file path",
    )


def pytest_configure(config):
    """Configure the markdown report plugin."""
    md_path = config.getoption("md_report")
    if md_path:
        config._md_report = MarkdownReport(md_path)
        config.pluginmanager.register(config._md_report)


def pytest_unconfigure(config):
    """Unregister the plugin."""
    md_report = getattr(config, "_md_report", None)
    if md_report:
        config.pluginmanager.unregister(md_report)
        del config._md_report


class MarkdownReport:
    """Generate markdown test reports."""

    def __init__(self, path):
        self.path = path
        self.results = []
        self.start_time = None
        self.end_time = None

    def pytest_sessionstart(self, session):
        """Record session start time."""
        self.start_time = datetime.now()

    def pytest_runtest_logreport(self, report):
        """Collect test results."""
        if report.when == "call" or (report.when == "setup" and report.skipped):
            self.results.append({
                "nodeid": report.nodeid,
                "outcome": report.outcome,
                "duration": report.duration,
                "longrepr": str(report.longrepr) if report.longrepr else None,
            })

    def pytest_sessionfinish(self, session, exitstatus):
        """Generate the markdown report."""
        self.end_time = datetime.now()

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        # Count results
        passed = sum(1 for r in self.results if r["outcome"] == "passed")
        failed = sum(1 for r in self.results if r["outcome"] == "failed")
        skipped = sum(1 for r in self.results if r["outcome"] == "skipped")
        total = len(self.results)
        duration = (self.end_time - self.start_time).total_seconds()

        # Generate markdown
        lines = [
            f"# Test Report",
            f"",
            f"**Generated:** {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## Summary",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Tests | {total} |",
            f"| Passed | {passed} |",
            f"| Failed | {failed} |",
            f"| Skipped | {skipped} |",
            f"| Duration | {duration:.2f}s |",
            f"",
            f"## Results",
            f"",
            f"| Status | Test | Duration |",
            f"|--------|------|----------|",
        ]

        # Add each test result
        status_emoji = {"passed": "PASS", "failed": "FAIL", "skipped": "SKIP"}
        for result in self.results:
            status = status_emoji.get(result["outcome"], result["outcome"])
            test_name = result["nodeid"].split("::")[-1]
            module = result["nodeid"].split("::")[0].replace("tests/", "")
            duration_str = f"{result['duration']:.3f}s"
            lines.append(f"| {status} | `{module}::{test_name}` | {duration_str} |")

        # Add skipped details section
        skipped_tests = [r for r in self.results if r["outcome"] == "skipped"]
        if skipped_tests:
            lines.extend([
                f"",
                f"## Skipped Tests (Database Unavailable)",
                f"",
                f"The following tests were skipped due to database unavailability (503 response):",
                f"",
            ])
            for result in skipped_tests:
                test_name = result["nodeid"].split("::")[-1]
                lines.append(f"- `{test_name}`")

        # Add failed details section
        failed_tests = [r for r in self.results if r["outcome"] == "failed"]
        if failed_tests:
            lines.extend([
                f"",
                f"## Failed Tests",
                f"",
            ])
            for result in failed_tests:
                test_name = result["nodeid"].split("::")[-1]
                lines.append(f"### `{test_name}`")
                lines.append(f"")
                lines.append(f"```")
                lines.append(result["longrepr"] or "No details available")
                lines.append(f"```")
                lines.append(f"")

        # Write the file
        with open(self.path, "w") as f:
            f.write("\n".join(lines))
