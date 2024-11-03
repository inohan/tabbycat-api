import dataclasses
from typing import get_origin, get_args, Any

from .. import UrlStr
from .. import models
from ..models import BaseModel
from ..my_types import NULL

def to_json(_object, _type=BaseModel, include_required=True, omit_dict=None):
    if omit_dict is None:
        omit_dict = ["client", "loaded"]
    if isinstance(_type, str):
        _type = getattr(models, _type)
    if get_origin(_type) is list and isinstance(_object, list):
        return [to_json(element, get_args(_type)[0], omit_dict) for element in _object]
    if _type == UrlStr and isinstance(_object, BaseModel):
            return _object.url
    if _type is not UrlStr and isinstance(_object, BaseModel):
        return_dict = {}
        for field in dataclasses.fields(_object):
            field_value = getattr(_object, field.name)
            if field.name in _object.FIELDS_READONLY or field.name in omit_dict:
                continue
            if field_value is None:
                if include_required and field.name in _object.FIELDS_REQUIRED:
                    raise ValueError(f"{field.name} is required")
                continue
            if field_value is NULL or field_value is None:
                return_dict[field.name] = None
                continue
            field_type = field.type
            if field.name in _object.FIELDS_URL_STR:
                field_type = UrlStr
            elif field.name in _object.FIELDS_URL_LIST:
                field_type = list[UrlStr]
            return_dict[field.name] = to_json(field_value, field_type, omit_dict)
        return return_dict

    return _object


