#!/bin/bash

if ! type python3 > /dev/null; then
    echo "Please install python3 in your system and run this script again"
else
    if ! type pip3 > /dev/null; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    fi
    echo "Found python3 installed, will continue with setup"
    python3 -m virtualenv venv/

    . venv/bin/activate
    pip3 install -r requirements.txt
fi