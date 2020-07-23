#!/usr/bin/env bash
versionsource=$(cat fungraph/_version.py);
version=$(python -c "${versionsource};print(__version__)");
mkdir testrelease && cd testrelease && python3 -m venv venvrelease && source venvrelease/bin/activate && cp -r ../tests ./

if [ $? -ne 0 ]; then
    exit 1
fi

pip install --no-cache-dir --upgrade "fungraph>=${version}" && python -m unittest discover tests
