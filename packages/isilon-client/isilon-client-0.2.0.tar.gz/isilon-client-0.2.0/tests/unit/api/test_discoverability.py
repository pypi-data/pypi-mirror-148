import pytest

from isilon.exceptions import TokenRetrieveException


@pytest.mark.asyncio
async def test_info(isilon_client):
    resp = await isilon_client.discoverability.info()
    assert isinstance(resp, str)


@pytest.mark.asyncio
async def test_info_failed_to_get_token(token_exeption, isilon_client2):
    with pytest.raises(TokenRetrieveException):
        await isilon_client2.discoverability.info()
