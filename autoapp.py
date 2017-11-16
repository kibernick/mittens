from flask.helpers import get_debug_flag

from mittens.factories import create_app
from mittens.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
