#!/bin/sh

# This script should be run as following:
# . ./install.sh
# Note the first dot is required for export to work in your terminal.

pushd $(dirname $(readlink -f "$BASH_SOURCE")) > /dev/null
SCRIPT_DIR="$PWD"
popd > /dev/null
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"
