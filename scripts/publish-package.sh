#!/usr/bin/env bash
# Print trace of commands
set -x 
set -e

rm -rf dist

poetry build

poetry publish
