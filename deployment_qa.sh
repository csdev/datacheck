#!/bin/bash
set -e

if [ "$#" != 1 ]; then
    echo "Usage: $0 <version_number>"
    exit 1
fi

VENV_NAME="venv3-temp-qa-$(date '+%s')"

function cleanup {
    rm -rf "$VENV_NAME"
}
trap cleanup EXIT

echo "Creating temporary virtualenv ..."
virtualenv -p python3 "$VENV_NAME"
source "$VENV_NAME/bin/activate"

echo "Checking package installation, version $1 ..."
pip install "datacheck==$1"

echo "Checking package import ..."

# if we run this from the script location, python may fall back to importing
# development code in the working directory, resulting in a false success
(cd "$VENV_NAME" && python -c 'import datacheck')

echo "SUCCESS!"
