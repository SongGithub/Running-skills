#!/bin/sh
# Install the guarded publisher into an existing local running workspace.
set -eu
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /absolute/path/to/local-running-workspace" >&2
  exit 2
fi
workspace=$1
case "$workspace" in /*) ;; *) echo "Workspace path must be absolute" >&2; exit 2;; esac
if [ ! -f "$workspace/strava_mcp_server.py" ]; then
  echo "Local Strava adapter not found; refusing installation" >&2
  exit 2
fi
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
install -m 0644 "$script_dir/pre_publish_hook.py" "$workspace/pre_publish_hook.py"
install -m 0755 "$script_dir/publish.py" "$workspace/strava_publish.py"
echo "Installed guarded publisher. Private policy is not created or modified."
