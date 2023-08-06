
from json import dumps
from json import dump
from json import loads
from json import load

from json import JSONEncoder
from json import JSONDecoder

from .figure import Figure

from io import TextIOWrapper
from typing import Union
from .figure import FigureType
from .figure import PointType
from .figure import LineType
from .figure import UnknownBoxType

def figdumps(fig:FigureType, **kwargs) -> str:
    if not isinstance(fig, Figure):
        raise TypeError(
            'should be inherited from figure type.'
            )

    return dumps(obj=fig.__class__.to_dict(fig), **kwargs)

def figdump(fig:FigureType, fp:TextIOWrapper, **kwargs) -> None:
    if not isinstance(fig, Figure):
        raise TypeError(
            'should be inherited from figure type.'
            )

    return dump(obj=fig.__class__.to_dict(fig), fp=fp, **kwargs)

def figloads(s:str, **kwargs) -> Union[PointType,LineType,UnknownBoxType]:
    dict_ = loads(s=s, **kwargs)

    for cls_ in Figure.__subclasses__():
        if 'cls' in dict_.keys():
            if cls_.__name__ == dict_['cls']:
                return cls_.to_instance(dict_)
        
    raise TypeError(
        'should be existing figure type.'
        )

def figload(fp:TextIOWrapper, **kwargs) -> Union[PointType,LineType,UnknownBoxType]:
    dict_ = load(fp=fp, **kwargs)

    for cls_ in Figure.__subclasses__():
        if 'cls' in dict_.keys():
            if cls_.__name__ == dict_['cls']:
                return cls_.to_instance(dict_)
        
    raise TypeError(
        'should be existing figure type.'
        )

class FigureEncoder(JSONEncoder):
    
    def default(self, obj:object) -> object:
        if isinstance(obj, Figure):
            return obj.__class__.to_dict(obj)
        
        return JSONEncoder.default(self, obj)

class FigureDecoder(JSONDecoder):

    def __init__(self):
        JSONDecoder.__init__(self, object_hook=FigureDecoder.object_hook)
    
    @staticmethod
    def object_hook(dict_:dict[str,object]) -> object:
        if 'cls' in dict_.keys():
            for cls_ in Figure.__subclasses__():
                if cls_.__name__ == dict_['cls']:

                    # return figure instance
                    return cls_.to_instance(dict_)
            
            # return dict which contains key 'cls'
            return dict_

        # return dict which not contains key 'cls'
        return dict_