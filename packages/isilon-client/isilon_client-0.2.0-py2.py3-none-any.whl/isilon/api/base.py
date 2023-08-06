from aiohttp import ClientSession

from isilon import exceptions


class BaseAPI:
    API_VERSION = "v1"

    def __init__(self, client) -> None:
        self._client = client

    async def include_auth_header(self, **kwargs: dict) -> dict:
        token = await self._client.credentials.x_auth_token()
        kwargs.update({"headers": token})
        return kwargs

    async def account_primary_key(self) -> str:
        metadata = await self._client.accounts.metadata(self.account)
        try:
            key = metadata["X-Account-Meta-Temp-URL-Key"]
        except KeyError:
            key = metadata["X-Account-Meta-Temp-Url-Key"]
        except KeyError:
            raise exceptions.NoTempURLKey(
                f"Account: {self.account} does not have 'X-Account-Meta-Temp-URL-Key', please see: https://docs.openstack.org/swift/latest/api/temporary_url_middleware.html#secret-keys"
            )
        return str(key)

    @property
    def address(self) -> str:
        return self._client.address  # type: ignore

    @property
    def http(self) -> ClientSession:
        return self._client.http  # type: ignore

    @property
    def account(self) -> str:
        return self._client.account  # type: ignore

    def __repr__(self) -> str:
        *_, name = str(self.__class__).split(".")
        return f"{name[:-2]}(api_version='{self.API_VERSION}')"
