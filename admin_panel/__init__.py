import falcon
# don't touch this file unless required
from . import controllers

from .resources.redis import redis as appCache