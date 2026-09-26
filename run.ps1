# PowerShell runner for tool-issue-form-architect
param(
    [string]$Command = "health",
    [string]$Target = ".",
    [string]$Owner = "maintainer"
)

switch ($Command) {
    "setup"    { python main.py setup }
    "run"      { python main.py run --target $Target }
    "test"     { python main.py test }
    "health"   { python main.py health }
    "clean"    { python main.py clean }
    "scaffold" { python main.py scaffold --target $Target --owner $Owner }
    "lint"     { python main.py lint --target $Target }
    Default    { python main.py $Command }
}
