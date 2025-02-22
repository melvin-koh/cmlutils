import os
import shutil
from datetime import datetime, timedelta
from string import Template

from cmlutils.constants import ApiV1Endpoints
from cmlutils.utils import call_api_v1



class BaseWorkspaceInteractor(object):
    # use a variable to store the apiv2 key for repeated use instead
    _apiv2_key = None

    def __init__(
        self,
        host: str,
        username: str,
        project_name: str,
        api_key: str,
        ca_path: str,
        project_slug: str,
    ) -> None:
        self.host = host
        self.username = username
        self.project_name = project_name
        self.api_key = api_key
        self.ca_path = ca_path
        self.project_slug = project_slug

    @property
    def apiv2_key(self) -> str:
        if self._apiv2_key:
            return self._apiv2_key

        endpoint = Template(ApiV1Endpoints.API_KEY.value).substitute(
            username=self.username
        )
        json_data = {
            "expiryDate": (datetime.now() + timedelta(weeks=1)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        }
        response = call_api_v1(
            host=self.host,
            endpoint=endpoint,
            method="POST",
            api_key=self.api_key,
            json_data=json_data,
            ca_path=self.ca_path,
        )
        response_dict = response.json()
        self._apiv2_key = response_dict["apiKey"]
        return self._apiv2_key

    def remove_cdswctl_dir(self, file_path: str):
        if os.path.exists(file_path):
            dirname = os.path.dirname(file_path)
            shutil.rmtree(dirname, ignore_errors=True)
