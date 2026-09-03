# axiom-sdd — wrapper fino (Windows): toda a logica vive em cli/axiom.py (Python 3.8+, stdlib).
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) { & py -3 "$dir\cli\axiom.py" @args; exit $LASTEXITCODE }
$py3 = Get-Command python -ErrorAction SilentlyContinue
if ($py3) { & python "$dir\cli\axiom.py" @args; exit $LASTEXITCODE }
Write-Error "Python 3.8+ nao encontrado. Instale via winget install Python.Python.3"; exit 1
