"""Custom pytest plugin for markdown report generation."""
import glob
import os
import shutil
from datetime import datetime

import pytest


# Default reports directory (under tests folder)
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
ARCHIVE_DIR = os.path.join(REPORTS_DIR, "archive")


# Endpoint mapping for each test file
ENDPOINT_INFO = {
    "test_health.py": {
        "description": "Health Check Endpoints",
        "endpoints": [
            ("GET", "/", "Service info"),
            ("GET", "/health", "Basic health check"),
            ("GET", "/health/detailed", "Detailed infrastructure status"),
            ("GET", "/health/live", "Kubernetes liveness probe"),
            ("GET", "/health/ready", "Kubernetes readiness probe"),
        ],
    },
    "test_auth.py": {
        "description": "Authentication Endpoints",
        "endpoints": [
            ("POST", "/api/v1/auth/login", "Form-based login"),
            ("POST", "/api/v1/auth/login/json", "JSON-based login"),
            ("POST", "/api/v1/auth/refresh", "Refresh access token"),
            ("GET", "/api/v1/auth/me", "Get current user info"),
            ("POST", "/api/v1/auth/logout", "Logout user"),
        ],
    },
    "test_bess.py": {
        "description": "BESS (Battery Energy Storage System) Endpoints",
        "endpoints": [
            ("GET", "/api/v1/bess/{bess_number}", "Get BESS unit info (1-12)"),
            ("GET", "/api/v1/bess/alert/rack/{rack_number}", "Get rack alerts (rack01-rack12)"),
        ],
    },
    "test_pcs.py": {
        "description": "PCS (Power Conversion System) Endpoints",
        "endpoints": [
            ("GET", "/api/v1/pcs/{pcs_number}", "Get PCS unit info (1-12)"),
            ("GET", "/api/v1/pcs/alert", "Get PCS alert status"),
        ],
    },
    "test_inverter.py": {
        "description": "Inverter Endpoints",
        "endpoints": [
            ("GET", "/api/v1/inverter", "Get inverter data (MPPT, strings, phases)"),
        ],
    },
    "test_meters.py": {
        "description": "Meter Endpoints",
        "endpoints": [
            ("GET", "/api/v1/meters", "Get all meter info"),
            ("GET", "/api/v1/meters/aux", "Get auxiliary meter data (chart/summary)"),
        ],
    },
    "test_config.py": {
        "description": "Configuration Endpoints",
        "endpoints": [
            ("GET", "/api/v1/config/sidebar", "Get sidebar configuration"),
            ("GET", "/api/v1/config/header", "Get header alert summary"),
        ],
    },
    "test_system.py": {
        "description": "System Endpoints",
        "endpoints": [
            ("GET", "/api/v1/system/overview", "Get system overview"),
            ("GET", "/api/v1/system/topology", "Get system topology (nodes/links)"),
        ],
    },
    "test_schedule.py": {
        "description": "Schedule & Income Endpoints",
        "endpoints": [
            ("GET", "/api/v1/schedule", "Get schedule events"),
            ("GET", "/api/v1/schedule/income/daily", "Get daily income data"),
            ("GET", "/api/v1/schedule/income/monthly", "Get monthly income data"),
            ("GET", "/api/v1/schedule/exec-rate", "Get execution rate data"),
        ],
    },
    "test_analysis.py": {
        "description": "Power Analysis Endpoints",
        "endpoints": [
            ("GET", "/api/v1/analysis/power-loss", "Get power loss analysis"),
            ("GET", "/api/v1/analysis/power-io", "Get power I/O data"),
            ("GET", "/api/v1/analysis/freq-power", "Get frequency-power data"),
        ],
    },
}


def archive_existing_reports():
    """Move existing reports to archive folder."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # Find all report files in root reports folder (not in archive)
    for report_file in glob.glob(os.path.join(REPORTS_DIR, "test_report_*.md")):
        if os.path.isfile(report_file):
            filename = os.path.basename(report_file)
            archive_path = os.path.join(ARCHIVE_DIR, filename)
            shutil.move(report_file, archive_path)


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
    group.addoption(
        "--md-report-auto",
        action="store_true",
        dest="md_report_auto",
        default=False,
        help="Auto-generate markdown report with timestamp in tests/reports/",
    )


def pytest_configure(config):
    """Configure the markdown report plugin."""
    md_path = config.getoption("md_report")
    md_auto = config.getoption("md_report_auto")

    if md_auto:
        # Archive existing reports and create new one with timestamp
        archive_existing_reports()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        md_path = os.path.join(REPORTS_DIR, f"test_report_{timestamp}.md")

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
        ]

        # Add API Endpoints Coverage section
        lines.extend([
            f"## API Endpoints Coverage",
            f"",
        ])

        # Count total endpoints
        total_endpoints = sum(len(info["endpoints"]) for info in ENDPOINT_INFO.values())
        lines.append(f"**Total Endpoints Tested:** {total_endpoints}")
        lines.append(f"")

        for test_file, info in ENDPOINT_INFO.items():
            # Count tests for this module
            module_results = [r for r in self.results if test_file in r["nodeid"]]
            module_passed = sum(1 for r in module_results if r["outcome"] == "passed")
            module_skipped = sum(1 for r in module_results if r["outcome"] == "skipped")
            module_failed = sum(1 for r in module_results if r["outcome"] == "failed")
            module_total = len(module_results)

            if module_total == 0:
                status_badge = "⚪"
            elif module_failed > 0:
                status_badge = "🔴"
            elif module_skipped == module_total:
                status_badge = "🟡"
            elif module_passed == module_total:
                status_badge = "🟢"
            else:
                status_badge = "🟡"

            lines.extend([
                f"### {status_badge} {info['description']}",
                f"",
                f"**Test File:** `{test_file}` | **Tests:** {module_passed} passed, {module_skipped} skipped, {module_failed} failed",
                f"",
                f"| Method | Endpoint | Description |",
                f"|--------|----------|-------------|",
            ])

            for method, endpoint, description in info["endpoints"]:
                lines.append(f"| `{method}` | `{endpoint}` | {description} |")

            lines.append(f"")

        # Add detailed results section
        lines.extend([
            f"## Detailed Test Results",
            f"",
            f"| Status | Test | Duration |",
            f"|--------|------|----------|",
        ])

        # Add each test result
        status_emoji = {"passed": "✅ PASS", "failed": "❌ FAIL", "skipped": "⏭️ SKIP"}
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
                f"The following {len(skipped_tests)} tests were skipped due to database unavailability (503 response):",
                f"",
            ])
            for result in skipped_tests:
                test_name = result["nodeid"].split("::")[-1]
                module = result["nodeid"].split("::")[0].replace("tests/", "")
                lines.append(f"- `{module}::{test_name}`")

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
                lines.append(f"### ❌ `{test_name}`")
                lines.append(f"")
                lines.append(f"```")
                lines.append(result["longrepr"] or "No details available")
                lines.append(f"```")
                lines.append(f"")

        # Write the file
        with open(self.path, "w") as f:
            f.write("\n".join(lines))
