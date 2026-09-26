"""Templates for GitHub Issue Forms, PR templates, and CODEOWNERS."""
from dataclasses import dataclass

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class GovernanceTemplates:
    @staticmethod
    def config_yml() -> str:
        return """blank_issues_enabled: false
contact_links:
  - name: Community Discussions & Q&A
    url: https://github.com/discussions
    about: Ask general questions, share ideas, or get help from the community.
  - name: Security Vulnerability Reporting
    url: https://github.com/security/advisories/new
    about: Privately report a security issue under Coordinated Vulnerability Disclosure.
"""

    @staticmethod
    def bug_report_yml() -> str:
        return """name: 🐛 Bug Report
description: File a structured report to help us reproduce and resolve an unexpected issue.
title: "[BUG]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting an issue! Please provide detailed and deterministic steps to reproduce.
  - type: input
    id: version
    attributes:
      label: Software / Package Version
      description: What version or Git commit are you running?
      placeholder: e.g. v1.2.0 or commit abc1234
    validations:
      required: true
  - type: dropdown
    id: os
    attributes:
      label: Operating System / Environment
      description: What platform did this error occur on?
      options:
        - Linux (Ubuntu / Debian)
        - Linux (Arch / Fedora)
        - Windows 11 / 10
        - macOS (Apple Silicon)
        - macOS (Intel)
        - Docker Container
    validations:
      required: true
  - type: textarea
    id: reproduce
    attributes:
      label: Steps to Reproduce
      description: List the exact sequential steps to reproduce the bug.
      placeholder: |
        1. Run command '...'
        2. Provide input '...'
        3. See error '...'
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Relevant Log Output or Stacktrace
      description: Please copy and paste any relevant logs or terminal output.
      render: shell
    validations:
      required: false
  - type: checkboxes
    id: checklist
    attributes:
      label: Validation Checklist
      description: Confirm before submitting
      options:
        - label: I have searched existing Issues and Discussions to ensure this is not a duplicate.
          required: true
        - label: I have included all necessary logs and minimal reproducible examples.
          required: true
"""

    @staticmethod
    def feature_request_yml() -> str:
        return """name: 💡 Feature Request / Proposal
description: Suggest an idea or architectural enhancement for this project.
title: "[FEAT]: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        We welcome well-scoped, first-principles feature proposals and improvements!
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement & Motivation
      description: What pain point or limitation does this proposal solve?
      placeholder: "I am always frustrated when..."
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution & Architecture
      description: Describe the design, CLI interface, or API additions you would like to see.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Approaches Considered
      description: What other solutions or workarounds have you evaluated?
    validations:
      required: false
"""

    @staticmethod
    def pr_template_md() -> str:
        return """## 🎯 Summary of Changes

Briefly explain the intent, scope, and technical rationale of this Pull Request.

Fixes #(issue)

## 🔍 Type of Change
- [ ] 🐛 Bug fix (non-breaking change fixing an existing defect)
- [ ] 🚀 New feature (non-breaking change adding functionality)
- [ ] 🚨 Breaking change (fix or feature modifying existing contracts)
- [ ] 📚 Documentation update / Refactoring

## 🧪 Verification & Testing
- [ ] Hermetic unit tests added / updated and passing (`python main.py test`)
- [ ] Health status verified healthy (`python main.py health`)
- [ ] No regression or memory leak detected

## 🛡️ Checklist
- [ ] My code adheres to the project's coding style and AST quality gates
- [ ] I have updated the documentation / README accordingly
- [ ] I have declared least-privilege permissions and defensive error boundaries
"""

    @staticmethod
    def codeowners(owner: str) -> str:
        clean_owner = f"@{owner.lstrip('@')}" if owner else "@maintainer"
        return f"""# GitHub CODEOWNERS
# Reference: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

# Default owner for everything in the repository
*                   {clean_owner}

# Core business logic and engine
/core/              {clean_owner}

# GitHub Actions workflows and automation
/.github/workflows/ {clean_owner}

# Documentation and Specifications
/specs/             {clean_owner}
/docs/              {clean_owner}
"""
