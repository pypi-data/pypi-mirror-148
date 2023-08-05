from dataclasses import dataclass
import dataclasses
import inspect
import typing
from zxutil.misc import parse_json
import inspect
def is_json_serializable(obj):
    return isinstance(obj, (str, int, float, bool, list, dict, tuple, set, frozenset))

def strip_nonjsonable_in_dict(obj1 : dict):
    obj = obj1.copy()
    for key, val in obj.items():
        if not is_json_serializable(val):
            obj.pop(key)
        
    return obj

class DataclassMeta(type):
    _instances = {}
    _nickname_instances = {}
    _partial_search_mapping : dict = {}
    _max_partial_search_history = 50
    
    def __call__(cls, *args, **kwargs):
        name : str = kwargs.pop("name", None)
        if name is None:
            raise ValueError("name is required")
        
        key_name :str = name.lower().strip()
        

        nickname : str = kwargs.pop("nickname", [])
        for nick in nickname:
            nick = nick.lower().strip()

        if not isinstance(nickname, list):
            raise ValueError("nickname must be a list")

        if cls not in cls._instances:
            kwargs["name"] = name
            kwargs["nickname"] = nickname
            item = super().__call__(*args, **kwargs)
            cls._instances[key_name] = item
            for nick in nickname:
                cls._nickname_instances[nick] = item

        return cls._instances[key_name]
        
    

@dataclass
class DataclassNode(metaclass=DataclassMeta):
    name :str
    nickname : typing.List[str]

    def __setitem__(self, key, value):
        if not hasattr(self, "_other"):
            self._other = {}
        self._other[key] = value
    
    def __getitem__(self, key):
        return self._other.get(key, None)

    def __hash__(self) -> int:
        return hash(self.name)

    def __post_init__(self):
        # get all parameters  
        self._params = inspect.signature(self.__init__).parameters
        # remove all params that start with _
        self._params = {k:v for k,v in self._params.items() if not k.startswith("_")}
        self._lock_params = True

    def __setattr__(self, name : str, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
            return

        if getattr(self, "_lock_params", False) and name in getattr(self, "_params", []):
            raise AttributeError(f"{name} cannot be changed after initialization")

        super().__setattr__(name, value)

    @classmethod
    def iterate(cls):
        for val in cls._instances.values():
            yield val

    @classmethod
    def __add_partial_result(cls, name : str, item : object):
        cls._partial_search_mapping[name] = item
        if len(cls._partial_search_mapping) > cls._max_partial_search_history:
            cls._partial_search_mapping.pop(list(cls._partial_search_mapping.keys())[0])

    @classmethod
    def get_partial(cls, name : str):
        name = name.lower().strip()

        if name in cls._partial_search_mapping:
            return cls._partial_search_mapping[name]

        target = None
        for key, val in cls._instances.items():
            if name in key:
                target = val
                break

        if target is not None:
            cls.__add_partial_result(name, target)
            return target
        
        for key, val in cls._instances.items():
            key : str
            if name in key.replace(" ", "").replace("-",""):
                target = val
                break
        
        if target is not None:
            cls.__add_partial_result(name, target)
            return target
        
        return None

    @classmethod
    def get_from_name(cls, name : str, partial : bool = False, nick : bool = False):
        name = name.lower().strip()
        if name in cls._instances:
            return cls._instances[name]
        
        if partial and (res :=cls.get_partial(name)) is not None:
            return res

        if nick and name in cls._nickname_instances:
            return cls._nickname_instances[name]
            
        return None

    def match(self, **kwargs) -> bool:
        for key, val in kwargs.items():
            if key not in self._data:
                return False
            if self._data[key] != val:
                return False
        return True

    @classmethod
    def get(cls, **kwargs) -> 'DataclassNode':
        if len(kwargs) == 0:
            return None

        if len(kwargs) == 1 and "name" in kwargs:
            return cls.get_from_name(kwargs["name"])

        for item in cls.iterate():
            item : DataclassNode
            if item.match(**kwargs):
                return item

    @classmethod
    def get_all(cls, **kwargs) -> typing.List['DataclassNode']:
        if len(kwargs) == 0:
            return list(cls.iterate())

        if len(kwargs) == 1 and "name" in kwargs:
            return [cls.get_from_name(kwargs["name"])]

        return [item for item in cls.iterate() if item.match(**kwargs)]

    @classmethod
    def create(cls,ignore :bool = False, mapping : dict =None, **kwargs) -> 'DataclassNode':
        if mapping is not None and isinstance(mapping, dict) and len(mapping) > 0:
            kwargs = {mapping.get(key, key):val for key, val in kwargs.items()}

        gathered = { k : v for k,v in kwargs.items() if k in inspect.signature(cls.__init__).parameters}
        if len(gathered) == 0:
            return None

        item = cls(**gathered)
        if len(gathered) == len(kwargs):
            return item
        
        if ignore:
            return item

        for key, val in kwargs.items():
            if key not in gathered:
                item[key] = val

        return item
        

    @classmethod
    def from_json(cls, data : typing.Union[dict, str], mapping : typing.Dict[str,str] = None):
        data = parse_json(data)
        if data is None:
            raise ValueError("data is not a valid json")

        #
        if mapping is None:
            mapping = {}
        
        
        if isinstance(data, dict):
            for key, val in data.items():
                val : dict
                val = {mapping.get(k, k):v for k,v in val.items()}
                val["name"] = key

                item = cls.create(**val)

            return

        if isinstance(data, list):
            for item in data:
                item = cls.create(**item)

    @property
    def all_names(self) -> typing.List[str]:
        # only english characters
        strip_name = self.name.lower().strip().encode("utf-8").decode("ascii", "ignore")
        no_space = strip_name.replace(" ", "")

        return [self.name] + self.nickname + [strip_name, no_space]

    def to_json(self) -> dict:
        return {k:v for k,v in self.__dict__.items() if not k.startswith("_")}