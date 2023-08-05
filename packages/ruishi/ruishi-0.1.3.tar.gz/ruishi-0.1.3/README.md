# ruishi

睿视门禁的接口封装

## 使用方法

```python
from ruishi import Ruishi

# 创建用户实例
user = Ruishi('username', 'password')
# 获取房间列表
room_list = user.get_room_list()
# 获取设备列表
device_list = user.get_device_list([room.nodeUuid for room in room_list])
# 开门请求
user.open_door()
```