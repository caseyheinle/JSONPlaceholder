import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"

class TestJSONPlaceholder:

    @pytest.mark.parametrize("post_id", [1])
    def test_get_post_by_id(self, post_id):
        res = requests.get(f"{BASE_URL}/{post_id}")
        assert res.status_code == 200
        data = res.json()
        for key in ("id", "userId", "title", "body"):
            assert key in data

    def test_get_posts_by_userId(self):
        res = requests.get(BASE_URL, params={"userId": 1})
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # for all posts in the response, userId should be 1
        for key in data:
            assert key["userId"] == 1

    def test_create_post(self):
        payload = {"title": "foo", "body": "bar", "userId": 1}
        res = requests.post(BASE_URL, json=payload)
        assert res.status_code ==201
        data = res.json()
        assert "id" in data
        for key in payload:
            assert data[key] == payload[key]

    def test_put_post(self):
        payload = {"id": 1, "title": "new title", "body": "new body", "userId": 1}
        res = requests.put(f"{BASE_URL}/1", json=payload)
        assert res.status_code == 200
        data = res.json()
        for key in payload:
            assert data[key] == payload[key]

    def test_patch_post(self):
        patch_payload = {"title": "updated"}
        res = requests.patch(f"{BASE_URL}/1", json=patch_payload)
        assert res.status_code == 200
        data = res.json()
        assert data.get("title") == "updated"

    def test_delete_post(self):
        res = requests.delete(f"{BASE_URL}/1")
        assert res.status_code == 200

    def test_get_nonexistent_post(self):
        res = requests.get(f"{BASE_URL}/99999")
        # Accept 404 or 200 with empty object/array
        assert res.status_code in (404, 200)
        try:
            data = res.json()
            assert data == {} or data == [] or data.get("id") is None
        except Exception:
            # If not JSON, that's fine for 404
            assert res.status_code == 404

    def test_post_invalid_body(self):
        """
        Test creating a post with missing required fields
        Note: JSONPlaceholder may still return 201/200, but logically this is a failure
        """
        payload = {"body": "bar", "userId": 1}
        res = requests.post(BASE_URL, json=payload)
        data = res.json()
        assert "title" in data and data["title"] is not None, "API accepted post without required 'title' field"
