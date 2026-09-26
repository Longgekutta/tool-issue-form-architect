# CORE INVARIANTS: tool-issue-form-architect

1. Schema Validity Invariance:
   - Generated Issue Forms MUST adhere strictly to GitHub's Issue Forms YAML schema (input, textarea, dropdown, checkboxes, validations).

2. Blank Issue Suppression Invariance:
   - Generated `.github/ISSUE_TEMPLATE/config.yml` MUST enforce `blank_issues_enabled: false` to eliminate unstructured issue noise.

3. Hermetic Generation Invariance:
   - Scaffolding and linting run 100% offline without network or GitHub API queries.
