import requests
from typing import List


class GrafanaClient:
    def __init__(
        self, server_url: str, api_key: str = None, verify_ssl=True, extra_headers=None
    ):
        self.server_url = server_url
        self.api_key = api_key
        self.verify_ssl = verify_ssl

        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        if api_key:
            self._session.headers.update({"Authorization": f"Bearer {api_key}"})
        if extra_headers:
            self._session.headers.update(extra_headers)
        self._session.verify = self.verify_ssl

    def list_folders(self) -> List[dict]:
        limit = 100
        page = 1
        folders = []
        while True:
            url = f"{self.server_url}/api/folders?limit={limit}&page={page}"
            response = self._session.get(url)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            folders.extend(data)
            page += 1

        return folders

    def list_datasources(self) -> List[dict]:
        url = f"{self.server_url}/api/datasources"
        response = self._session.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    def list_dashboards(
        self, folder_id: int = None, tags: List[str] = None
    ) -> List[dict]:
        url = f"{self.server_url}/api/search"
        dashboards = []
        limit = 500
        page = 1
        while True:
            params = {
                "limit": limit,
                "page": page,
                "type": "dash-db",
            }
            if folder_id:
                params["folderIds"] = [folder_id]
            if tags:
                params["tag"] = tags
            response = self._session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            dashboards.extend(data)
            page += 1

        return dashboards

    def get_dashboard(self, uid: str) -> dict:
        url = f"{self.server_url}/api/dashboards/uid/{uid}"
        response = self._session.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    def upload_dashboard(
        self,
        dashboard: dict,
        folder_id: str = None,
        folder_uid: str = None,
        overwrite: bool = False,
        commit_message: str = None,
    ) -> dict:
        url = f"{self.server_url}/api/dashboards/db"
        data = {
            "dashboard": dashboard,
            "overwrite": overwrite,
            "folderId": folder_id,
            "folderUid": folder_uid,
            "message": commit_message,
        }
        response = self._session.post(url, json=data)
        response.raise_for_status()
        data = response.json()
        return data
