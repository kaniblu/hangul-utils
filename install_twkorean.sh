#!/bin/bash

REPO_DIR=/tmp/twkorean

rm -rf $REPO_DIR
git clone https://github.com/open-korean-text/open-korean-text-wrapper-python $REPO_DIR
cd $REPO_DIR
python setup.py install
