#!/usr/bin/env sh
# axiom-sdd — wrapper fino: toda a logica vive em cli/axiom.py (Python 3.8+, stdlib).
DIR="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-}"
[ -z "$PY" ] && command -v python3 >/dev/null 2>&1 && PY=python3
[ -z "$PY" ] && command -v python  >/dev/null 2>&1 && PY=python
[ -z "$PY" ] && { echo "erro: Python 3.8+ nao encontrado (defina \$PYTHON)"; exit 1; }
exec "$PY" "$DIR/cli/axiom.py" "$@"
