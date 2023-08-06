import asyncio

from isilon import init_client


class Operator:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.client = self.loop.run_until_complete(init_client())

    def execute(self, command, *args, **kwargs):
        resp = self.loop.run_until_complete(command(*args, **kwargs))
        return resp
