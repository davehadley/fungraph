#!/usr/bin/env bash
version=$(python -c "import fungraph; print(fungraph.__version__)")
mkdir testrelease && cd testrelease
python3 -m venv venvrelease
source venvrelease/bin/activate
pip install --no-cache-dir --upgrade "fungraph>=${version}"
cp -r ../tests ./
python -m unittest discover tests
