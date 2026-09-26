"""Scaffolder generating GitHub issue forms and governance templates."""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from .templates import GovernanceTemplates

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

@dataclass
class ScaffoldConfig:
    owner: str = "maintainer"
    include_bug_report: bool = True
    include_feature_request: bool = True
    include_pr_template: bool = True
    include_codeowners: bool = True
    include_community_health: bool = False
    disable_blank_issues: bool = True

class IssueFormScaffolder:
    def __init__(self, config: Optional[ScaffoldConfig] = None):
        self.config = config or ScaffoldConfig()

    def scaffold(self, target_dir: str | Path) -> List[Path]:
        root = Path(target_dir).resolve()
        gh_dir = root / ".github"
        issue_dir = gh_dir / "ISSUE_TEMPLATE"
        issue_dir.mkdir(parents=True, exist_ok=True)

        created_files: List[Path] = []
        cfg = self.config

        # 1. config.yml
        if cfg.disable_blank_issues:
            c_file = issue_dir / "config.yml"
            c_file.write_text(GovernanceTemplates.config_yml(), encoding="utf-8")
            created_files.append(c_file)

        # 2. bug_report.yml
        if cfg.include_bug_report:
            br_file = issue_dir / "bug_report.yml"
            br_file.write_text(GovernanceTemplates.bug_report_yml(), encoding="utf-8")
            created_files.append(br_file)

        # 3. feature_request.yml
        if cfg.include_feature_request:
            fr_file = issue_dir / "feature_request.yml"
            fr_file.write_text(GovernanceTemplates.feature_request_yml(), encoding="utf-8")
            created_files.append(fr_file)

        # 4. pull_request_template.md
        if cfg.include_pr_template:
            pr_file = gh_dir / "pull_request_template.md"
            pr_file.write_text(GovernanceTemplates.pr_template_md(), encoding="utf-8")
            created_files.append(pr_file)

        # 5. CODEOWNERS
        if cfg.include_codeowners:
            co_file = gh_dir / "CODEOWNERS"
            co_file.write_text(GovernanceTemplates.codeowners(cfg.owner), encoding="utf-8")
            created_files.append(co_file)

        # 6. Community health suite
        if cfg.include_community_health:
            created_files.extend(self.scaffold_community_health(root, project_name=root.name))

        return created_files

    def scaffold_community_health(self, target_dir: str | Path, project_name: str = "") -> List[Path]:
        root = Path(target_dir).resolve()
        gh_dir = root / ".github"
        gh_dir.mkdir(parents=True, exist_ok=True)
        name = project_name or root.name
        created: List[Path] = []

        # SECURITY.md
        sec = root / "SECURITY.md"
        sec.write_text(GovernanceTemplates.security_md(name), encoding="utf-8")
        created.append(sec)

        # CONTRIBUTING.md
        contrib = root / "CONTRIBUTING.md"
        contrib.write_text(GovernanceTemplates.contributing_md(name), encoding="utf-8")
        created.append(contrib)

        # CODE_OF_CONDUCT.md
        coc = root / "CODE_OF_CONDUCT.md"
        coc.write_text(GovernanceTemplates.code_of_conduct_md(), encoding="utf-8")
        created.append(coc)

        # SUPPORT.md
        supp = root / "SUPPORT.md"
        supp.write_text(GovernanceTemplates.support_md(name), encoding="utf-8")
        created.append(supp)

        # FUNDING.yml
        funding = gh_dir / "FUNDING.yml"
        funding.write_text(GovernanceTemplates.funding_yml(self.config.owner), encoding="utf-8")
        created.append(funding)

        return created
