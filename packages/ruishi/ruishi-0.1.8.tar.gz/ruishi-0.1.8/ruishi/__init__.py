version = (0, 1, 8)

__name__ = 'ruishi'
__version__ = '.'.join([str(i) for i in version])

from .main import Ruishi
from .models.ruishi_models import UserCreate
