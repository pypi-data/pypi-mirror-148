import dataclasses
from typing import Dict, List, Any
from PIL import Image
import base64
import io
import uuid
import time
import datetime


TRX_TYPES = [
    "POST",
    "ANNOUNCE",
    "REQ_BLOCK_FORWARD",
    "REQ_BLOCK_BACKWARD",
    "BLOCK_SYNCED",
    "BLOCK_PRODUCED",
    "ASK_PEERID",
]


@dataclasses.dataclass
class ImgObj:
    content: Any
    mediaType: str = "image/png"
    name: str = f"{uuid.uuid4()}-{round(int(time.time()*1000000))}"

    def __post_init__(self):
        tgt = self.content
        try:
            if type(tgt) == str:
                with open(tgt, "rb") as f:
                    self.content = self.encode(f.read())
                self.mediaType = tgt.split(".")[-1]
            elif type(tgt) == bytes:
                self.content = self.encode(tgt)
            elif type(tgt) == dict:
                self.mediaType = tgt.get("mediaType") or self.mediaType
                self.content = tgt.get("content") or ""
                self.name = tgt.get("name") or self.name
        except Exception as e:
            print(e)
            return print(tgt, "must be imgpath or imgbytes")

    def encode(self, imgbytes):
        return base64.b64encode(imgbytes).decode("utf-8")


@dataclasses.dataclass
class NodeInfo:
    node_id: str
    node_publickey: str
    node_status: str
    node_type: str
    node_version: str
    peers: Dict

    def values(self):
        """供 sql 调用"""
        return (
            self.node_id,
            self.node_publickey,
            self.node_status,
            self.node_type,
            self.node_version,
            json.dumps(self.peers),
        )


@dataclasses.dataclass
class Block:
    BlockId: str
    GroupId: str
    ProducerPubKey: str
    Hash: str
    Signature: str
    TimeStamp: str


@dataclasses.dataclass
class Seed:
    genesis_block: Block.__dict__
    group_id: str
    group_name: str
    consensus_type: str
    encryption_type: str
    cipher_key: str
    app_key: str
    signature: str
    owner_pubkey: str
    owner_encryptpubkey: str = None  # 新版本似乎弃用该字段了


@dataclasses.dataclass
class SnapShotInfo:
    TimeStamp: int
    HighestHeight: int
    HighestBlockId: str
    Nonce: int
    SnapshotPackageId: str
    SenderPubkey: str


@dataclasses.dataclass
class GroupInfo:
    group_id: str
    group_name: str
    owner_pubkey: str
    user_pubkey: str
    user_eth_addr: str
    consensus_type: str
    encryption_type: str
    cipher_key: str
    app_key: str
    last_updated: int
    highest_height: int
    highest_block_id: str
    group_status: str
    snapshot_info: SnapShotInfo.__dict__


@dataclasses.dataclass
class ProfileParams:
    name: str = None
    image: str = None
    wallet: str = None

    def __post_init__(self):
        d = {}
        if self.name:
            d["name"] = self.name

        if self.image:
            d["image"] = {"mediaType": "image/png", "content": self.image}

        if self.wallet:
            d["wallet"] = [{"id": self.wallet, "type": "mixin", "name": "mixin messenger"}]

        if len(d) == 0:
            raise ValueError("Person must have name or image fields")
        self.__dict__ = d
