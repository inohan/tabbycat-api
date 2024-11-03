import typing

UrlStr = typing.NewType("UrlStr", str)

class _NULL:
    def __repr__(self):
        return "NULL"
    
    def __bool__(self):
        return False

NULL = _NULL()