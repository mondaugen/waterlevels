from os import environ

class _get_env:
    def __get_env(self,name,default=None,conv=None,check_if_none=False):
        try:
            ret=environ[name]
        except KeyError:
            ret=default
            if check_if_none and ret is None:
                    raise Exception("Specify " + name + ".")
            return ret
        if conv is not None:
            return conv(ret)
        return ret
    def int(self,name,default=None):
        return self.__get_env(name,default=default,conv=int)
    def float(self,name,default=None):
        return self.__get_env(name,default=default,conv=float)
    def str(self,name,default=None):
        return self.__get_env(name,default=default)
get_env=_get_env()
