from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Ruishi(BaseModel):
    pass


class UserCreate(Ruishi):
    username: str
    password: str
    token: Optional[str]
    uuid: Optional[UUID]


class User(UserCreate):
    uuid: UUID
    token: str


class Community(Ruishi):
    name: str
    uuid: UUID
    level: int


class Node(Ruishi):
    name: str = Field(alias='nodeName')
    uuid: UUID = Field(alias='nodeUuid')
    type: str = Field(alias='nodeType')
    level: int = Field(alias='nodeLevel')
    fullname: str = Field(alias='fullNodeName')


class DoorOwner(BaseModel):
    nodeName: str = Field(alias='fullNodeName')
    communityUuid: UUID = Field(alias='communityUuid')


class Door(Ruishi):
    name: str = Field(alias='deviceName')
    uuid: UUID = Field(alias='deviceCode')
    owner: DoorOwner
