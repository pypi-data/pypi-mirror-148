
import json
import requests
import  logging
from typing import Protocol, Callable


logger = logging.getLogger(__name__)


class PackageResponse(Protocol):
    package_found: bool


def build_request_getter() -> Callable[[str], PackageResponse]:
    PROJECT_API = 'pypi.org/project'
    def get_response(package_name: str) -> PackageResponse:
        response = requests.get('https://{api_url}/{package_name}'.format(
            api_url=PROJECT_API,
            package_name=package_name,
        ))
        return type('PackageResponse', (), {
            'package_found': response.status_code == 200
        })
    return get_response


def get_response(package_name: str):
    get_package_response = build_request_getter()
    try:
        return get_package_response(package_name)
    except Exception as error:
        logger.error("Http Request Error: " + json.dumps({
            'exception': str(error),
        }))
        raise error


def is_project(package_name: str):
    return get_response(package_name).package_found


pypi = type('PyPI', (), {
    'is_project': is_project,
})
