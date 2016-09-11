#!/bin/bash
set -e
cd $(dirname $0)/..
sphinx-apidoc -H reffipe -f -o build/.tmp reffipe
rsync --checksum build/.tmp/*.rst doc/
sphinx-build -W doc -d build/sphinx/doctrees build/sphinx/html
if ! [ -z "`git status --porcelain`" ]; then
    echo "Modified files found!"
    git status --porcelain
    exit 1
fi
