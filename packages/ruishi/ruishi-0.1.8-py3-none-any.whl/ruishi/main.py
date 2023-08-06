from typing import Tuple, List

import httpx

from .models import request as req_models
from .models import response as res_models
from .models import ruishi_models as data_models


class Ruishi:
    BASE_URL = 'https://acs.corelines.cn'

    class Auth(httpx.Auth):
        def __init__(self, token):
            self.token = token

        def auth_flow(self, request):
            request.headers['token'] = self.token
            yield request

    def __init__(self, user: data_models.UserCreate):
        self.client = httpx.Client(base_url=Ruishi.BASE_URL)
        self.async_client = httpx.AsyncClient(base_url=Ruishi.BASE_URL)
        self.username = user.username
        self.password = user.password
        if user.token and user.uuid:
            self.uuid = user.uuid
            self.auth = Ruishi.Auth(user.token)
        else:
            self.login()

    def login(self) -> Tuple[str, res_models.User]:
        """
        :return:更新授权并返回token和用户信息
        """
        url = '/auth/login'
        req = req_models.LoginRequest(account=self.username, password=self.password)
        res = self.client.post(url, json=req.dict(by_alias=True))
        res.raise_for_status()
        res = res_models.LoginResponse(**res.json())
        self.uuid = res.content.userDetail.user.uuid
        self.auth = Ruishi.Auth(res.content.token)
        return res.content.token, res.content.userDetail.user

    def get_room_list(self) -> List[res_models.Room]:
        """
        :return:返回房间信息列表
        """
        url = '/control/community/v1/room/list'
        req = req_models.RoomListRequest()
        res = self.client.post(url, json=req.dict(), auth=self.auth)
        res.raise_for_status()
        res = res_models.RoomListResponse(**res.json())
        return res.content.list

    def get_device_list(self, nodeuuids: List[str]) -> List[res_models.Device]:
        """
        :param nodeuuids:房间uuid列表
        :return:返回设备列表
        """
        url = '/control/device/v1/p/list'
        req = req_models.DeviceListRequest(nodeUuids=nodeuuids)
        res = self.client.post(url, json=req.dict(), auth=self.auth)
        res.raise_for_status()
        res = res_models.DeviceListResponse(**res.json())
        return res.content.list

    def open_door(self, devicecode: str) -> bool:
        """
        :param devicecode: 设备uuid
        :return:开门是否成功
        """
        url = '/control/device/v1/control'
        req = req_models.DeviceControlRequest(deviceCode=devicecode, useruuid=self.uuid)
        res = self.client.post(url, json=req.dict(), auth=self.auth)
        res.raise_for_status()
        res = res_models.DeviceControlResponse(**res.json())
        return res.status == 0
