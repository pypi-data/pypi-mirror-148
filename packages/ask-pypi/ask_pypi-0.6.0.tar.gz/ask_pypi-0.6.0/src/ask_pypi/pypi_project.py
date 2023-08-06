
import json
import requests
import  logging


logger = logging.getLogger(__name__)


class PackageResponse:
    def __init__(self, status_code: int):
        self._status_code = status_code

    @property
    def package_found(self):
        return self._status_code == 200

    @staticmethod
    def from_request(package_name: str):
        PROJECT_API = 'pypi.org/project'
        try:
            return PackageResponse(requests.get('https://{api_url}/{package_name}'.format(
                api_url=PROJECT_API,
                package_name=package_name,
            )).status_code)
        except Exception as error:
            logger.error("Http Request Error: " + json.dumps({
                'exception': str(error),
            }))
            raise error


def is_project(package_name: str):
    return PackageResponse.from_request(package_name).package_found
