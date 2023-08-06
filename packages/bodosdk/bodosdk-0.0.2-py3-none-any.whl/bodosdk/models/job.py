from datetime import datetime
from typing import Optional, List
from uuid import UUID

import pydantic
from pydantic import Field

from bodosdk.models.base import JobStatus, ClusterStatus, TaskStatus


class JobClusterDefinition(pydantic.BaseModel):
    instanceType: str
    workersQuantity: int
    acceleratedNetworking: bool
    imageId: str


class JobDefinition(pydantic.BaseModel):
    name: str
    command: str
    workspacePath: str
    workspaceUsername: str
    workspacePassword: str
    clusterObject: JobClusterDefinition
    workspaceReference: Optional[str] = ""
    variables: List[str] = Field(default_factory=list)
    schedule: Optional[datetime] = datetime.now()
    timeout: Optional[int] = 120


class JobClusterResponse(pydantic.BaseModel):
    name: str
    instanceType: str
    workersQuantity: int
    imageId: str
    acceleratedNetworking: bool


class JobResponse(pydantic.BaseModel):
    uuid: UUID
    name: str
    status: JobStatus
    schedule: datetime
    command: str
    variables: List[str]
    workspacePath: str
    workspaceReference: str
    cluster: JobClusterResponse


class JobExecution(pydantic.BaseModel):
    uuid: UUID
    status: TaskStatus
    logs: str
    modifyDate: datetime
    createdAt: datetime