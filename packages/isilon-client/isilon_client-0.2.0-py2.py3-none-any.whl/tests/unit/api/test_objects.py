import pytest


@pytest.mark.asyncio
async def test_get_object(isilon_client):
    resp = await isilon_client.objects.get("container", "obj")
    assert resp is not None


@pytest.mark.asyncio
async def test_create_object(isilon_client):
    resp = await isilon_client.objects.create("container", "obj2", "mycontent")
    assert resp == 200


@pytest.mark.asyncio
async def test_copy_object(isilon_client):
    with pytest.raises(NotImplementedError):
        await isilon_client.objects.copy("container", "obj2")


@pytest.mark.asyncio
async def test_delete_object(isilon_client):
    resp = await isilon_client.objects.delete("container", "obj2")
    assert resp == 200


@pytest.mark.asyncio
async def test_show_metadata(isilon_client):
    resp = await isilon_client.objects.show_metadata("container", "obj2")
    assert "X-Object-Meta" in resp


@pytest.mark.asyncio
async def test_update_metadata(isilon_client):
    resp = await isilon_client.objects.update_metadata("container", "obj2")
    assert resp == 200
