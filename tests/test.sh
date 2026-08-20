#!/bin/bash

cp "$(dirname "$0")/test_outputs.py" /app/tests/test_outputs.py
cd /app

uv run pytest tests/ -v

if [ $? -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
else
    echo 0 > /logs/verifier/reward.txt
fi