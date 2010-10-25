#!/bin/bash
SRC=$(dirname $0)/starcluster_plugins
echo ">>> Running pyflakes..."
find $SRC -iname \*.py -exec pyflakes {} \;
echo ">>> Running pep8..."
find $SRC -iname \*.py -exec pep8 {} \;
echo ">>> Done"
