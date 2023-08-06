import os
from typing import Optional

from aiohttp import ClientSession
from attrs import field, mutable, validators

from .api import Accounts, Containers, Discoverability, Endpoints, Objects
from .creds import Credentials


@mutable
class IsilonClient:
    http: Optional[ClientSession] = field(
        validator=validators.optional(validators.instance_of(ClientSession)),
        repr=False,
    )
    address: str = field(
        default=os.getenv("ISILON_ADDRESS", "http://localhost:8080"),
        validator=validators.instance_of(str),
    )
    account: str = field(
        default=os.getenv("ISILON_ACCOUNT", "test"),
        validator=validators.instance_of(str),
    )
    user: str = field(
        default=os.getenv("ISILON_USER", "tester"),
        validator=validators.instance_of(str),
    )
    password: str = field(
        default=os.getenv("ISILON_PASSWORD", "testing"),
        validator=validators.instance_of(str),
    )

    credentials = field(init=False, repr=False)
    discoverability = field(init=False, repr=False)
    objects = field(init=False, repr=False)
    containers = field(init=False, repr=False)
    endpoints = field(init=False, repr=False)
    accounts = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self.credentials = Credentials(self)
        self.discoverability = Discoverability(self)
        self.objects = Objects(self)
        self.containers = Containers(self)
        self.endpoints = Endpoints(self)
        self.accounts = Accounts(self)

    async def close(self):
        await self.http.close()


async def init_client(
    address: str = os.getenv("ISILON_ADDRESS", "http://localhost:8080"),
    account: str = os.getenv("ISILON_ACCOUNT", "test"),
    user: str = os.getenv("ISILON_USER", "tester"),
    password: str = os.getenv("ISILON_PASSWORD", "testing"),
    http: Optional[ClientSession] = None,
) -> IsilonClient:
    if http is None:
        http = ClientSession()
    return IsilonClient(http, address, account, user, password)
