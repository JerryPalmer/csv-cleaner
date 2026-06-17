param(
    [string]$Input = "${PSScriptRoot}\sample.csv",
    [string]$Output = "${PSScriptRoot}\cleaned.csv",
    [switch]$Open
)

$python = Join-Path $PSScriptRoot ".\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Error "Virtualenv python not found at $python. Create the .venv and install requirements first."
    exit 1
}

# Build argument list
$args = @()
$args += $Input
$args += $Output
if ($Open) { $args += '--open-output' }

# Run
& $python $PSScriptRoot\clean_csv.py @args
