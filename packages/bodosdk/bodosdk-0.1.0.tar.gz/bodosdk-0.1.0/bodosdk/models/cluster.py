from typing import List, Dict

import pydantic


class InstanceType(pydantic.BaseModel):
    name: str
    vcpus: int
    cores: int
    memory: int
    efa: bool


class InstanceCategory(pydantic.BaseModel):
    name: str
    instance_types: Dict[str, InstanceType]


class BodoImage(pydantic.BaseModel):
    image_id: str
    bodo_version: str