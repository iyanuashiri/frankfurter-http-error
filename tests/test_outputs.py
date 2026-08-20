"""
Use this file to define pytest tests that verify the outputs of the task.

This file will be copied to /tests/test_outputs.py and run by the /tests/test.sh file
from the working directory.
"""

import pytest
from aioresponses import aioresponses
from fastapi import HTTPException

from frankfurter.rest_adapter import RestAdapter


@pytest.mark.asyncio
async def test_get_raises_on_404():
    """Verify that RestAdapter.get() raises HTTPException with status 404 on not found.
    """
    adapter = RestAdapter()
    url = f"https://{adapter.hostname}/{adapter.ver}/latest?base=USD&symbols=ZZZ"

    with aioresponses() as mocked:
        mocked.get(url, status=404, payload={"message": "not found"})

        with pytest.raises(HTTPException) as exc_info:
            await adapter.get(url)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_succeeds_on_200():
    """Verify that RestAdapter.get() successfully returns parsed JSON on 200 response.
    """
    adapter = RestAdapter()
    url = f"https://{adapter.hostname}/{adapter.ver}/latest?base=USD&symbols=CAD"

    with aioresponses() as mocked:
        mocked.get(
            url,
            status=200,
            payload={"amount": 1.0, "base": "USD", "rates": {"CAD": 1.35}},
        )

        result = await adapter.get(url)

    assert result["base"] == "USD"
    assert result["rates"]["CAD"] == 1.35


@pytest.mark.asyncio
async def test_get_raises_exactly_at_400_boundary():
    """Status exactly 400 (the boundary the >= comparison must include) must raise."""
    adapter = RestAdapter()
    url = f"https://{adapter.hostname}/{adapter.ver}/latest?base=XXX&symbols=USD"

    with aioresponses() as mocked:
        mocked.get(url, status=400, payload={"message": "bad request"})
        with pytest.raises(HTTPException) as exc_info:
            await adapter.get(url)

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_get_succeeds_just_below_boundary():
    """Status 399 (just under the error threshold) must NOT raise."""
    adapter = RestAdapter()
    url = f"https://{adapter.hostname}/{adapter.ver}/latest?base=USD&symbols=CAD"

    with aioresponses() as mocked:
        mocked.get(url, status=399, payload={"amount": 1.0})
        result = await adapter.get(url)

    assert result["amount"] == 1.0    