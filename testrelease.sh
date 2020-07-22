#!/usr/bin/env bash
mkdir testrelease && cd testrelease
python3 -m venv venvrelease
source venvrelease/bin/activate
pip install fungraph
python -m unittest discover ../tests
