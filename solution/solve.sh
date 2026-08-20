#!/bin/bash

sed -i 's/response.status > 400/response.status >= 400/' \
    /app/frankfurter/rest_adapter.py

echo "Fixed off-by-one in HTTP error status check"