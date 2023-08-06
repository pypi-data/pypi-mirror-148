from typing import Dict

from bodosdk.api.cluster import ClusterApi
from bodosdk.models.cluster import InstanceCategory, BodoImage


class ClusterClient:
    def __init__(self, api: ClusterApi):
        self._api = api

    def get_available_instance_types(self, region: str) -> Dict[str, InstanceCategory]:
        """
        Returns mapping of categorized instance types

        :param region: region for which we check instance types
        :type region: str
        :return: mapping where key is category name
        :rtype: Dict[str, InstanceCategory]
        """
        return self._api.get_available_instances(region)

    def get_available_images(self, region: str) -> Dict[str, BodoImage]:
        """
        Returns mapping of bodo version and image name

        :param region: region for which we check images
        :type region: str
        :return: mapping where key is bodo version and value is object with name and version
        :rtype: Dict[str, BodoImage]
        """
        return self._api.get_available_images(region)
