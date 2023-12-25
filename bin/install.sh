#!/usr/bin/env bash

echo "Installing requirements..."

pip3 install --upgrade setuptools
pip3 install pip-tools

pip3 install -r requirements.txt
