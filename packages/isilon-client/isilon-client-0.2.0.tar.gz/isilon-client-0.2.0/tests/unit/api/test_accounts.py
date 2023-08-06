import pytest


@pytest.mark.asyncio
async def test_show(isilon_client):
    resp = await isilon_client.accounts.show("test")
    assert isinstance(resp, str)


@pytest.mark.asyncio
async def test_update(isilon_client):
    resp = await isilon_client.accounts.update("test")
    assert resp is not None


@pytest.mark.asyncio
async def test_metadata(isilon_client):
    resp = await isilon_client.accounts.metadata("test")
    assert "X-Object-Meta" in resp
