from importlib import import_module

from .. import settings
from .display import Display

impl = import_module(settings.DISPLAY_IMPL).impl
display = Display(impl)
