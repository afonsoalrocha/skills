#!/usr/bin/env bash
# Run the marketplace checks. LEAK_DENYLIST, when set, is a newline-separated
# list of terms. The scan skips with a notice when the variable is absent.
set -euo pipefail

cd "$(dirname "$0")/.."
exec python3 scripts/validate.py "$@"
