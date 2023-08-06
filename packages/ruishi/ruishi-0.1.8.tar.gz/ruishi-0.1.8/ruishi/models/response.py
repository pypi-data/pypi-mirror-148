from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, validator

from .ruishi_models import Node, Door


class Response(BaseModel):
    message: str
    status: int
    content: Optional[dict]

    @validator('status')
    def res_status(cls, v, values):
        if v != 0:
            from ruishi.erros import error_dict
            error_type = error_dict.get(v, Exception)
            raise error_type(values['message'])
        return v


class User(BaseModel):
    uuid: UUID
    appSign: str = "ruishi"
    phone: str
    name: str
    productSign: str = "community"
    username: str


class UserDetail(BaseModel):
    user: User


class LoginContent(BaseModel):
    token: str
    userDetail: UserDetail


class LoginResponse(Response):
    content: LoginContent


class Room(BaseModel):
    nodeName: str
    level: int
    nodeUuid: UUID
    nodeType: str
    fullNodeName: str
    nodeLevel: int
    communityUuid: UUID
    communityName: str

    def to_data_model(self) -> Node:
        return Node(**self.dict())


class RoomListContent(BaseModel):
    list: List[Room]


class RoomListResponse(Response):
    content: RoomListContent


class Device(BaseModel):
    deviceCode: UUID
    fullNodeName: str
    deviceName: str
    communityUuid: UUID

    def to_data_model(self) -> Door:
        return Door(**self.dict(), owner=self.dict())


class DeviceContent(BaseModel):
    list: List[Device]


class DeviceListResponse(Response):
    content: DeviceContent


class DeviceControlResponse(Response):
    pass
