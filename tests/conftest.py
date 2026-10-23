from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_requests():
    """Patch requests.get/post in the client module so no real API calls are made."""
    response = MagicMock()
    response.json.return_value = {"status": "success"}
    with patch("voipms_api.voipms_client.requests.get", return_value=response) as get, \
         patch("voipms_api.voipms_client.requests.post", return_value=response) as post:
        yield get, post
