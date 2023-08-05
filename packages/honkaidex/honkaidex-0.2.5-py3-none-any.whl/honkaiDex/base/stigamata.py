from dataclasses import dataclass
import dataclasses
import typing

from honkaiDex.base import DataclassNode

class StigPieceMetaClass(type):
    t_piece = {}
    m_piece = {}
    b_piece = {}

    def __call__(cls, *args, **kwargs):
        if "__stig_pos__" not in kwargs:
            raise ValueError("__stig_pos__ is required")
        if "__stig_set__" not in kwargs:
            raise ValueError("__stig_set__ is required")
        stig_pos = kwargs.get("__stig_pos__", None)
        if stig_pos is None:
            raise ValueError("__stig_pos__ cannot be None")
        if stig_pos < 0 or stig_pos > 3:
            raise ValueError("__stig_pos__ must be between 0 and 3")
        
        stig_set = kwargs.get("__stig_set__", None)
        if stig_set is None or not isinstance(stig_set, StigamataSet):
            raise ValueError("__stig_set__ cannot be None")
        stig_name = stig_set.name
        stig_pos = int(stig_pos)
        
        if stig_pos == 0:
            interested_dict = cls.t_piece
        elif stig_pos == 1:
            interested_dict = cls.m_piece
        else:
            interested_dict = cls.b_piece

        if stig_name not in interested_dict:
            interested_dict[stig_name] = super().__call__(*args, **kwargs)
        
        return interested_dict[stig_name]


@dataclass
class StigamataPiece(metaclass=StigPieceMetaClass):
    __stig_pos__ : int
    __stig_set__ : 'StigamataSet'

    def __post_init__(self):
        if not (0 <= self.__stig_pos__ <=2):
            raise ValueError("__stig_pos__ must be between 0 and 2")

    @property
    def pos(self) -> int:
        return self.__stig_pos__

    @property
    def is_top(self):
        return self.__stig_pos__ == 0

    @property
    def is_middle(self):
        return self.__stig_pos__ == 1

    @property
    def is_bottom(self):
        return self.__stig_pos__ == 2

    @staticmethod
    def get_top(stig_name : str):
        return StigamataPiece.t_piece.get(stig_name, None)
    
    @staticmethod
    def get_middle(stig_name : str):
        return StigamataPiece.m_piece.get(stig_name, None)

    @staticmethod
    def get_bottom(stig_name : str):
        return StigamataPiece.b_piece.get(stig_name, None)
    
    @property
    def effect(self):
        return self.__stig_set__.effect(self.__stig_pos__)


    @property
    def stigset(self) -> 'StigamataSet':
        """
        returns the stig set object of this piece
        """
        return self.__stig_set__

    def __str__(self) -> str:
        if self.is_top:
            return f"{self.__stig_set__.name} (T)"
        elif self.is_middle:
            return f"{self.__stig_set__.name} (M)"
        else:
            return f"{self.__stig_set__.name} (B)"

    @property
    def img(self):
        if self.is_top:
            return self.__stig_set__.top_img
        elif self.is_middle:
            return self.__stig_set__.mid_img
        else:
            return self.__stig_set__.bot_img


@dataclass
class StigamataSet(DataclassNode):
    top_e : str = None
    mid_e : str = None
    bot_e : str = None
    two_piece : str = None
    three_piece : str = None
    bot_img : str = None
    mid_img : str = None
    top_img : str = None
    
    def __post_init__(self):
        top = self.top
        mid = self.middle
        bot = self.bottom

    def effect(self, pos: int):
        if pos == 0:
            return self.top_e
        elif pos == 1:
            return self.mid_e
        elif pos == 2:
            return self.bot_e
        else:
            raise ValueError("pos must be between 0 and 2")

    def has_effect(self, pos: int):
        return self.effect(pos) is not None

    @property
    def has_top(self):
        return self.top_e is not None

    @property
    def has_middle(self):
        return self.mid_e is not None
    
    @property
    def has_bottom(self):
        return self.bot_e is not None

    @property
    def top(self):
        if not self.has_top:
            return None

        return StigamataPiece(
            __stig_pos__=0,
            __stig_set__=self
        )

    @property
    def middle(self):
        if not self.has_middle:
            return None

        return StigamataPiece(
            __stig_pos__=1,
            __stig_set__=self
        )
    
    @property
    def bottom(self):
        if not self.has_bottom:
            return None
    
        return StigamataPiece(
            __stig_pos__=2,
            __stig_set__=self
        )

    