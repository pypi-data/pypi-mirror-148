# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .hash import Hash

__all__ = ["Hashes3"]


class Hashes3:
    """
    XDR Source Code::

        typedef Hash Hashes3<>;
    """

    def __init__(self, hashes3: List[Hash]) -> None:
        if hashes3 and len(hashes3) > 4294967295:
            raise ValueError(
                f"The maximum length of `hashes3` should be 4294967295, but got {len(hashes3)}."
            )
        self.hashes3 = hashes3

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.hashes3))
        for hashes3_item in self.hashes3:
            hashes3_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Hashes3":
        length = unpacker.unpack_uint()
        hashes3 = []
        for _ in range(length):
            hashes3.append(Hash.unpack(unpacker))
        return cls(hashes3)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Hashes3":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Hashes3":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hashes3 == other.hashes3

    def __str__(self):
        return f"<Hashes3 [hashes3={self.hashes3}]>"
