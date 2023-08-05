
from dataclasses import dataclass
import dataclasses
import typing
from honkaiDex.base import DataclassNode


@dataclass
class BaseCharacter(DataclassNode):
    pass

from enum import Enum
class BattlesuitType(Enum):
    MECH = "Mech"
    PSY = "Psy"
    BIO = "Bio"
    QUA = "Qua"
    IMG = "Img"

@dataclass
class Battlesuit(DataclassNode):
    base_character : BaseCharacter
    version_released : str
    rarity : str
    tags : typing.List[str] = dataclasses.field(default_factory=lambda : [])
    img_link : str = None
    type : BattlesuitType = None
