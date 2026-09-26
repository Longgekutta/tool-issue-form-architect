"""Linter for GitHub Issue Forms and CODEOWNERS governance contracts."""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re
from typing import List, Optional

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class IssueSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"

@dataclass
class FormLintIssue:
    file_path: str
    rule_id: str
    severity: IssueSeverity
    message: str
    remediation: str

class FormLinter:
    def lint_repo(self, root_dir: str | Path) -> List[FormLintIssue]:
        root = Path(root_dir).resolve()
        issues: List[FormLintIssue] = []

        gh_dir = root / ".github"
        if not gh_dir.is_dir():
            issues.append(FormLintIssue(
                file_path=str(root),
                rule_id="GOV_MISSING_GITHUB_DIR",
                severity=IssueSeverity.WARNING,
                message="Missing .github directory. Repository has no cloud-native governance scaffolding.",
                remediation="Run 'python main.py scaffold' to create issue forms and PR templates."
            ))
            return issues

        tmpl_dir = gh_dir / "ISSUE_TEMPLATE"
        if not tmpl_dir.is_dir():
            issues.append(FormLintIssue(
                file_path=str(gh_dir),
                rule_id="GOV_MISSING_ISSUE_TEMPLATE_DIR",
                severity=IssueSeverity.WARNING,
                message="Missing .github/ISSUE_TEMPLATE directory.",
                remediation="Run 'python main.py scaffold' to generate structured issue templates."
            ))
        else:
            # Check config.yml
            cfg_file = tmpl_dir / "config.yml"
            if not cfg_file.exists():
                issues.append(FormLintIssue(
                    file_path=str(tmpl_dir),
                    rule_id="GOV_MISSING_CONFIG_YML",
                    severity=IssueSeverity.WARNING,
                    message="Missing .github/ISSUE_TEMPLATE/config.yml. Blank unstructured issues remain allowed.",
                    remediation="Add config.yml with 'blank_issues_enabled: false'."
                ))
            else:
                try:
                    c_txt = cfg_file.read_text(encoding="utf-8", errors="ignore")
                    if "blank_issues_enabled: false" not in c_txt:
                        issues.append(FormLintIssue(
                            file_path=str(cfg_file),
                            rule_id="GOV_BLANK_ISSUES_ALLOWED",
                            severity=IssueSeverity.WARNING,
                            message="blank_issues_enabled is not set to false.",
                            remediation="Set 'blank_issues_enabled: false' in config.yml."
                        ))
                except Exception as e:
                    pass

            # Check yaml forms
            yml_forms = list(tmpl_dir.glob("*.yml")) + list(tmpl_dir.glob("*.yaml"))
            yml_forms = [f for f in yml_forms if f.name != "config.yml"]
            if not yml_forms:
                issues.append(FormLintIssue(
                    file_path=str(tmpl_dir),
                    rule_id="GOV_NO_YAML_FORMS",
                    severity=IssueSeverity.WARNING,
                    message="No YAML issue forms found in .github/ISSUE_TEMPLATE/.",
                    remediation="Scaffold structured YAML issue forms (e.g. bug_report.yml, feature_request.yml)."
                ))
            for yml in yml_forms:
                try:
                    txt = yml.read_text(encoding="utf-8", errors="ignore")
                    if "name:" not in txt or "description:" not in txt or "body:" not in txt:
                        issues.append(FormLintIssue(
                            file_path=str(yml),
                            rule_id="GOV_MALFORMED_FORM_HEADER",
                            severity=IssueSeverity.CRITICAL,
                            message=f"Issue form {yml.name} lacks required top-level keys ('name', 'description', or 'body').",
                            remediation="Ensure form declares 'name:', 'description:', and 'body:' list."
                        ))
                except Exception:
                    pass

        # Check pull_request_template.md
        pr_tmpl = gh_dir / "pull_request_template.md"
        if not pr_tmpl.exists():
            issues.append(FormLintIssue(
                file_path=str(gh_dir),
                rule_id="GOV_MISSING_PR_TEMPLATE",
                severity=IssueSeverity.INFO,
                message="Missing .github/pull_request_template.md.",
                remediation="Generate pull_request_template.md to enforce contribution checklist."
            ))

        # Check CODEOWNERS
        codeowners = gh_dir / "CODEOWNERS"
        if not codeowners.exists():
            codeowners = root / "CODEOWNERS"
        if not codeowners.exists():
            issues.append(FormLintIssue(
                file_path=str(gh_dir),
                rule_id="GOV_MISSING_CODEOWNERS",
                severity=IssueSeverity.INFO,
                message="Missing CODEOWNERS file for automated review assignment.",
                remediation="Create .github/CODEOWNERS mapping directory patterns to maintainers."
            ))

        return issues
