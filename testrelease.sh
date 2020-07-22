#!/usr/bin/env bash
mkdir testrelease && cd testrelease
python3 -m venv venvrelease
source venvrelease/bin/activate
pip install --no-cache-dir --upgrade fungraph
python -m unittest discover ../tests
