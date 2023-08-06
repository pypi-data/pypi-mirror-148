import time
from datetime import datetime
from typing import List, Optional, Any, Iterable
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class Request(BaseModel):
    version: str = Field(default='1.0')
    productSign: str = Field(default='community')
    appSign: str = Field(default='ruishi')
    requestId: UUID = Field(default_factory=uuid4)
    applyTime: datetime = Field(default_factory=lambda: int(round(time.time() * 1000)))

    @staticmethod
    def format_dict(func):
        def convert(data: Any):
            if type(data) == str:
                return data
            elif type(data) == UUID:
                return data.hex
            elif isinstance(data, Iterable):
                data_type = type(data)
                if data_type == tuple:
                    new_tuple = []
                    for i in data:
                        new_tuple.append(convert(i))
                    return tuple(new_tuple)
                elif data_type == list:
                    new_list = []
                    for i in data:
                        new_list.append(convert(i))
                    return new_list
                elif data_type == dict:
                    new_dict = {}
                    for i, v in data.items():
                        new_dict.update({i: convert(v)})
                    return new_dict
                else:
                    print(data)
                    raise ValueError('不知道什么类型')
            else:
                return data

        def inner(*args, **kwargs):
            data = func(*args, **kwargs)
            return convert(data)

        return inner

    @format_dict
    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs)

    def __repr__(self):
        return self.dict()


class LoginRequest(Request):
    username: str = Field(alias='account')
    password: str


class RoomListRequest(Request):
    pass


class DeviceListRequest(Request):
    nodeUuids: List[UUID]


class DeviceControlRequest(Request):
    deviceCode: UUID
    useruuid: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
    transactionNo: Optional[str]

    class Config:
        fields = {'timestamp': {'exclude': True},
                  'useruuid': {'exclude': True}}

    @validator('transactionNo', always=True)
    def transactionno_verify(cls, _, values):
        return f'a{values["timestamp"]}{values["useruuid"].hex}'
