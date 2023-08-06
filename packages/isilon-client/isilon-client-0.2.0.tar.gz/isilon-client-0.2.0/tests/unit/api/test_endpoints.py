import pytest

from isilon.exceptions import TokenRetrieveException


@pytest.mark.asyncio
async def test_call(isilon_client):
    resp = await isilon_client.endpoints()
    assert resp == ""


@pytest.mark.asyncio
async def test_failed_to_get_token(token_exeption, isilon_client2):
    with pytest.raises(TokenRetrieveException):
        await isilon_client2.endpoints()
