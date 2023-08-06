from dataclasses import dataclass
import dataclasses
import inspect
import typing
from zxutil.FUNCS import parse_json
from zxutil.cond import CondLex
import inspect
from fuzzywuzzy import process

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
    _fields = {}
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
            cls._instances[cls] = {}

        if key_name not in cls._instances[cls]:
            kwargs["name"] = name
            kwargs["nickname"] = nickname
            item = super().__call__(*args, **kwargs)
            cls._instances[cls][key_name] = item
            for nick in nickname:
                if nick in cls._nickname_instances:
                    raise ValueError(f"nickname {nick} is already used by {cls._nickname_instances[nick]}")
                cls._nickname_instances[nick] = item

        return cls._instances[cls][key_name]
    
    def get_fields(cls):
        if cls in cls._fields:
            return cls._fields[cls]

        fields = [item.name for item in dataclasses.fields(cls)]
        cls._fields[cls] = fields
        return fields
    

@dataclass(frozen=True)
class DataclassNode(metaclass=DataclassMeta):
    name :str
    nickname : typing.List[str]
    other : typing.Dict[str, typing.Any]

    def __hash__(self) -> int:
        return hash(self.name)

    def match(self, **kwargs) -> bool:
        for key, val in kwargs.items():
            if key not in self._data:
                return False
            if self._data[key] != val:
                return False
        return True
    
    @property
    def _data(self):
        return self.__dict__

    def to_json(self) -> dict:
        return {k:v for k,v in self.__dict__.items() if not k.startswith("_")}

    #ANCHOR class methods
    @classmethod
    def iterate(cls, **kwargs):
        for val in cls._instances[cls].values():
            if val.match(**kwargs):
                yield val

    @classmethod
    def iterate_field(cls, field_name, ret_object=False, **kwargs):
        if field_name not in cls.get_fields():
            raise ValueError(f"{field_name} is not a field of {cls.__name__}")

        for val in cls._instances[cls].values():
            if not val.match(**kwargs):
                continue
            if ret_object:
                yield getattr(val, field_name), val
            else:
                yield getattr(val, field_name) 

    @classmethod
    def get_field(cls, field_name, **kwargs):
        ret = []
        for val in cls.iterate_field(field_name, **kwargs):
            ret.append(val)
        return ret

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

    @classmethod
    def fuzzy_match_names(self, name : str) -> typing.List[set]:
        names = self.get_field("name")
        processes = process.extract(name, names, limit=10)
        ret = []
        for item in processes:
            ret.append((self.get(name=item[0]), item[1]))
        return ret

    @classmethod
    def fuzzy_match_nicknames(self, name : str) -> typing.List[set]:
        nicknames = self.get_field("nickname")
        processes = process.extract(name, nicknames, limit=10)
        ret = []
        for item in processes:
            ret.append((self.get(nickname=item[0]), item[1]))
        return ret
    

    @classmethod
    def get(cls, **kwargs) -> 'DataclassNode':
        if len(kwargs) == 0:
            return None

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
        not_gathererd = {k : v for k,v in kwargs.items() if k not in inspect.signature(cls.__init__).parameters}
        if len(gathered) == 0:
            return None

        item = cls(**gathered, other=not_gathererd)
        
        return item
        