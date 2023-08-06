# ruishi

睿视门禁API的封装

## 使用方法

```python
from ruishi import Ruishi
from ruishi.models import UserCreate

user = Ruishi(UserCreate(username='yourusername', password='yourpassword'))
rooms = user.get_room_list()
print([room.dict() for room in rooms])
doors = user.get_device_list([room.nodeUuid.hex for room in rooms])
print(print([door.dict() for door in doors]))
print(user.open_door('dooruuid'))
```