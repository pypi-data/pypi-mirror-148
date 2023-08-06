import pytest
from yarl import URL

from isilon.utils import generate_presigned_uri


@pytest.mark.parametrize(
    "uri,expected",
    [
        (
            "http://localhost:8080/v1/AUTH_test/container/myfile.pdf",
            "http://localhost:8080/v1/AUTH_test/container/myfile.pdf?temp_url_sig={sign}&temp_url_expires={expires}&filename=myfile.pdf",
        ),
        (
            "http://localhost:8080/v1/AUTH_test/container/large_file.pdf",
            "http://localhost:8080/v1/AUTH_test/container/large_file.pdf?temp_url_sig={sign}&temp_url_expires={expires}&filename=large_file.pdf",
        ),
    ],
)
def test_generate_presigned_uri(uri, expected):
    resp = generate_presigned_uri("user_key", uri)
    pattern = URL(resp)
    assert resp == expected.format(
        sign=pattern.query["temp_url_sig"], expires=pattern.query["temp_url_expires"]
    )


@pytest.mark.parametrize(
    "uri",
    [
        "http://localhost:8080/v1/AUTH_test/container//",
        "http://localhost:8080/v1/AUTH_test/container/",
        "http://localhost:8080/v1/AUTH_test/container",
        "http://localhost:8080/v1/AUTH_test/",
        "http://localhost:8080/v1/AUTH_test",
        "http://localhost:8080/v1/",
        "http://localhost:8080/v1",
        "http://localhost:8080/",
        "http://localhost:8080",
    ],
)
def test_generate_presigned_uri_invalid(uri):
    with pytest.raises(Exception):
        generate_presigned_uri("user_key", uri)
