from pydantic import (BaseSettings)

import inspect
import sys


class GritConfig(BaseSettings):
    debug: bool = False

    class Config(BaseSettings.Config):
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

class Folder(BaseSettings):
    title: str
    
    def __init__(self, **data):
        super().__init__(**data)
        caller = inspect.currentframe().f_back
        caller_module = sys.modules[caller.f_globals['__name__']]
        setattr(caller_module, '__folder__', self)

    class Config:
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
