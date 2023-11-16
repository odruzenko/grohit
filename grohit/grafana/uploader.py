import copy
import logging

from grohit.grafana.client import GrafanaClient

logger = logging.getLogger(__name__)


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
        auto_version: bool = False,
        overwrite: bool = False,
        commit_message: str = "",
    ):
        version = None
        if auto_version:
            uid = dashboard_uid or dashboard["uid"]
            logger.info("Getting latest dashboard version")
            version = self.get_latest_version(uid)
            logger.info(f"Automatically calculated dashboard version: {version}")

        req_args = {
            "dashboard": dashboard,
            "dashboard_id": dashboard_id,
            "dashboard_uid": dashboard_uid,
            "version": version,
            "folder_id": folder_id,
            "folder_uid": folder_uid,
            "overwrite": overwrite,
            "commit_message": commit_message,
        }
        req_args = {k: v for k, v in req_args.items() if v is not None}
        upload_request = self.build_upload_request(**req_args)
        return self._upload_dashboard(upload_request)

    def upload_from_response_data(
        self,
        dashboard_response_data: dict,
        dashboard_id: int = None,
        dashboard_uid: str = None,
        folder_id: int = None,
        folder_uid: str = None,
        auto_version: bool = False,
        overwrite: bool = False,
        commit_message: str = "",
    ) -> dict:
        assert dashboard_response_data["dashboard"]
        assert dashboard_response_data["meta"]

        dashboard = dashboard_response_data["dashboard"]
        meta = dashboard_response_data["meta"]

        version = None
        if auto_version:
            uid = dashboard_uid or dashboard["uid"]
            logger.info("Getting latest dashboard version")
            version = self.get_latest_version(uid)
            logger.info(f"Automatically calculated dashboard version: {version}")

        meta_req_args = {
            "folder_id": meta["folderId"],
            "folder_uid": meta["folderUid"],
        }
        req_args = {
            "dashboard": dashboard,
            "dashboard_id": dashboard_id,
            "dashboard_uid": dashboard_uid,
            "version": version,
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
        version: int = None,
        overwrite: bool = False,
        commit_message: str = "",
    ) -> dict:
        logger.info("Building upload request")
        req = {
            "dashboard": copy.deepcopy(dashboard),
        }
        if dashboard_id:
            req["dashboard"]["id"] = dashboard_id
        if dashboard_uid:
            req["dashboard"]["uid"] = dashboard_uid
        if version:
            req["dashboard"]["version"] = version
        if folder_id:
            req["folder_id"] = folder_id
        if folder_uid:
            req["folder_uid"] = folder_uid
        if commit_message:
            req["message"] = commit_message
        req["overwrite"] = overwrite if overwrite is not None else False
        return req

    def get_latest_version(self, dashboard_uid: str):
        current_dashboard = self.client.get_dashboard(dashboard_uid)
        if not current_dashboard:
            return None
        current_version = current_dashboard["dashboard"]["version"]
        return current_version

    def _upload_dashboard(self, upload_request: dict):
        return self.client.upload_dashboard(**upload_request)
