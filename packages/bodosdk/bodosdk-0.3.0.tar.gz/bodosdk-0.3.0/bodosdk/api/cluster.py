from typing import Dict

from bodosdk.api.base import BackendApi
from bodosdk.models.cluster import InstanceType, InstanceCategory, BodoImage


class ClusterApi(BackendApi):

    def __init__(self, *args, **kwargs):
        super(ClusterApi, self).__init__(*args, **kwargs)
        self.resource_url = f"{self._base_url}/cluster"

    def get_available_instances(self, region) -> Dict[str, InstanceCategory]:
        resp = self._requests.get(f"{self.resource_url}/availableInstances/{region}", headers=self.get_auth_header())

        result = {}
        for row in resp.json():
            cat = InstanceCategory(
                name=row.get('label'),
                instance_types={}
            )
            for opt in row.get('options', []):
                instance_type = InstanceType(**opt.get('label'))
                cat.instance_types[instance_type.name] = instance_type
            result[cat.name] = cat
        return result

    def get_available_images(self, region) -> Dict[str, BodoImage]:
        resp = self._requests.get(f"{self.resource_url}/availableImages/{region}/worker",
                                  headers=self.get_auth_header())
        result = {}
        for row in resp.json():
            for opt in row.get('options'):
                img = BodoImage(
                    image_id=opt['label']['imageId'],
                    bodo_version=opt['label']['bodo_version']
                )
                result[img.bodo_version] = img
        return result
