"""Hermetic offline unit tests for tool-issue-form-architect."""
import tempfile
import unittest
from pathlib import Path

from core.templates import GovernanceTemplates
from core.scaffolder import IssueFormScaffolder, ScaffoldConfig
from core.linter import FormLinter, IssueSeverity

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class TestIssueFormArchitectOffline(unittest.TestCase):
    def test_01_templates_have_required_yaml_schema(self):
        bug_yml = GovernanceTemplates.bug_report_yml()
        self.assertIn("name: 🐛 Bug Report", bug_yml)
        self.assertIn("validations:", bug_yml)
        self.assertIn("required: true", bug_yml)
        self.assertIn("type: dropdown", bug_yml)

        feat_yml = GovernanceTemplates.feature_request_yml()
        self.assertIn("name: 💡 Feature Request", feat_yml)
        self.assertIn("Problem Statement", feat_yml)

        cfg_yml = GovernanceTemplates.config_yml()
        self.assertIn("blank_issues_enabled: false", cfg_yml)

    def test_02_scaffolder_creates_all_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scaffolder = IssueFormScaffolder()
            created = scaffolder.scaffold(tmp)

            self.assertEqual(len(created), 5)
            self.assertTrue((tmp / ".github" / "ISSUE_TEMPLATE" / "config.yml").exists())
            self.assertTrue((tmp / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml").exists())
            self.assertTrue((tmp / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml").exists())
            self.assertTrue((tmp / ".github" / "pull_request_template.md").exists())
            self.assertTrue((tmp / ".github" / "CODEOWNERS").exists())

    def test_03_scaffolder_custom_owner_in_codeowners(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scaffolder = IssueFormScaffolder(ScaffoldConfig(owner="octocat-lead"))
            scaffolder.scaffold(tmp)

            co_txt = (tmp / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
            self.assertIn("@octocat-lead", co_txt)

    def test_04_linter_detects_empty_repo_findings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            linter = FormLinter()
            issues = linter.lint_repo(tmpdir)
            rule_ids = [i.rule_id for i in issues]
            self.assertIn("GOV_MISSING_GITHUB_DIR", rule_ids)

    def test_05_linter_passes_on_scaffolded_repo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scaffolder = IssueFormScaffolder()
            scaffolder.scaffold(tmp)

            linter = FormLinter()
            issues = linter.lint_repo(tmp)
            criticals = [i for i in issues if i.severity == IssueSeverity.CRITICAL]
            self.assertEqual(len(criticals), 0)

    def test_06_community_health_scaffold_and_lint(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            scaffolder = IssueFormScaffolder(ScaffoldConfig(include_community_health=True))
            scaffolder.scaffold(tmp)

            self.assertTrue((tmp / "SECURITY.md").exists())
            self.assertTrue((tmp / "CONTRIBUTING.md").exists())
            self.assertTrue((tmp / "CODE_OF_CONDUCT.md").exists())
            self.assertTrue((tmp / "SUPPORT.md").exists())
            self.assertTrue((tmp / ".github" / "FUNDING.yml").exists())

            linter = FormLinter()
            issues = linter.lint_repo(tmp)
            rule_ids = [i.rule_id for i in issues]
            self.assertNotIn("GOV_MISSING_SECURITY_POLICY", rule_ids)
            self.assertNotIn("GOV_MISSING_CONTRIBUTING_GUIDE", rule_ids)

if __name__ == "__main__":
    unittest.main()
