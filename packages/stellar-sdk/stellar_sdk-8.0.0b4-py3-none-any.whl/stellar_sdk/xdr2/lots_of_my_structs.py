# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .my_struct import MyStruct

__all__ = ["LotsOfMyStructs"]


class LotsOfMyStructs:
    """
    XDR Source Code::

        struct LotsOfMyStructs
        {
            MyStruct members<>;
        };
    """

    def __init__(
        self,
        members: List[MyStruct],
    ) -> None:
        if members and len(members) > 4294967295:
            raise ValueError(
                f"The maximum length of `members` should be 4294967295, but got {len(members)}."
            )
        self.members = members

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.members))
        for members_item in self.members:
            members_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LotsOfMyStructs":
        length = unpacker.unpack_uint()
        members = []
        for _ in range(length):
            members.append(MyStruct.unpack(unpacker))
        return cls(
            members=members,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LotsOfMyStructs":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LotsOfMyStructs":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.members == other.members

    def __str__(self):
        out = [
            f"members={self.members}",
        ]
        return f"<LotsOfMyStructs {[', '.join(out)]}>"
