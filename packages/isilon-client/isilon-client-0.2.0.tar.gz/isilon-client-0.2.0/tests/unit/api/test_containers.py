import pytest


@pytest.mark.asyncio
async def test_objects(isilon_client):
    objects = await isilon_client.containers.objects("test")
    assert isinstance(objects, str)


@pytest.mark.asyncio
async def test_create(isilon_client):
    resp = await isilon_client.containers.create("teste2")
    assert resp == 200


@pytest.mark.asyncio
async def test_update_metadata(isilon_client):
    resp = await isilon_client.containers.update_metadata("teste2")
    assert resp == 200


@pytest.mark.asyncio
async def test_show_metadata(isilon_client):
    resp = await isilon_client.containers.metadata("teste2")
    assert "X-Object-Meta" in resp


@pytest.mark.asyncio
async def test_delete(isilon_client):
    resp = await isilon_client.containers.delete("teste2")
    assert resp == 200
