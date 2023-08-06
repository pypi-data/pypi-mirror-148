from distutils.log import error
from meta import iniMeta
import os


class model(metaclass=iniMeta):
    def __init__(self, source):
        assert isinstance(source, str), error("source is not str type.")
        if os.path.exists(source):
            self.Meta.source = source if isinstance(source, str) else [source]
            self.__instance__()
        else:
            raise "can't found file:'%s'" % (source)

    class Meta:
        source = None