import copy

from grohit.grafana.client import GrafanaClient


class GrafanaUploader:
    def __init__(self, client: GrafanaClient):
        self.client = client

    def upload(
        self,
        dashboard: dict,
        dashboard_id: int = None,
        dashboard_uid: str = None,
        folder_id: int = None,
        folder_uid: str = None,
        overwrite: bool = False,
        commit_message: str = "",
    ):
        pass

    def upload_from_respose_data(
        self,
        dashboard_response_data: dict,
        dashboard_id: int = None,
        dashboard_uid: str = None,
        folder_id: int = None,
        folder_uid: str = None,
        overwrite: bool = False,
        commit_message: str = "",
    ) -> dict:
        assert dashboard_response_data["dashboard"]
        assert dashboard_response_data["meta"]

        dashboard = dashboard_response_data["dashboard"]
        meta = dashboard_response_data["meta"]

        meta_req_args = {
            "folder_id": meta["folderId"],
            "folder_uid": meta["folderUid"],
        }
        req_args = {
            "dashboard": dashboard,
            "dashboard_id": dashboard_id,
            "dashboard_uid": dashboard_uid,
            "folder_id": folder_id,
            "folder_uid": folder_uid,
            "overwrite": overwrite,
            "commit_message": commit_message,
        }
        req_args = {k: v for k, v in req_args.items() if v is not None}
        req_args = {**meta_req_args, **req_args}

        upload_request = self.build_upload_request(**req_args)
        return self._upload_dashboard(upload_request)

    def build_upload_request(
        self,
        dashboard: dict,
        dashboard_id: int = None,
        dashboard_uid: str = None,
        folder_id: int = None,
        folder_uid: str = None,
        overwrite: bool = False,
        commit_message: str = "",
    ) -> dict:
        req = {
            "dashboard": copy.deepcopy(dashboard),
        }
        if dashboard_id:
            req["dashboard"]["id"] = dashboard_id
        if dashboard_uid:
            req["dashboard"]["uid"] = dashboard_uid
        if folder_id:
            req["folderId"] = folder_id
        if folder_uid:
            req["folderUid"] = folder_uid
        if commit_message:
            req["message"] = commit_message
        req["overwrite"] = overwrite if overwrite is not None else False
        return req

    def _upload_dashboard(self, upload_request: dict):
        return self.client.upload_dashboard(**upload_request)
