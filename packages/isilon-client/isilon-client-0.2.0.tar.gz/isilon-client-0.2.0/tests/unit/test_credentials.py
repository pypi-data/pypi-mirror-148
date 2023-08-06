import pytest

from isilon.exceptions import TokenRetrieveException


@pytest.mark.asyncio
async def test_token(isilon_client):
    token = await isilon_client.credentials.token()
    assert token == "abc123lkj"


@pytest.mark.asyncio
async def test_token_failed(token_exeption, isilon_client2):
    with pytest.raises(TokenRetrieveException):
        await isilon_client2.credentials.token()


@pytest.mark.asyncio
async def test_x_auth_token(isilon_client):
    auth_token = await isilon_client.credentials.x_auth_token()
    assert auth_token == {"X-Auth-Token": "abc123lkj"}


@pytest.mark.asyncio
async def test_x_auth_token_failed(token_exeption, isilon_client2):
    with pytest.raises(TokenRetrieveException):
        await isilon_client2.credentials.x_auth_token()
