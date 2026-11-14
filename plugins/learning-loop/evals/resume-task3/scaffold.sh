#!/bin/bash
# Puts the day-one end state (the project, its handover note and its outside folder) in the workspace.
set -e
tar -xzf "$(cd "$(dirname "$0")" && pwd)/fixture.tgz"
